import json
from enum import Enum

import requests
from requests.status_codes import _codes

from extract import dtos, getField, getIssue, getString
from utils import mylog

domain = '10.176.111.32:8080'
cookie_path = ''

def read_cookie():
    cookie = ''
    with open(cookie_path+"cookie.txt","r") as f:
        cookie = f.read()
    return cookie

""" This function returns all issue assigned to the user 'user' """

def send_request(url, method, headers, params, data):
    r = requests.Response
    try:
        if method is method.Get:
            r = requests.get(url, headers=headers, params=params, timeout=5)
        elif method is method.Put:
            r = requests.put(url, headers=headers, data=data, timeout=5)
        elif method is method.Delete:
            r = requests.delete(url, headers=headers,data=data, timeout=5)
        else:
            r = requests.post(url, headers=headers, data=data, timeout=5)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            mylog.error(r.text)
            try:
                errmsg = r.json()['errorMessages']
                return (False,
                'Request denied!\r\nerror code:' + str(r.status_code)+' '+errmsg[0])
            except KeyError:
                return (False,
                    'Request denied!\r\nerror code: {} {}'.format(str(r.status_code), str(_codes[r.status_code][0])))
            except json.JSONDecodeError:
                return (False,
                    'Request denied!\r\nerror code: {} {}'.format(str(r.status_code), str(_codes[r.status_code][0])))
        mylog.info(r)
        return (True, r)
    except requests.exceptions.RequestException as err:
        mylog.error(err)
        return (
            False,
            'Internet error\r\nTry:\r\n\tChecking the network cables, modem, and route\r\n\tReconnecting to Wi-Fi\r\n\tRunning Network Diagnostics'
        )

def query(field1, field2, f):
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        return err
    url = 'http://'+domain+'/rest/api/2/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    data = '{"jql":"'+field1
    if f:
        data += ' and '+field2+'","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    else:
        data += '","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    flag,r = send_request(url, method.Post, headers, None, data)
    if not flag:
        print(r)
        return r
    string = getString(r.text)
    mylog.info(string)
    return string


""" This function will return all information of issue represented by pid """

''' lst = ['issue name or id'] '''
def query_number(lst):
    issue = lst[0]
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        return err

    url = 'http://'+domain+'/rest/api/2/issue/'+issue
    headers = {'Content-Type':'application/json','cookie':cookie}
    f,r = send_request(url, method.Get, headers, None, None)
    if not f:
        return r
    j = json.loads(r.text)
    try:
        mylog.error(j['warningMessages'])
        return j['warningMessages']
    except KeyError:
        try:
            string = dtos(getField(j,None),j['key'])
            mylog.info(string)
            return string
        except KeyError as err:
            mylog.error(err)
            return 'given field "{}" not found'.format(err)



def addQuotation(s):
    return '\''+s+'\''

''' lst = ['sprint name or id'] '''
def query_sprint(lst):
    return query('sprint='+ addQuotation(lst[0]),'',0)
    
''' lst = ['assignee name or id'] '''
def query_assignee(lst):
    return query('assignee='+ addQuotation(lst[0]),'',0)

''' lst = ['issuetype or issuetype id'] '''
def query_type(lst):
    return query('issuetype ='+ addQuotation(lst[0]),'',0)

''' lst = ['issue status name or id'] '''
def query_status(lst):
    return query('status='+ addQuotation(lst[0]),'',0)

''' lst = ['project name or id','issuetype or issuetype id'] '''
def query_project_type(lst):
    return query('project='+addQuotation(lst[0]),'issuetype ='+addQuotation(lst[1]),1)

''' lst = ['project name or id','assignee name or id'] '''
def query_project_assignee(lst):
    return query('project='+addQuotation(lst[0]),'assignee ='+addQuotation(lst[1]),1)

''' lst = ['project name or id','sprint name or id'] '''
def query_project_sprint(lst):
    return query('project =' + addQuotation(lst[0]), 'sprint =' + addQuotation(lst[1]), 1)

''' lst = ['project name or id','issue status name or id'] '''
def query_project_status(lst):
    return query('project =' + addQuotation(lst[0]), 'status =' + addQuotation(lst[1]), 1)

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
# query_project_type(['Sira', 'bug'])
# query_project_type(['Sira', 'task'])
# query_project_assignee(['TEST', 'Hang'])
# query_project_sprint(['Sira', '2'])
# query_project_assignee(['Sira', 'xp Zheng'])

# query_project_assignee(['TEST', 'Hang'])
# query_number(['TEST-17'])
# query_sprint(['Sira Sprint 2'])
# query_assignee(['xp zheng'])
# query_status(['In progress'])
# query_project_status(['sira','to do'])