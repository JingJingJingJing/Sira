import json
from enum import Enum

import requests
from requests.status_codes import _codes

from extract import dtos, getField, getIssue, getString
from utils import mylog
from utils import Super401
from utils import glob_dic




def read_cookie():
    if glob_dic.get_value('cookie') == '' or glob_dic.get_value('cookie') is None:
        try:
            with open(glob_dic.get_value('cookie_path') + "cookie.txt", "r") as f:
                glob_dic.set_value('cookie',f.read())
                f.close()
        except FileNotFoundError as err:
            mylog.error(err)
            raise Super401
    return glob_dic.get_value('cookie')
        


""" This function returns all issue assigned to the user 'user' """


def send_request(url, method, headers, params, data):
    r = requests.Response
    try:
        if method is method.Get:
            r = requests.get(url, headers=headers, params=params, timeout=5)
        elif method is method.Put:
            r = requests.put(url, headers=headers, data=data, timeout=5)
        elif method is method.Delete:
            r = requests.delete(url, headers=headers, data=data, timeout=5)
        else:
            r = requests.post(url, headers=headers, data=data, timeout=5)
        if r.status_code == 401:
            mylog.error("401 Unauthorized")
            raise Super401
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            mylog.error(r.status_code)
            mylog.error(r.text)
            try:
                lst = r.json().get('errorMessages')
                if (lst is not None) and (lst != []):
                    string = 'Request denied!\r\nerror code: {}. May be one of the listed reasons\r\n'.format(str(r.status_code))
                    # print('Request denied!\r\nerror code:{}'.format(str(r.status_code))
                    for all_errors in lst:
                        string += all_errors + '\r\n'
                    return (False, string)
                dic = r.json().get('errors')
                if (dic is not None) and (dic != {}):
                    s = 'Request denied!\r\nerror code:{} '.format(str(
                        r.status_code))
                    for key in dic:
                        s+='{} '.format(dic[key])
                    return (False,s)
            except json.JSONDecodeError:
                pass
            return (False, 'Request denied!\r\nerror code: {} {}'.format(
                str(r.status_code), str(_codes[r.status_code][0])))
        mylog.info(r)
        return (True, r.json())
    except requests.exceptions.RequestException as err:
        mylog.error(err)
        return (
            False,
            'Internet error\r\nTry:\r\n\tChecking the network cables, modem, and route\r\n\tReconnecting to Wi-Fi\r\n\tRunning Network Diagnostics'
        )


def query(field1, field2, f):
    cookie = read_cookie()
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/search'
    headers = {'Content-Type': 'application/json', 'cookie': cookie}
    data = '{"jql":"' + field1
    if f:
        data += ' and ' + field2 + '","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    else:
        data += '","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    flag, r = send_request(url, method.Post, headers, None, data)
    if not flag:
        return r
    string = getString(r)
    mylog.info(string)
    return string


""" This function will return all information of issue represented by pid """
''' lst = ['issue name or id'] '''
def query_number(lst):
    issue = lst[0]
    cookie = read_cookie()
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/issue/' + issue
    headers = {'Content-Type': 'application/json', 'cookie': cookie}
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return r
    try:
        mylog.error(r['warningMessages'])
        return r['warningMessages']
    except KeyError:
        try:
            string = dtos(getField(r, None), r['key'])
            mylog.info(string)
            return string
        except KeyError as err:
            mylog.error(err)
            return 'given field "{}" not found'.format(err)


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


# def test():
#     query_number(['sira-21'])
#     query_assignee([''])
#     query_assignee(['xp zheng'])
#     query_type(['story'])
#     query_sprint(['Spike'])
#     query_project_type(['Sira', 'bug'])
#     pass
#     '''
#     options = {
#     'server': 'http://10.176.111.32:8080',
#     'cookies': {'JSESSIONID':'DD537C56B9ABD14EEAA710C6BE539644'}
#     }

#     jira = JIRA(options)
#     '''

# test()
if __name__ == '__main__':
    # query_project_type(['Sira', 'bug'])
    # query_project_type(['Sira', 'task'])
    # query_project_assignee(['TEST', 'Hang'])
    # query_project_sprint(['Sira', '2'])
    # query_project_assignee(['Sira', 'xp Zheng'])

    # query_project_assignee(['TEST', 'Hang'])
    # query_number(['TEST-17'])
    # query_sprint(['Sira Sprint 2'])
    # query_assignee(['testuser1'])
    # query_status(['In progress'])
    # query_project_status(['sira','to do'])
    pass