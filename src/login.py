import requests
import json
import logging
from enum import Enum
domain = '10.176.111.32:8080'
cookie_path = ''

def login(lst):
    un = lst[0]
    pw = lst[1]
    url = 'http://'+domain+'/rest/auth/1/session'
    data = '{"username":"'+str(un)+'","password":"'+str(pw)+'"}'
    headers = {'Content-Type':'application/json'}
    flag,r = send_request(url, method.Post, headers, None, data)
    if not flag:
        return (False,r)
    j = json.loads(r.text)
    try:
        cookie = j['session']['name'] + '=' + j['session']['value']
    except KeyError:
        return (False, 'session info not found!')
    f = open(cookie_path+"cookie.txt","w")
    f.write(cookie)
    f.close
    return(True, "Success")

def logout():
    f = open(cookie_path+"cookie.txt","w")
    f.write('')
    f.close

def send_request(url, method, headers, params, data):
    r = requests.Response
    try:
        if method is method.Get:
            r = requests.get(url,headers=headers,params=params,timeout=5)
        else:
            r = requests.post(url,headers=headers,data=data,timeout = 5)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            return(False, err)
        return (True,r)
    except requests.exceptions.RequestException as err:
        return (False,err)

class method(Enum):
    Get = 0
    Post = 1