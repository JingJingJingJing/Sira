import requests
import json
from extract import getIssue
from extract import getField
from extract import dtos
domain = '10.176.111.32:8080'
cookie_path = ''

def read_cookie():
    cookie = ''
    with open(cookie_path+"cookie.txt","r") as f:
        cookie = f.read()
    return cookie

""" This function returns all issue assigned to the user 'user' """

def query(data):

    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    try:
        r = requests.post(url,headers=headers,data=data,timeout = 3)
        if(r.status_code == 200):
            j = json.loads(r.text)
            try:
                print(j['warningMessages'])
                return j['warningMessages']
            except KeyError:
                pass
            issue_lst = getIssue(r.text, None)
            if issue_lst is not None:
                string = ''
                for i in issue_lst:
                    try:
                        string += dtos(getField(i,None),i['key']) + '\r\n'
                    except KeyError as err:
                        return_val = 'given field "{}" not found'.format(err)
                        return return_val
                print(string)
                return string
            else:
                return 'Issue not Found'
        else:
            print(str(r.status_code) +'\r\n'+ r.text)
            return str(r.status_code) + r.text 
    except requests.exceptions.RequestException as err:
        return err


'''
def query_assignee(lst):
    if len(lst) == 0:
        return None
    user = lst[0]
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    data = '{"jql":"assignee='+user+'","startAt":0, "maxResults": 15,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    try:
        r = requests.post(url,headers=headers,data=data,timeout = 3)
        if(r.status_code == 200):
            j = json.loads(r.text)
            try:
                return j['warningMessages']
            except KeyError:
                pass
            issue_lst = getIssue(r.text, None)
            if issue_lst is not None:
                string = ''
                for i in issue_lst:
                    try:
                        string += dtos(getField(i,None),i['key']) + '\r\n'
                    except KeyError as err:
                        return_val = 'given field "{}" not found'.format(err)
                        return return_val
                print(string)
                return string
            else:
                return 'Issue not Found'
        else:
            print(str(r.status_code) +'\r\n'+ r.text)
            return str(r.status_code) + r.text 
    except requests.exceptions.RequestException as err:
        return err
'''



""" This function will return all information of issue represented by pid """
'''
def query_number(lst):
    if len(lst) == 0:
        return None
    issue = lst[0]
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/issue'+issue
    headers = {'Content-Type':'application/json','cookie':cookie}

    data = '{"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    try:
        r = requests.post(url,headers=headers,data=data,timeout = 3)
        if(r.status_code == 200):
            j = json.loads(r.text)
            try:
                return j['warningMessages']
            except KeyError:
                pass
            issue_lst = getIssue(r.text, None)
            if issue_lst is not None:
                string = ''
                for i in issue_lst:
                    try:
                        string += dtos(getField(i,None),i['key']) + '\r\n'
                    except KeyError as err:
                        return_val = 'given field "{}" not found'.format(err)
                        return return_val
                print(string)
                return string
            else:
                return 'Issue not Found'
        else:
            print(str(r.status_code) +'\r\n'+ r.text)
            return str(r.status_code) + r.text 
    except requests.exceptions.RequestException as err:
        return err
'''
def query_assignee(lst):
    if len(lst) == 0:
        return None
    user = lst[0]
    
    data = '{"jql":"assignee='+user+'","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    return query(data)

def query_project(lst):
    if len(lst) == 0:
        return None
    project = lst[0]
    data = '{"jql":"project='+project+'","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    #data = '{"jql":"project=TEST"}'
    return query(data)
    

def query_type(lst):
    if len(lst) == 0:
        return None
    itype = lst[0]
    data = '{"jql":"issuetype='+itype+'","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    #print(findKey(r.text))
    #print(r.status_code)
    #print(r.text)
    return query(data)

def mypermission():
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/mypermissions?projectKey$projectId&issueKey&issueId'
    headers = {'Content-Type':'application/json','cookie':cookie}
    r = requests.get(url,headers=headers)
    #print(r.text)
    return findKey(r.text)



def findKey(s):
    lst = s.split('"')
    issue = []
    for i in range(0, len(lst)-2):
        if(lst[i] == 'key'):
            issue.append(lst[i+2])
    return issue



def watcher():
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/issue/TEST-05/watchers'
    headers = {'Content-Type':'application/json','cookie':cookie}
    r = requests.get(url,headers=headers)
 
    print(r.text)
def ltest():
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/issue/TEST-03'
    data = '{"update":{"status":[{"set":"Done"}]}}'
    headers = {'Content-Type':'application/json','cookie':cookie}
    r = requests.put(url,data = data, headers=headers)
    if(r.status_code == 200):
        print(findKey(r.text))
        return findKey(r.text)
    else:
        pass


def test():
    #query_number(['TEST-03'])
    query_assignee(['Hg'])
    query_project(['Sira'])
    query_type(['Task'])

test()