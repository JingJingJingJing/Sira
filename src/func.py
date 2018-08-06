import json
from enum import Enum
from os import F_OK, access, mkdir
from threading import Thread
import requests

from utils import Super401, glob_dic, mylog, prepare, func_log
''' ************ login logout ************* '''


def login(lst):
    un = lst[0]
    pw = lst[1]
    url = prepare('login')[0]
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"username": un, "password": pw})
    try:
        requests.urllib3.disable_warnings()
        r = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=glob_dic.get_value('timeout'),
            verify=False)
        mylog.error(r.text)
        if r.status_code == 401:
            mylog.error("401 Unauthorized")
            return False, [
                '401 Unauthorized!',
                'Please make sure the username and password are correct'
            ]
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
            return (False, [
                'Login failed! Please make sure that your username and password are correct!'
            ])
        j = r.json()
        try:
            cookie = j['session']['name'] + '=' + j['session']['value']
            glob_dic.set_value(
                'cookie', j['session']['name'] + '=' + j['session']['value'])
        except KeyError:
            mylog.error('No session information from HTTP response\r\n' +
                        r.text)
            return (False, ['session info not found!'])
        write_to_config(["credential"], ["cookie", "username"], [cookie, un])
        mylog.info("Successfully logged in as " + un)
        return (True, ["Success"])
    except requests.exceptions.RequestException as err:
        return (False, ['Login failed due to an internet error!'])


def logout():
    url, headers = prepare('logout')
    try:
        r = requests.delete(url, headers=headers, timeout=5)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            pass
    except requests.exceptions.RequestException:
        pass
    # f = open(glob_dic.get_value('cookie_path') + "cookie.txt", "w")
    # f.write('')
    # f.close
    # glob_dic.set_value('cookie', '')
    # mylog.info('Successfully logged out')
    return (True, ['Successfully logged out'])


''' ************** All requests are sent through this function except login logout ************** '''


class method(Enum):
    Get = 0
    Post = 1
    Put = 2
    Delete = 3


def send_request(url, method, headers, params, data):
    r = requests.Response()
    try:
        if method is method.Get:
            r = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=glob_dic.get_value('timeout'),
                verify=False)
        elif method is method.Put:
            r = requests.put(
                url,
                headers=headers,
                data=data,
                timeout=glob_dic.get_value('timeout'),
                verify=False)
        elif method is method.Delete:
            r = requests.delete(
                url,
                headers=headers,
                data=data,
                timeout=glob_dic.get_value('timeout'),
                verify=False)
        elif method is method.Post:
            r = requests.post(
                url,
                headers=headers,
                data=data,
                timeout=glob_dic.get_value('timeout'),
                verify=False)
        else:
            mylog.error('Wrong method that not suppord:' + str(method))
            return (False, 'Unknown internal error occured')
        if r.status_code == 401:
            mylog.error("401 Unauthorized")
            return (False, "401 Unauthorized")
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            mylog.error(r.text)

            s = 'Request denied!\r\nerror code: {} {}\r\n'.format(
                str(r.status_code),
                str(requests.status_codes._codes[r.status_code][0]))

            try:
                lst = r.json().get('errorMessages', [])
                for i, errors in enumerate(lst):
                    s += errors
                    if i != len(lst) - 1:
                        s += '\r\n'
                dic = r.json().get('errors', {})
                for i, key in enumerate(dic):
                    s += dic[key] + ' '

            except json.JSONDecodeError:
                pass
            s += "Please Try Again"
            return False, s
        mylog.info(r)
        try:
            try:
                s = ''
                lst = r.json()['warningMessages']
                for i, errors in enumerate(lst):
                    s += errors
                    if s != len(lst):
                        s += '\r\n'
                mylog.error(s)
                return (False, s)
            except KeyError:
                return (True, r.json())
            except TypeError:
                return (True, r.json())
        except json.JSONDecodeError:
            return (True, r)
    except requests.exceptions.RequestException as err:
        mylog.error(err)
        return (False, '''Internet Error! Try:\r\n
            \tChecking the network cables, modem, and route\r\n
            \tReconnecting to Wi-Fi\r\n
            \tRunning Network Diagnostics''')


''' ************** Queries ************** '''

def getTarget(fields, field):
    '''
    This function only works for identifier "name" or "key"
    fields: dict()
    field: str() (identifiers)
    '''
    ret = ''
    try:
        ret = fields.get(field)['name']
    except KeyError:
        try:
            ret = fields.get(field)['key']
        except KeyError:
            ret = fields.get(field)
    except TypeError:
        try:
            ret = str(fields.get(field)[0].get('name'))
        except IndexError:
            ret = str(fields.get(field))
        except TypeError:
            pass
        except AttributeError:
            ret = fields.get(field)
    if ret != '':
        if (' ' in ret) or isinstance(ret, list):
            ret = '"{}"'.format(str(ret))
        return ret
    else:
        return 'N/A'


def getResponse(lst):
    '''
    This function used to get target field information from a list of issues
    Only information of the fields in defaultList will be returned
    '''
    try:
        defaultList = json.loads(
            read_from_config()).get('query_field').get('issue_default')
    except AttributeError:
        defaultList = [
            "assignee", "reporter", "priority", "status", "labels",
            "fixVersions", "summary"
        ]
    if not lst:
        return 'Issue Not Found'
    s = ''
    for i, issue in enumerate(lst):
        s += str(issue.get('key')) + ' '
        fields = issue.get('fields')
        for j, field in enumerate(defaultList):
            s += str(getTarget(fields, field)) + ' '
            if (i != len(lst) - 1) and (j == len(defaultList) - 1):
                s += '\r\n'
    return s


@func_log
def query_issue(constraint, board=0, limit=0, order=None, verbose=None, **kwargs):
    if verbose is None:
        verbose = json.loads(read_from_config()).get("verbose")
        verbose = verbose.lower()=="true"
    print_v("Formating Input ...", verbose)
    if order:
        order = order.lower()
        if order == 'asc':
            constraint += ' order by key ASC'
        elif order == 'desc':
            constraint += ' order by key DESC'
    else:
        constraint += ' order by updated DESC'
    data = {}
    data["jql"] = constraint
    data["startAt"] = 0

    if limit:
        data["maxResults"] = limit
    print_v("Sending the Request ...", verbose)

    if board:
        url, headers = prepare('getBoard','/{}/issue'.format(board))
        f, r = send_request(url, method.Get, headers, data, None)
    else:
        url, headers = prepare('query')
        f, r = send_request(url, method.Post, headers, None, json.dumps(data))
    if not f:
        print_v("Request Failed !!!", verbose)
        return False, r
    print_v("Extracting the Results ...", verbose)
    return True, getResponse(r.get('issues'))


def getInfo(r, order):
    '''
    This function used to get target field information from a list of projects
    Only information of the fields in defaultList will be returned
    '''
    lst = []
    defaultList = ['name', 'key', 'lead']
    for i, pro in enumerate(r):
        s = ''
        key = pro.get('key')
        for j, f in enumerate(defaultList):
            s += getTarget(pro, f)
            if j != len(defaultList) - 1:
                s += ' '
        if i != len(r) - 1:
            s += '\r\n'
        lst.append((key, s))
    if order and order.lower() == 'asc':
        lst.sort()
    elif order and order.lower == 'desc':
        lst.sort(reverse=True)
    s = ''
    for tup in lst:
        s += tup[1]
    return s


@func_log
def query_project(limit=0, order=None, verbose=None, **kwargs):
    if verbose is None:
        verbose = json.loads(read_from_config()).get("verbose")
        verbose = verbose.lower()=="true"
    if order:
        order = order.lower()
    param = {}
    print_v("Formating Input ...", verbose)
    if order == 'recent':
        if limit:
            param["recent"] = limit
        else:
            param["recent"] = 20
    param["expand"] = "lead"
    print_v("Sending the Request ...", verbose)
    url, headers = prepare('getProject')
    f, r = send_request(url, method.Get, headers, param, None)

    if not f:
        print_v("Request Failed !!!", verbose)
        return False, r
    print_v("Extracting the Results ...", verbose)
    return True, getInfo(r, order)


@func_log
def query_board(key=None, limit=None, order=None, verbose=None, **kwargs):
    '''
    This function return all boards and order the return value.
    The return value is a string of board id adn board name
    If key is specified and valid, only one line will be returned
    '''
    if verbose is None:
        verbose = json.loads(read_from_config()).get("verbose")
        verbose = verbose.lower()=="true"
    print_v("Formating Input ...", verbose)
    url, headers = prepare('getBoard')
    print_v("Sending the Request ...", verbose)
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        print_v("Request Failed !!!", verbose)
        return False, r
    print_v("Extracting the Results ...", verbose)
    lst = []
    defaultList = ['id', 'name']
    for info in r.get('values'):
        bid = info.get('id')
        innerlst = []
        for f in defaultList:
            innerlst.append(info.get(f))
        lst.append(tuple(innerlst))
        if key and (bid == key):
            tup = lst.pop()
            return True, '{} "{}"'.format(tup[0], tup[1])
    if key:
        return False, 'Not found or you don\'t have permission to view this board.'
    if order and order.lower() == 'asc':
        lst.sort()
    elif order and order.lower() == 'desc':
        lst.sort(reverse=True)
    s = ''
    for i, tup in enumerate(lst):
        s += '{} "{}"'.format(tup[0], tup[1])
        if i != len(lst) - 1:
            s += '\r\n'
    return True, s


''' ******************* Update ******************* '''


def issue_update_assignee(issue, info):
    url, headers = prepare('issue', '/{}'.format(issue))
    data = {"fields": {"assignee": {"name": info}}}
    f, r = send_request(url, method.Put, headers, None, json.dumps(data))
    if not f:
        return False, r
    return True, 'success'


def issue_update_status(issue, info):
    status = info.title()
    url, headers = prepare(
        'issue', '/{}/transitions?expand=transitions.fields'.format(issue))
    data = {}
    dic = {}

    def issue_get_tansition(issue, dic):
        url, headers = prepare('issue', '/{}/transitions'.format(issue))
        f, r = send_request(url, method.Get, headers, None, None)
        if not f:
            return None
        for msg in r.get('transitions'):
            dic[msg.get('name')] = msg.get('id')
        return dic

    if not issue_get_tansition(issue, dic):
        return False, 'no transit is avaiable'
    transition = {"id": dic.get(status)}
    data = json.dumps({"transition": transition})
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        return r
    return True, 'success'


def issue_update_labels(issue, labels, mode='add'):
    url, headers = prepare('issue', '/{}'.format(issue))
    target = []
    if isinstance(labels, str):
        target = [{mode: labels}]
    else:
        for l in labels:
            target.append({mode: l})
    data = json.dumps({"update": {"labels": target}})
    f, r = send_request(url, method.Put, headers, None, data)
    if not f:
        return False, str(r)

    return True, 'label successfully {}ed'.format(mode)


def issue_get_comment(issue):
    url, headers = prepare('issue', '/{}{}'.format(issue, '/comment'))

    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return False, str(r)

    comments = r.get('comments', [])
    if len(comments) > 0:
        string = 'Here are the comments for ' + issue + ':\r\n'
        for com in comments:
            string += '"{}"\r\n\twrote by {}\r\n\t{}\r\n\t(cid: {})\r\n'.format(
                com['body'], com['updateAuthor']['key'], com['created'],
                com['id'])
        return True, string
    else:
        return True, "There is no comment yet!"


def issue_edit_comment(issue, cid, body):
    url, headers = prepare('issue', '/{}{}{}'.format(issue, '/comment/', cid))
    data = {"body": body}
    f, r = send_request(url, method.Put, headers, None, data)
    if not f:
        return r
    return True, 'Comment(ID: ' + r['id'] + ') modified'


def issue_add_comment(issue, body):
    url, headers = prepare('issue', '/{}/{}'.format(issue, 'comment'))
    data = json.dumps({"body": body})
    f, r = send_request(url, method.Post, headers, None, data)
    if not f:
        return False, r
    return True, 'Comment(ID: ' + r['id'] + ') added'


def issue_del_comment(issue, cid):
    url, headers = prepare('issue', '/{}{}{}'.format(issue, '/comment/', cid))
    f, r = send_request(url, method.Delete, headers, None, None)
    if not f:
        return False, r
    return True, 'Comment deleted'


def issue_watch(issue, user=None):
    url, headers = prepare('issue', '/{}/watchers'.format(issue))
    if user is None:
        user = json.loads(read_from_config()).get('credential').get('username')
    print(url, headers)
    return send_request(url, method.Post, headers, None, '"{}"'.format(user))


def issue_get_watcher(issue):
    url, headers = prepare('issue', '/{}/watchers'.format(issue))
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return r
    lst = r.get('watchers')
    s = ''
    for i, user in enumerate(lst):
        s += user.get('name')
        if i != len(lst) - 1:
            s += '\r\n'
    return s


def issue_del_watcher(issue, user):
    url, headers = prepare('issue', '/{}/watchers'.format(issue))
    return send_request(url, method.Delete, headers, '"ysg"', None)


def write_to_config(dic_path, field, info):

    fh = open('.sirarc', 'r')
    content = fh.read()
    if content:
        data = json.loads(content)
    else:
        data = {}
    dic = data
    for x in dic_path:
        dic = dic[x]
    if isinstance(field, list):

        for i in range(len(field)):
            if isinstance(info, list):
                if len(field) != len(info):
                    fh.close()
                    raise "Field and Info length need to be equal"
                dic[field[i]] = info[i]
            else:
                dic[field[i]] = info
    else:
        dic[field] = info
    fh = open('.sirarc', 'w')
    ret = json.dumps(data)
    fh.write(ret)
    fh.close()
    return ret


def read_from_config():
    try:
        fh = open('.sirarc', 'r')
        content = fh.read()
        fh.close()
        return content
    except FileNotFoundError:
        fh = open('.sirarc', 'w')
        fh.write('')
        fh.close()


def getPermission():
    url, headers = prepare('mypermission')
    f, r = send_request(url, method.Get, headers, None, None)
    if not f:
        return r
    for permission in r.get('permissions'):
        write_to_config(['permissions'], permission, True)


def print_v(s, f=False):
    if f:
        print(s)


if __name__ == '__main__':
    # login(['admin','admin'])
    # print(query_issue('assignee=ysg')[1])
    # print(query_project())
    # print(query_board())
    # print(query_board(key=4))
    # print(update_status('test-88','to do'))
    # print(read_from_config())
    # test = 'test-88'
    # print(issue_watch(test)[1])
    # print(issue_get_watcher(test))
    # print(issue_del_watcher(test, 'ysg')[1])
    # print(issue_get_watcher(test))

    pass