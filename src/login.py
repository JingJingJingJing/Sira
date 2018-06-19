import json

import requests

from utils import mylog
from utils import Super401
from query import read_cookie
from query import method
from query import send_request
from utils import glob_dic





project = []

''' lst = ['username','password'] '''
def login(lst):
    un = lst[0]
    pw = lst[1]
    url = 'http://' + glob_dic.get_value('domain') + '/rest/auth/1/session'
    data = '{"username":"' + str(un) + '","password":"' + str(pw) + '"}'
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, headers=headers, data=data, timeout=3)
        mylog.error(r.text)
        if r.status_code == 401:
            mylog.error("401 Unauthorized")
            raise Super401
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
            return (
                False,
                'Login failed! Please make sure that your username and password are correct!'
            )
        j = r.json()
        try:
            glob_dic.set_value('cookie', j['session']['name'] + '=' + j['session']['value'])
        except KeyError:
            mylog.error('No session information from HTTP response\r\n' +
                          r.text)
            return (False, 'session info not found!')
        f = open(glob_dic.get_value('cookie_path') + "cookie.txt", "w")
        f.write(glob_dic.get_value('cookie'))
        f.close
        mylog.info("Successfully logged in as "+un)
        return (True, "Success")
    except requests.exceptions.RequestException as err:
        mylog.error(err)
        return (False, 'Login failed due to an internet error!')


def logout():
    cookie = read_cookie()
    url = 'http://' + glob_dic.get_value('domain') + '/rest/auth/1/session'
    headers = {'Accept': 'application/json', 'cookie':cookie}
    try:
        r = requests.delete(url, headers=headers, timeout=5)
        if r.status_code == 401:
            mylog.error("401 Unauthorized")
            raise Super401
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
            mylog.error('Unknown error occured')
            return (False, 'Unknown error occured')
    except requests.exceptions.RequestException as err:
        mylog.error(err)
        return (False, 'Internet Error Occured!')

    f = open(glob_dic.get_value('cookie_path') + "cookie.txt", "w")
    f.write('')
    f.close
    glob_dic.set_value('cookie','')
    mylog.info('Successfully logged out')
    return 'Successfully logged out'

def download():
    pass

def goInto(lst, key, field):
    target = []
    for element in lst:
        tmp = element.get(field,'')
        if (tmp is not '') and (tmp not in target):
            target.append(tmp)
    if target:
        glob_dic.set_value(key,target)
        return True
    return False

def getProject():
    cookie = read_cookie()
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/project'
    headers = {'Accept': 'application/json', 'cookie':cookie}
    f, r = send_request(url, method.Get, headers, None, None)
   
    if not f:
        mylog.error(r)
        return False
    mylog.debug(r)
    return goInto(r, 'project', 'key')

def getBoard():
    cookie = read_cookie()
    url = 'http://' + glob_dic.get_value('domain') + '/rest/agile/1.0/board'
    headers = {'Accept': 'application/json', 'cookie':cookie}
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        mylog.error(r)
        return False

    lst = r.get("values")
    mylog.debug(lst)
    return goInto(lst, 'board', 'id')

def getSprint():
    cookie = read_cookie()
    headers = {'Accept': 'application/json', 'cookie':cookie}
    lst = []
    for boardid in glob_dic.get_value('board'):
        url = 'http://' + glob_dic.get_value('domain') + '/rest/agile/1.0/board/'+str(boardid)+'/sprint'
        f, r = send_request(url, method.Get, headers, None, None)
        if not f:
            mylog.error(r)
            return False
        lst += r.get("values")
    goInto(lst, 'sprint', 'name')
    return True

def getStatus():
    cookie = read_cookie()
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/status'
    headers = {'Accept': 'application/json', 'cookie':cookie}
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        mylog.error(r)
    
    return goInto(r, 'status', 'name')

def getType():
    cookie = read_cookie()
    headers = {'Accept': 'application/json', 'cookie':cookie}
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/project/type'
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        mylog.error(r)
    
    return goInto(r, 'type', 'key')
    # lst = r.get("values")
    # mylog.debug(lst)
    # return goInto(lst, 'board', 'name')

def getIssuetype():
    cookie = read_cookie()
    headers = {'Accept': 'application/json', 'cookie':cookie}
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/issuetype'
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        mylog.error(r)
    return goInto(r, 'issuetype', 'name')


login(['admin','admin'])

getStatus()
print(glob_dic.get_value('status'))
getType()
print(glob_dic.get_value('type'))
getIssuetype()
print(glob_dic.get_value('issuetype'))
