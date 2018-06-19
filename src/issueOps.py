import requests
import json
from utils import mylog
from query import read_cookie
from query import send_request
from query import method
domain = '10.176.111.32:8080'
cookie_path = ''
'''
send_request(url, method, headers, params, data);
'''


def issue_create(lst):
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        return err

    url = 'http://' + domain + '/rest/api/2/issue'
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
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        return err
    url = 'http://' + domain + '/rest/api/2/issue/' + issue + '/assignee'

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
    url = 'http://' + domain + '/rest/api/2/issue/' + issue + '/comment'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': cookie
    }
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return r
    comments = r.json()['comments']
    string = 'Here are the comments for ' + issue + ':\r\n'
    for com in comments:
        string += '"' + com['body'] + '"\r\n\twrote by ' + com['updateAuthor']['key'] + '\r\n\t' + com['created'] + '\r\n\r\n'
    mylog.info(string)
    return string


def issue_addComment(lst):
    issue = lst[0]
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        return err
    url = 'http://' + domain + '/rest/api/2/issue/' + issue + '/comment'
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
    return 'Comment added'


# issue_addComment(['Test-01'])
# issue_getComment(['Test-01'])
