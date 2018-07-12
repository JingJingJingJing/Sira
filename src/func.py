import json
from enum import Enum
from os import F_OK, access, mkdir
from threading import Thread

import requests
from requests.status_codes import _codes

from utils import Super401, glob_dic, mylog, prepare



''' ************ login logout ************* '''
def login(lst):
    un = lst[0]
    pw = lst[1]
    url = prepare('login')[0]
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"username": un, "password": pw})
    try:
        r = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=glob_dic.get_value('timeout'),
            verify=False)
        mylog.error(r.text)
        if r.status_code == 401:
            mylog.error("401 Unauthorized")
            return False, [
                '401 Unauthorized!',
                'Please make sure the username and password are correct'
            ]
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            mylog.error(err)
            try:
                errmsg = r.json()['errorMessages'][0]
                mylog.error(errmsg)
            except KeyError:
                pass
            except json.decoder.JSONDecodeError:
                pass
            return (False, [
                'Login failed! Please make sure that your username and password are correct!'
            ])
        j = r.json()
        try:
            glob_dic.set_value(
                'cookie', j['session']['name'] + '=' + j['session']['value'])
        except KeyError:
            mylog.error('No session information from HTTP response\r\n' +
                        r.text)
            return (False, ['session info not found!'])
        f = open(glob_dic.get_value('cookie_path') + "cookie.txt", "w")
        f.write(glob_dic.get_value('cookie'))
        f.close()
        mylog.info("Successfully logged in as " + un)
        # thr = Thread(target=download, args=(None, un))
        # thr.start()
        return (True, ["Success"])
    except requests.exceptions.RequestException as err:
        return (False, ['Login failed due to an internet error!'])


def logout():
    url, headers = prepare('logout')
    try:
        r = requests.delete(url, headers=headers, timeout=5)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            pass
    except requests.exceptions.RequestException:
        pass
    f = open(glob_dic.get_value('cookie_path') + "cookie.txt", "w")
    f.write('')
    f.close
    glob_dic.set_value('cookie', '')
    mylog.info('Successfully logged out')
    return (True, ['Successfully logged out'])


''' ************** All requests are sent through this function except login logout ************** '''


def send_request(url, method, headers, params, data):
    r = requests.Response()
    try:
        if method is method.Get:
            r = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=glob_dic.get_value('timeout'),
                verify=False)
        elif method is method.Put:
            r = requests.put(
                url,
                headers=headers,
                data=data,
                timeout=glob_dic.get_value('timeout'),
                verify=False)
        elif method is method.Delete:
            r = requests.delete(
                url,
                headers=headers,
                data=data,
                timeout=glob_dic.get_value('timeout'),
                verify=False)
        elif method is method.Post:
            r = requests.post(
                url,
                headers=headers,
                data=data,
                timeout=glob_dic.get_value('timeout'),
                verify=False)
        else:
            mylog.error('Wrong method that not suppord:' + str(method))
            return (False, ['Unknown internal error occured'])
        if r.status_code == 401:
            mylog.error("401 Unauthorized")
            raise Super401()
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            mylog.error(r.text)
            sLst = [
                'Request denied!', 'error code: {} {}'.format(
                    str(r.status_code), str(_codes[r.status_code][0]))
            ]
            try:
                lst = r.json().get('errorMessages', [])
                for errors in lst:
                    sLst.append(errors)
                dic = r.json().get('errors', {})
                for key in dic:
                    sLst.append('{} '.format(dic[key]))
            except json.JSONDecodeError:
                pass
            sLst.append('Please try again')
            return (False, sLst)
        mylog.info(r)
        try:
            try:
                s = ''
                lst = r.json()['warningMessages']
                for errors in lst:
                    s += errors + '\r\n'
                mylog.error(s)
                return (False, [s])
            except KeyError:
                return (True, r.json())
            except TypeError:
                return (True, r.json())
        except json.JSONDecodeError:
            return (True, r)
    except requests.exceptions.RequestException as err:
        mylog.error(err)
        return (False, [
            'Internet error', 'Try:',
            '\tChecking the network cables, modem, and route',
            '\tReconnecting to Wi-Fi', '\tRunning Network Diagnostics'
        ])


''' ************** Queries ************** '''


class method(Enum):
    Get = 0
    Post = 1
    Put = 2
    Delete = 3


def getTarget(fields, field):
    ret = ''
    try:
        ret = fields.get(field)['name']
    except KeyError:
        try:
            ret = fields.get(field)['key']
        except KeyError:
            ret = fields.get(field)
    except TypeError:
        try:
            ret = str(fields.get(field)[0].get('name'))
        except IndexError:
            ret = str(fields.get(field))
        except TypeError:
            pass
        except AttributeError:
            ret = fields.get(field)
    if ret != '':
        return ret
    else:
        return 'Not available'


def getResponse(lst):
    if not lst:
        return ['Issue Not Found']
    defaultList = [
        'issuetype', 'assignee', 'status', 'sprint', 'fixVersions', 'summary'
    ]
    defaultHeader = [
        'IssueID', 'Type', 'Assignee', 'Status', 'Sprint', 'FixVer.', 'Summary'
    ]
    stringLst = []
    s = ''
    for i in defaultHeader:
        s += '{}'.format(i).ljust(18, ' ')
    stringLst.append(s)
    for issue in lst:
        s = '{}'.format(issue.get('key')).ljust(14, ' ') + ' |  '
        fields = issue.get('fields')
        for j, field in enumerate(defaultList):
            s += getTarget(fields, field).ljust(14, ' ')
            if j != len(defaultList) - 1:
                s += ' |  '
        stringLst.append(s)
    return stringLst


def query_number(lst):
    issue = lst[0].upper()
    url, headers = prepare('query_number', '/{}'.format(issue))
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return False, r
    return True, getResponse([r])

def query(constraint, mode='mine', limit='5', order='DESC'):
    url, headers = prepare('query')
    data = {}
    data["jql"] = '{} order by updated {}'.format(constraint, order)
    data["startAt"] = 0
    data["maxResults"] = limit
    f, r = send_request(url, method.Post, headers, None, json.dumps(data))
    if not f:
        return False, r
    ret = getResponse(r.get('issues'))
    
    if ret == ['Issue Not Found']:
        return False, ['Issue Not Found']
    else:
        return True, ret

# def query(field1, field2, counter=int(0)):
#     url, headers = prepare('query')
#     if field2:
#         field2 = 'and ' + field2
#     data = {}
#     data["jql"] = '{} {} order by updated DESC'.format(field1, field2)
#     data["startAt"] = 30
#     data["maxResults"] = 10
#     data = json.dumps(data)
#     f, r = send_request(url, method.Post, headers, None, data)
#     if not f:
#         return False, r
#     ret = getResponse(r.get('issues'))
#     print(len(ret))
#     if ret == ['Issue Not Found']:
#         return False, ['Issue Not Found']
#     else:
#         return True, ret


def addQuotation(s):
    return '\'' + s + '\''


''' lst = ['sprint name or id'] '''


def query_sprint(lst):
    return query('sprint=' + addQuotation(lst[0]), '')


''' lst = ['assignee name or id'] '''


def query_assignee(lst):
    return query('assignee=' + addQuotation(lst[0]), '')


''' lst = ['issuetype or issuetype id'] '''


def query_type(lst):
    return query('issuetype =' + addQuotation(lst[0]), '')


''' lst = ['issue status name or id'] '''


def query_status(lst):
    return query('status=' + addQuotation(lst[0]), '')


''' lst = ['project name or id','issuetype or issuetype id'] '''


def query_project_type(lst):
    return query('project=' + addQuotation(lst[0]),
                 'issuetype =' + addQuotation(lst[1]))


''' lst = ['project name or id','assignee name or id'] '''


def query_project_assignee(lst):
    return query('project=' + addQuotation(lst[0]),
                 'assignee =' + addQuotation(lst[1]))


''' lst = ['project name or id','sprint name or id'] '''


def query_project_sprint(lst):
    return query('project =' + addQuotation(lst[0]),
                 'sprint =' + addQuotation(lst[1]))


''' lst = ['project name or id','issue status name or id'] '''


def query_project_status(lst):
    return query('project =' + addQuotation(lst[0]),
                 'status =' + addQuotation(lst[1]))

if __name__ == '__main__':
    print(query_sprint(['Test sprint 1']))
    pass