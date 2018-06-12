import requests
import json

from extract import getIssue
from extract import getField
from extract import dtos
from login import method
from login import send_request
domain = '10.176.111.32:8080'
cookie_path = ''

def read_cookie():
    cookie = ''
    with open(cookie_path+"cookie.txt","r") as f:
        cookie = f.read()
    return cookie

""" This function returns all issue assigned to the user 'user' """


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

    j = json.loads(r.text)
    try:
        return j['warningMessages']
    except KeyError:
        pass
    issue_lst = getIssue(r.text, None)
    if len(issue_lst) > 0:
        string = ''
        for i in range(0, len(issue_lst)):
            try:
                if i == len(issue_lst)-1:
                    string += dtos(getField(issue_lst[i],None),issue_lst[i]['key'])
                else:
                    string += dtos(getField(issue_lst[i],None),issue_lst[i]['key']) + '\r\n'
            except KeyError as err:
                return_val = 'given field "{}" not found'.format(err)
                return return_val
        print(string)
        return string
    else:
        return 'Issue not Found'


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
    return query('project ='+lst[0],'sprint ='+lst[1],1)
    



def finduser(user):
    if user == '':
        return (False,'No user found!')
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        return (False,err)
    url = 'http://'+domain+'/rest/api/2/user/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    params={'username':user}
    f,r = send_request(url, method.Get, headers, params, None)
    if not f:
        return r
    j = json.loads(r.text)
    try:
        r = requests.get(url,headers=headers,timeout=3)
        if r.status_code != 200:
            return str(r.status_code) + r.text 
        j = json.loads(r.text)
        try:
            return j['warningMessages']
        except KeyError:
            pass
        try:
            string = dtos(getField(j,None),j['key']) + '\r\n'
            return string
        except KeyError as err:
            return_val = 'given field "{}" not found'.format(err)
            return return_val
    except requests.exceptions.RequestException as err:
        return err
    
