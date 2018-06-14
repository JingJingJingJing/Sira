import json
import logging
from enum import Enum

import requests
from requests.status_codes import _codes

from extract import dtos, getField, getIssue, getString
from login import login

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
        else:
            r = requests.post(url, headers=headers, data=data, timeout=5)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(err)
            # print('Request denied!\r\nerror code:' + str(r.status_code) +
                #   '\r\n' + str(_codes[r.status_code][0]))
            return (False,
                    'Request denied!\r\nerror code:' + str(r.status_code))
        logging.info(r)
        return (True, r)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return (
            False,
            'Internet error\r\nTry:\r\n\tChecking the network cables, modem, and route\r\n\tReconnecting to Wi-Fi\r\n\tRunning Network Diagnostics'
        )


def finduser(user):
    if user == '':
        return (False, 'No user found!')
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        logging.error(err)
        return (False, "Please log in first")
    url = 'http://' + domain + '/rest/api/2/user/search'
    headers = {'Content-Type': 'application/json', 'cookie': cookie}
    params = {'username': user}
    f, r = send_request(url, method.Get, headers, params, None)
    if not f:
        logging.error(r)
        return (False, r)
    j = json.loads(r.text)
    try:
        return (True, j[0]['key'])
    except KeyError as err:
        logging.error(err)
        return (False, 'No user found!')
    except IndexError as err:
        logging.error(err)
        return (False, 'No user found!')


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
        return r
    string = getString(r.text)
    logging.error(string)
    return string


""" This function will return all information of issue represented by pid """

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
        return j['warningMessages']
    except KeyError:
        try:
            return dtos(getField(j,None),j['key'])
        except KeyError as err:
            return 'given field "{}" not found'.format(err)



def query_sprint(lst):
    return query('sprint='+ lst[0],'',0)
    
def query_assignee(lst):
    sign, data = finduser(lst[0])
    if sign:
        return query('assignee='+ data,'',0)
    else:
        return data

def query_type(lst):
    print(lst)
    return query('issuetype ='+ lst[0],'',0)

def query_project_type(lst):
    return query('project='+lst[0],'issuetype ='+lst[1],1)

def query_project_assignee(lst):
    sign, data = finduser(lst[1])
    if sign:
        return query('project ='+lst[0],'assignee ='+data,1)
    else:
        return data

def query_project_sprint(lst):
    return query('project =' + lst[0], 'sprint =' + lst[1], 1)


class method(Enum):
    Get = 0
    Post = 1


def test():
    login(["ysg", "Yh961130"])
    query_number(['sira-21'])
    query_assignee([''])
    query_assignee(['xp zheng'])
    query_type(['story'])
    query_sprint(['2'])
    query_project_type(['Sira', 'bug'])
    pass
    '''
    options = {
    'server': 'http://10.176.111.32:8080',
    'cookies': {'JSESSIONID':'DD537C56B9ABD14EEAA710C6BE539644'}
    }
    
    jira = JIRA(options)
    '''


test()
query_project_type(['Sira', 'bug'])
query_project_type(['Sira', 'task'])
query_project_assignee(['Sira', 'Hang'])
query_project_sprint(['Sira', '2'])
query_project_assignee(['Sira', 'xp Zheng'])
