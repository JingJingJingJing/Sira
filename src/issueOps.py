import requests
import json
from utils import mylog
from query import read_cookie
from query import send_request
from query import method
from utils import glob_dic

cookie_path = ''
'''
send_request(url, method, headers, params, data);
'''


def issue_create(lst):
    cookie = read_cookie()
    if not cookie:
        return 'Cookie not Found, please log in again'

    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/issue'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': cookie
    }
    data = ''
    with open("res/create.json", "r") as f:
        data = json.load(f)
        data = json.dumps(data)
    f, r = send_request(url, method.Post, headers, None, data)
    print(r)
    if not f:
        return r
    return "Issue successfully created!"


def issue_assign(lst):
    issue = lst[0]
    assignee = lst[1]
    cookie = read_cookie()
    if not cookie:
        return 'Cookie not Found, please log in again'
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/issue/' + issue + '/assignee'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': cookie
    }
    data = '{"name":"' + assignee + '"}'

    f, r = send_request(url, method.Put, headers, None, data)
    if not f:
        return r
    mylog.info(issue + ' successfully assigned to ' + assignee)
    return issue + ' successfully assigned to ' + assignee


def issue_getComment(lst):
    issue = lst[0]
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        return err
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/issue/' + issue + '/comment'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': cookie
    }
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return r

    comments = r.json()['comments']
    if len(comments) > 0:
        string = 'Here are the comments for ' + issue + ':\r\n'
        for com in comments:
            string += '"' + com['body'] + '"\r\n\twrote by ' + com['updateAuthor']['key'] + '\r\n\t' + com['created'] + '\r\n\t' + '(cid: ' + com['id'] + ')\r\n'
        mylog.info(string)
        return string
    else:
        mylog.info('get empty msg')
        return "There is no comment yet!"


def issue_addComment(lst):
    issue = lst[0]
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        return err
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/issue/' + issue + '/comment'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': cookie
    }
    data = ''
    with open("res/comments.json", "r") as f:
        data = json.load(f)
        data = json.dumps(data)
    print(data, type(data))
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        return r
    mylog.info(r.text)
    print('Comment(ID: ' + r.json()['id'] + ')added')
    return 'Comment(ID: ' + r.json()['id'] + ')added'


def issue_delComment(lst):
    issue = lst[0]
    cid = lst[1]
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        return err
    url = 'http://' + glob_dic.get_value('domain') + '/rest/api/2/issue/' + issue + '/comment/' + cid
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': cookie
    }

    f, r = send_request(url, method.Delete, headers, None, None)
    if not f:
        return r
    mylog.info('Comment {} deleted'.format(cid))
    #print('Comment(ID: '+r.json()['id']+')added')
    return 'Comment deleted'


# issue_delComment(['Test-01','10103'])
# issue_getComment(['Test-01'])
# issue_assign(['Test-01','testuser1'])
