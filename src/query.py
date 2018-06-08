import requests
import json
from extract import getIssue
from extract import getField

domain = '10.176.111.32:8080'
cookie_path = ''

def read_cookie():
    cookie = ''
    with open(cookie_path+"cookie.txt","r") as f:
        cookie = f.read()
    return cookie

""" This function returns all issue assigned to the user 'user' """
def query_assignee(user):
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/search?jql=assignee='+user
    headers = {'Content-Type':'application/json','cookie':cookie}
    r = requests.get(url,headers=headers)
    if(r.status_code == 200):
        print("!!!!!!!")
        print(r.text)

        print("!!!!!!!")
        print(findKey(r.text))
        return findKey(r.text)
    else:
        print(r.status_code,r.text)
    # need to extract information from r.text

def test_assign():
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    '''type | number | title | assignee | sprint | status | fixed version | project '''
    data = '{"jql":"assignee=Hang","startAt":0, "maxResults": 15,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    r = requests.post(url,headers=headers,data=data)
    if(r.status_code == 200):
        print("!!!!!!!")
        #jdata = json.loads(r.text)
        #print(r.text)
        ans = getIssue(r.text, 'TEST-3')
        if ans is not None:
            print("       *****")
            getField(ans,None)
            print("       *****")
        print("!!!!!!!")
    else:
        print(r.status_code,r.text)




""" This function will return all information of issue represented by pid """
def query_project(project):
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    data = '{"jql":"key='+str(project)+'","startAt":0,"maxResults":2,"fields":["id","key"]}'
    #data = '{"jql":"project=TEST"}'
    r = requests.post(url,headers=headers,data=data)
    #print(r)
    #print(r.status_code)
    #print(r.text)
    findKey(r.text)

def query_type(itype):
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    data = '{"jql":"issuetype='+str(itype)+'","startAt":0,"maxResults":2,"fields":["id","key"]}'
    r = requests.post(url,headers=headers,data=data)
    #print(findKey(r.text))
    #print(r.status_code)
    #print(r.text)
    return findKey(r.text)

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
    print(r.status_code)
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
        print(r.status_code,r.text)


def test():
    test_assign()

test()