import json
from enum import Enum

import requests
from requests.status_codes import _codes

from extract import dtos, getField, getString
from utils import Super401, glob_dic, mylog, prepare, read_cookie
""" This function returns all issue assigned to the user 'user' """


def send_request(url, method, headers, params, data):
    r = requests.Response
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
            return (False, 'Unknown internal error occured')
        if r.status_code == 401:
            mylog.error("401 Unauthorized")
            raise Super401()
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            mylog.error(r.text)
            s = 'Request denied!\r\nerror code: {} {}\r\n'.format(
                str(r.status_code), str(_codes[r.status_code][0]))
            try:
                lst = r.json().get('errorMessages', [])
                for errors in lst:
                    s += errors + '\r\n'
                dic = r.json().get('errors', {})
                for key in dic:
                    s += '{} '.format(dic[key]) + '\r\n'
            except json.JSONDecodeError:
                pass
            s += 'Please try again'
            mylog.error(s)
            return (False, s)
        mylog.info(r)
        try:
            try:
                s = ''
                lst = r.json()['warningMessages']
                for errors in lst:
                    s += errors + '\r\n'
                mylog.error(s)
                return (False, s)
            except KeyError:
                return (True, r.json())
            except TypeError:
                return (True, r.json())
        except json.JSONDecodeError:
            return (True, r)
    except requests.exceptions.RequestException as err:
        mylog.error(err)
        return (False,
                '''Internet error\r\nTry:\r\n\tChecking the network cables, 
            modem, and route\r\n\tReconnecting to Wi-Fi\r\n\tRunning Network Diagnostics'''
                )


def query(field1, field2, f):
    url, headers = prepare('query')
    if field2:
        field2 = 'and ' + field2
    data = {}
    data["jql"] = '{} {}'.format(field1, field2)
    data["startAt"] = 0
    data["maxResults"] = 100
    # data["fields"] = [
    #     "summary", "issuetype", "project", "fixVersions", "assignee", "status"
    # ]
    data = json.dumps(data)
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        return False, r
    return True, getResponse(r.get('issues'))


""" This function will return all information of issue represented by pid """
''' lst = ['issue name or id'] '''
''' add issue id after get address from address book'''

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
        ret = str(fields.get(field))
    if ret != '':
        return ret
    else:
        return 'Not available'
    




def getResponse(lst):
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
    for i, issue in enumerate(lst):
        s = '{}'.format(issue.get('key')).ljust(14, ' ')+ ' |  '
        fields = issue.get('fields')
        for j, field in enumerate(defaultList):
            s += getTarget(fields,field).ljust(14, ' ')
            if j != len(defaultList) - 1:
                s +=  ' |  '
        stringLst.append(s)
    return stringLst

                
        
    


def query_number(lst):
    issue = lst[0].upper()
    url, headers = prepare('query_number', '/{}'.format(issue))
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return False, r
    return True, getResponse([r])

    # print(string)
    # return True



def addQuotation(s):
    return '\'' + s + '\''


''' lst = ['sprint name or id'] '''


def query_sprint(lst):
    return query('sprint=' + addQuotation(lst[0]), '', 0)


''' lst = ['assignee name or id'] '''


def query_assignee(lst):
    return query('assignee=' + addQuotation(lst[0]), '', 0)


''' lst = ['issuetype or issuetype id'] '''


def query_type(lst):
    return query('issuetype =' + addQuotation(lst[0]), '', 0)


''' lst = ['issue status name or id'] '''


def query_status(lst):
    return query('status=' + addQuotation(lst[0]), '', 0)


''' lst = ['project name or id','issuetype or issuetype id'] '''


def query_project_type(lst):
    return query('project=' + addQuotation(lst[0]),
                 'issuetype =' + addQuotation(lst[1]), 1)


''' lst = ['project name or id','assignee name or id'] '''


def query_project_assignee(lst):
    return query('project=' + addQuotation(lst[0]),
                 'assignee =' + addQuotation(lst[1]), 1)


''' lst = ['project name or id','sprint name or id'] '''


def query_project_sprint(lst):
    return query('project =' + addQuotation(lst[0]),
                 'sprint =' + addQuotation(lst[1]), 1)


''' lst = ['project name or id','issue status name or id'] '''


def query_project_status(lst):
    return query('project =' + addQuotation(lst[0]),
                 'status =' + addQuotation(lst[1]), 1)


class method(Enum):
    Get = 0
    Post = 1
    Put = 2
    Delete = 3


if __name__ == '__main__':

    # query_project_type(['Tangram', 'bug'])
    # query_project_type(['Sira', 'task'])
    # query_project_assignee(['TEST', 'Hang'])
    # query_project_sprint(['Sira', '2'])
    # query_project_assignee(['sira', 'xp zheng'])

    # query_project_assignee(['TEST', 'admin'])
    # query_number(['TEST-88'])
    # query_sprint(['Sira Sprint 2'])
    # query_number(['test-88'])
    query_assignee(['ysg'])
    # query_status(['In progress'])
    # query_project_status(['sira','to do'])
    pass
