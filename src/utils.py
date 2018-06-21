"""
usage:
from myLog import mylog

...
mylog.info('msg')
mylog.debug('msg')
mylog.error('msg')
...

"""
import logging

import inspect

import json


def read_cookie():
    if glob_dic.get_value('cookie') == '' or glob_dic.get_value('cookie') is None:
        try:
            with open(glob_dic.get_value('cookie_path') + "cookie.txt", "r") as f:
                glob_dic.set_value('cookie',f.read())
                f.close()
        except FileNotFoundError as err:
            mylog.error(err)
            raise Super401
    return glob_dic.get_value('cookie')
        




logformat = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d]\r\n%(message)s\r\n'
logging.basicConfig(
    filename='user.log', format=logformat, datefmt='%d-%m-%Y:%H:%M:%S')

mylog = logging.getLogger(__name__)
mylog.setLevel(logging.DEBUG)


def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider

def asserts(expression, msg):
    try:
        assert expression, msg
    except AssertionError as err:
        mylog.error(err)
        return False
    return True


class Super401(Exception):
    def __init__(self):
        err = 'Error Unauthorized. please login in again'
        Exception.__init__(self, err)

class glob():
    def __init__(self,dic):
        self.dic = dic
        self.set_value('domain', '10.176.111.32:8080')
        self.set_value('cookie_path', '')
        self.set_value('cookie', '')
        self.set_value('timeout', 5)
        self.set_value('jql_default_tail','","startAt":0, "maxResults": 100,"fields":["summary","issuetype","project","fixVersions","assignee","status"]}')
        self.tips = tips({'project':[],'issuetype':[],'type':[],'sprint':[],'board':[]})

    def set_value(self,key,value):
        self.dic[key] = value

    def get_value(self,key,defValue=None):
        try:
            return self.dic[key]
        except KeyError:
            return defValue


class tips(dict):
    def __init__(self,dic):
        self.dic = dic
    def set_value(self,key,value):
        self.dic[key] = value
    def get_value(self,key,defValue=None):
        try:
            return self.dic[key]
        except KeyError:
            return defValue


glob_dic = glob({})
issue_create_args = dict()


def prepare(s):
    address_book = {
        'login':'http://' + glob_dic.get_value('domain') + '/rest/auth/1/session',
        'logout':'http://' + glob_dic.get_value('domain') + '/rest/auth/1/session',
        'getProject':'http://' + glob_dic.get_value('domain') + '/rest/api/2/project',
        'getBoard':'http://' + glob_dic.get_value('domain') + '/rest/agile/1.0/board',
        'getStatus':'http://' + glob_dic.get_value('domain') + '/rest/api/2/status',
        'getType':'http://' + glob_dic.get_value('domain') + '/rest/api/2/project/type',
        'getIssuetype':'http://' + glob_dic.get_value('domain') + '/rest/api/2/issuetype',
        'query':'http://' + glob_dic.get_value('domain') + '/rest/api/2/search',
        'query_number':'http://' + glob_dic.get_value('domain') + '/rest/api/2/issue/',
        'issue':'http://' + glob_dic.get_value('domain') + '/rest/api/2/issue',
        'search':'http://' + glob_dic.get_value('domain') + '/rest/api/2/user'
    }
    headers_book = {
        'login':{'Content-Type': 'application/json'},
        'logout':{'Accept': 'application/json', 'cookie':read_cookie()},
        'getProject':{'Accept': 'application/json', 'cookie':read_cookie()},
        'getBoard':{'Accept': 'application/json', 'cookie':read_cookie()},
        'getStatus':{'Accept': 'application/json', 'cookie':read_cookie()},
        'getSprint':{'Accept': 'application/json', 'cookie':read_cookie()},
        'getType':{'Accept': 'application/json', 'cookie':read_cookie()},
        'getIssuetype':{'Accept': 'application/json', 'cookie':read_cookie()},
        'query':{'Content-Type': 'application/json', 'cookie':read_cookie()},
        'query_number':{'Content-Type': 'application/json', 'cookie':read_cookie()},
        'issue':{
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'cookie':read_cookie()
            },
        'search':{'Accept': 'application/json','cookie':read_cookie()}
    }
    return (address_book.get(s), headers_book.get(s))