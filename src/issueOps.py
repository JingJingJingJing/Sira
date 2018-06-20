import requests
import json
from utils import mylog
from query import read_cookie
from query import send_request
from query import method
from utils import glob_dic
from utils import prepare, issue_create_args
from receiver import issue_create_data

issue_list = []
'''
send_request(url, method, headers, params, data);
'''
default_order = ['project', 'summary', 'issuetype']

def todic(lst):
    for i in range(0,len(default_order)):
        issue_create_args[default_order[i]] = lst[i]


def issue_create(lst):
    todic(lst)
    url, headers = prepare('issue')
    data = json.dumps(issue_create_data())
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        print(r)
        return r
    msg = 'Issue {} successfully created!'.format(r['key'])
    mylog.info(msg)
    return msg

def issue_delete(lst):
    msg = ''
    for issue in lst:
        msg += '{}\r\n'.format(issue_delete_helper(issue))
    msg += 'Done!'
    return msg

def issue_delete_helper(issue):
    url, headers = prepare('issue')
    url += '/{}'.format(issue)
    f, r = send_request(url, method.Delete, headers, None, None)
    if not f:
        return 'DOING {}\r\n{}'.format(issue, r)
    msg = '{} successfully deleted!'.format(issue)
    mylog.info(msg)
    return msg


# def finduser(user):
#     url,headers = prepare('search')
#     params={'username':user}
#     f,r = send_request(url, method.Get, headers, params, None)
#     if not f:
#         return r
#     return r.get('key')

def issue_assign(lst):
    issue = lst[0]
    assignee = lst[1]
    url, headers = prepare('issue')
    url += '/{}/assignee'.format(issue)
    # user_key = finduser(assignee)
    # if not user_key:
    #     return 'User not found!'
    data = '{"name":"' + assignee + '"}'

    f, r = send_request(url, method.Put, headers, None, data)
    if not f:
        return r
    msg = '{} successfully assigned to {}'.format(issue, assignee)
    mylog.info(msg)
    return msg


def issue_getComment(lst):
    issue = lst[0]
    url, headers = prepare('issue')
    url += issue + '/comment'
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return r

    comments = r.json().get('comments',[])
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
    url, headers = prepare('issue')
    url += issue + '/comment'
    data = ''
    with open("res/comments.json", "r") as f:
        data = json.load(f)
        data = json.dumps(data)
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        return r
    mylog.info(r.text)
    return 'Comment(ID: ' + r.json()['id'] + ')added'


def issue_delComment(lst):
    issue = lst[0]
    cid = lst[1]
    url, headers = prepare('issue')
    url += issue + '/comment/' + cid
    f, r = send_request(url, method.Delete, headers, None, None)
    if not f:
        return r
    mylog.info('Comment {} deleted'.format(cid))
    return 'Comment deleted'

# for i in range(0,11):
#     a = 'This is test. Iteration '+ str(i)
#     issue_create(['TEST',a, 'Task'])

# issue_assign(['TEST-38','hang'])
# issue_assign(['TEST-29','hang'])
# finduser('xp zheng')
# finduser('yuhang4')
# issue_delComment(['Test-01','10103'])
# issue_getComment(['Test-01'])
# issue_assign(['Test-01','testuser1'])
