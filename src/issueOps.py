import requests
import json
from utils import mylog
from query import read_cookie
from query import send_request
from query import method
from utils import glob_dic
from utils import prepare
from login import login
from login import goInto
from login import getSprint
from login import getIssueFromSprint

issue_list = []
'''
send_request(url, method, headers, params, data);
'''


def addfield(dic, lst):
    reporter = {"name": lst[0]}
    priority = {"name": lst[1].capitalize()}
    labels = lst[2].split(' ')
    description = lst[3]
    assignee = {"name": lst[4]}
    fields = [reporter, priority, labels, description, assignee]
    extend = ['reporter', 'priority', 'labels', 'description', 'assignee']
    for i in range(0, len(lst)):
        if lst[i]:
            dic[extend[i]] = fields[i]
    return dic


'''
lst = [project, issuetype, summary, reporter, 
    priority, lable, description, assignee, sprint]
'''


def issue_assign_sprint(issue, sprint):
    sprint = sprint.split(' ')
    sprint[0] = sprint[0].upper()
    sprint[1] = sprint[1].capitalize()
    sprint = ' '.join(sprint)
    getSprint()
    url, headers = prepare(
        'assign_sprint', '/{}/issue'.format(
            glob_dic.get_value('sid').get(sprint)))
    data = {}
    data['issues'] = [issue]
    data = json.dumps(data)
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        mylog.error('Problem occured during assigning sprint\r\n{}'.format(r))
        return False, 'Issue {} failed to assigned to {}\r\n{}'.format(issue, sprint,r)
    return True, 'Issue {} successfully assigned to {}'.format(issue, sprint)


def issue_create(lst):
    url, headers = prepare('issue')
    project = {"key": lst[0].upper()}
    issuetype = {"name": lst[1].capitalize()}
    summary = lst[2]
    field = {"project": project, "summary": summary, "issuetype": issuetype}
    data = json.dumps({"fields": addfield(field, lst[3:8])})
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        return r
    new_issue = r.get('key')
    if lst[8] is not '':
        f, r = issue_assign_sprint(new_issue,lst[8])
        if not f:
            return 'Problem occured while assigning the issue to target sprint: Issue {} successfully created but not assigned to {}!\r\n{}'.format(
                 new_issue, lst[8],r)
    msg = 'Issue {} successfully created!'.format(new_issue)
    mylog.info(msg)
    return msg


def issue_get_tansition(issue, dic):
    url, headers = prepare('issue', '/{}/transitions'.format(issue))
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return None
    for msg in r.get('transitions'):
        dic[msg.get('name')] = msg.get('id')
    return dic


def issue_transit(lst):
    issue = lst[0]
    status = lst[1].title()
    url, headers = prepare(
        'issue', '/{}/transitions?expand=transitions.fields'.format(issue))
    data = {}
    dic = {}
    if not issue_get_tansition(issue, dic):
        return False, 'no transit is avaiable'
    transition = {"id": dic.get(status)}
    data = json.dumps({"transition": transition})
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        return False, 'Error occured durin transit\r\n{}'.format(r)
    msg = 'Status of {} has been changed to {}'.format(issue, status)
    mylog.info(msg)
    return True, msg


'''
lst = [status, issuetype, summary, reporter, 
    priority, lable, description, assignee, sprint]
'''

# def query_number(lst):
#     issue = lst[0]
#     url, headers = prepare('query_number', '/{}'.format(issue))
#     f, r = send_request(url, method.Get, headers, None, None)
#     if not f:
#         return r
#     try:
#         mylog.error(r['warningMessages'])
#         return r['warningMessages']
#     except KeyError:
#         try:
#             string = dtos(getField(r, None), r['key'])
#             mylog.info(string)
#             return string
#         except KeyError as err:
#             mylog.error(err)
#             return 'given field "{}" not found'.format(err)
def issue_display_info(issue):
    url, headers = prepare('query_number', '/{}'.format(issue))
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return False, r
    dic = r.get('fields')
    s = 'Here are the information of {}:\r\n'.format(issue)
    lst = ['status', 'issuetype', 'summary', 'reporter', 
    'priority', 'lable', 'description', 'assignee']
    for field in lst:
        obj = dic.get(field)
        if isinstance(obj,dict):
            s += '{}: {}\r\n'.format(field,obj.get('name'))
        else:
            s += '{}: {}\r\n'.format(field,dic.get(field))
    if getIssueFromSprint():
        sprint = glob_dic.get_value('issues')[issue]
    s += '{}: {}\r\n'.format('sprint',sprint)
    s += 'Please choose from the fields above to update'
    print(s)
    return True, s
# issue_display_info('TEST-77')


issue_display_info('TEST-77')

def issue_edit(lst):
    issue = lst[0]
    lst = lst[1:]
    url, headers = prepare('issue', '/{}'.format(issue))
    status = lst[0]
    if not issue_transit([issue, status]):
        return 'Error occured during transit'

    issuetype = {"name": lst[1].capitalize()}
    summary = lst[2]
    reporter = {"name": lst[3]}
    priority = {"name": lst[4].capitalize()}
    labels = lst[5].split(' ')
    description = lst[6]
    assignee = {"name": lst[7]}
    fields = [
        issuetype, summary, reporter, priority, labels, description, assignee
    ]
    keys = [
        'issuetype', 'summary', 'reporter', 'priority', 'labels',
        'description', 'assignee'
    ]
    dic = {}
    for i in range(0, len(fields)):
        if lst[i]:
            dic[keys[i]] = fields[i]
    data = json.dumps({"fields": dic})
    f, r = send_request(url, method.Put, headers, None, data)
    if lst[8]:
        f, r = issue_assign_sprint(issue,lst[8])
        if not f:
            return 'Problem occured while assigning the issue to target sprint: Issue {} successfully created but not assigned to {}!\r\n{}'.format(
                 issue, lst[8],r)
    return 'Edit Success'


# issue_edit([
#     'TEST-77', 'done', 'epic', 'a new y', 'ysg', 'lowest', '',
#     'try  one', 'ysg', 'test sprnit 1'
# ])


def issue_edit_labels(lst):
    issue = lst[0]
    mode = lst[1]
    labels = lst[2:]
    url, headers = prepare('issue', '/{}'.format(issue))
    target = []
    for l in labels:
        target.append({mode:l})
    data = json.dumps({"update":{"labels":target}})
    f, r = send_request(url, method.Put, headers, None, data)
    if not f:
        return False, 'Error occured while add labels\r\n{}'.format(r)
    print('label successfully {}ed'.format(mode))
    return True, 'label successfully {}ed'.format(mode)

# issue_edit_labels(['Test-77','remove', 'label1','label2','label3'])


def issue_delete(lst):
    msg = ''
    for issue in lst:
        msg += '{}\r\n'.format(issue_delete_helper(issue))
    msg += 'Done!'
    return msg


def issue_delete_helper(issue):
    url, headers = prepare('issue', '/{}'.format(issue))
    f, r = send_request(url, method.Delete, headers, None, None)
    if not f:
        return 'DOING {}\r\n{}'.format(issue, r)
    msg = '{} successfully deleted!'.format(issue)
    mylog.info(msg)
    return msg


def issue_assign(lst):
    issue = lst[0]
    assignee = lst[1]
    url, headers = prepare('issue', '/{}/assignee'.format(issue))
    data = '{"name":"' + assignee + '"}'

    f, r = send_request(url, method.Put, headers, None, data)
    if not f:
        return r
    msg = '{} successfully assigned to {}'.format(issue, assignee)
    mylog.info(msg)
    return msg


def issue_getComment(lst):
    issue = lst[0]
    url, headers = prepare('issue', '/{}{}'.format(issue, '/comment'))

    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return r

    comments = r.get('comments', [])
    if len(comments) > 0:
        string = 'Here are the comments for ' + issue + ':\r\n'
        for com in comments:
            string += '"{}"\r\n\twrote by {}\r\n\t{}\r\n\t(cid: {})\r\n'.format(
                com['body'], com['updateAuthor']['key'], com['created'],
                com['id'])
        mylog.info(string)
        print(string)
        return string
    else:
        mylog.info('get empty msg')
        return "There is no comment yet!"


def issue_addComment(lst):
    issue = lst[0]
    url, headers = prepare('issue', '/{}/{}'.format(issue, 'comment'))
    data = json.dumps({"body": lst[1]})
    # with open("res/comments.json", "r") as f:
    #     data = json.load(f)
    #     data = json.dumps(data)
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        return r
    mylog.info(r)
    print('Comment(ID: ' + r['id'] + ')added')
    return 'Comment(ID: ' + r['id'] + ')added'


def issue_delComment(lst):
    issue = lst[0]
    cid = lst[1]
    url, headers = prepare('issue', '/{}{}{}'.format(issue, '/comment/', cid))
    f, r = send_request(url, method.Delete, headers, None, None)
    if not f:
        return r
    mylog.info('Comment {} deleted'.format(cid))
    return 'Comment deleted'


# login(['admin','admin'])
# issue_create(['test', 'story','This is summaryyyyyyy', '', 'medium', '', 'This is Decriptionnnnnnn', 'ysg','test sprint 1'])
# issue_assign(['TEST-38','hang'])
# issue_assign(['TEST-29','hang'])
# finduser('xp zheng')
# finduser('yuhang4')
# issue_addComment(['Test-77','New added comments'])
# issue_delComment(['Test-77',10111])
# issue_getComment(['Test-77'])
# issue_assign(['Test-01','testuser1'])
# issue_transit(['TEST-72', 'Done'])
