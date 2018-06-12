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

def query(f, data):
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    data = '{"jql":"'+f+'='+data+'","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    try:
        r = requests.post(url,headers=headers,data=data,timeout = 3)
        if(r.status_code == 200):
            j = json.loads(r.text)
            try:
                return j['warningMessages']
            except KeyError:
                pass
            issue_lst = getIssue(r.text, None)

            if len(issue_lst) > 0:
                string = ''
                for i in issue_lst:
                    try:
                        string += dtos(getField(i,None),i['key']) + '\r\n'
                    except KeyError as err:
                        return_val = 'given field "{}" not found'.format(err)
                        return return_val
                return string
            else:
                return 'Issue not Found'
        else:
            return str(r.status_code) + "Failed"
    except requests.exceptions.RequestException as err:
        return err

def finduser(user):
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/user/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    data={'username':user}
    try:
        r = requests.get(url,headers=headers,params=data,timeout=3)
        if r.status_code != 200:
            return (0,str(r.status_code) + r.text)
        j = json.loads(r.text)
        try:
            return (1,j[0]['key'])
        except KeyError:
            return (0,'No user found!')
        except IndexError:
            return (0,'No user found!')
    except requests.exceptions.RequestException as err:
        return (0,err)

""" This function will return all information of issue represented by pid """

def query_number(lst):
    if len(lst) == 0:
        return None
    issue = lst[0]
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/issue/'+issue
    headers = {'Content-Type':'application/json','cookie':cookie}
    try:
        r = requests.get(url,headers=headers,timeout=3)
        if r.status_code != 200:
            return str(r.status_code) + "Failed"
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

def query_sprint(lst):
    if len(lst) == 0:
        return None
    sp = lst[0]
    return query('sprint', sp)
    
def query_assignee(lst):
    if len(lst) == 0:
        return None
    
    sign, data = finduser(lst[0])
    if sign:
        return query('assignee', data)
    else:
        return data

def query_project(data,p,t):
    cookie = read_cookie()
    url = 'http://'+domain+'/rest/api/2/search'
    headers = {'Content-Type':'application/json','cookie':cookie}
    data = '{"jql":"project='+data+' and '+p+'='+t+'","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}'
    try:
        r = requests.post(url,headers=headers,data=data,timeout = 3)
        if(r.status_code == 200):
            
            j = json.loads(r.text)
            try:
                return j['warningMessages']
            except KeyError:
                
                pass
            issue_lst = getIssue(r.text, None)

            if len(issue_lst) > 0:
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
            return str(r.status_code) + "Failed"
    except requests.exceptions.RequestException as err:
        return err


def query_project_type(lst):
    return query_project(lst[0],'issuetype',lst[1])
def query_project_user(lst):
    sign, data = finduser(lst[1])
    if sign:
        return query_project(lst[0],'assignee',data)
    else:
        return data
def query_project_sprint(lst):
    return query_project(lst[0],'sprint',lst[1])
    


def query_type(lst):
    if len(lst) == 0:
        return None
    itype = lst[0]
    return query('issuetype', itype)


def getBoard():
    cookie = read_cookie()
    url = 'http://10.176.111.32:8080/rest/agile/1.0/board'
    headers = {'Content-Type':'application/json','cookie':cookie}
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
    
def test():
    #query_number(['sira-21'])
    #query_assignee([''])
    #query_assignee(['xp zheng'])
    #query_project(['Sira'])
    #query_type(['epic'])
    #query_sprint(['2'])
    #query_sprint([''])
    #query_project_type(['Sirsdf'])
    pass
    '''
    options = {
    'server': 'http://10.176.111.32:8080',
    'cookies': {'JSESSIONID':'DD537C56B9ABD14EEAA710C6BE539644'}
    }
    
    jira = JIRA(options)
    '''
#test()
#query_project_type(['Sira','bug'])
#query_project_type(['Sira','task'])
#query_project_user(['Sira','Hang'])
#query_project_sprint(['Sira','2'])
#query_project_user(['Sira','xp Zheng'])
