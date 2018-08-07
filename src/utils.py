"""
usage:
from myLog import mylog

...
mylog.info('msg')
mylog.debug('msg')
mylog.error('msg')
...

"""
import json
import logging
import sys
from config import read_from_config
from os import F_OK, access, listdir, mkdir, remove
from time import localtime, strftime, strptime

from termcolor import cprint

log_directory = "log/"
if not access(log_directory, F_OK):
    mkdir(log_directory)
time_format = '%d(%b)%Y %H-%M-%S'
logformat = '%(asctime)s.%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d]\r\t%(message)s\r\n'
min_time = localtime()
logging.basicConfig(
    filename='{}{}.log'.format(log_directory, strftime(time_format, min_time)),
    format=logformat,
    datefmt=time_format)
log_list = listdir(log_directory)
if len(log_list) > 10:
    for s in listdir(log_directory):
        try:
            log_time = strptime(s, time_format + ".log")
            if log_time < min_time:
                min_time = log_time
        except ValueError as ve:
            remove(log_directory + s)
    remove('{}{}.log'.format(log_directory, strftime(time_format, min_time)))
mylog = logging.getLogger(__name__)
mylog.setLevel(logging.DEBUG)

func_enter_log_format = \
"""Entered method {}.{} with the following positional arguments:
\t\t{},
\tand the following keyword arguments:
\t\t{}"""

func_return_log_format = \
"""Exited method {}.{} with the following return value(s):
\t\t{}"""


def func_log(method):
    def log(*args, **kwargs):
        info = func_enter_log_format.format(method.__module__, method.__name__,
                                            args, kwargs)
        mylog.info(info)
        result = method(*args, **kwargs)
        info = func_return_log_format.format(method.__module__,
                                             method.__name__, result)
        mylog.info(info)
        return result

    return log


def overrides(interface_class):
    def overrider(method):
        assert (method.__name__ in dir(interface_class))
        return method

    return overrider


def asserts(expression, msg):
    try:
        assert expression, msg
    except AssertionError as err:
        mylog.error(err)
        return False
    return True


def write_memo_log(*args):
    info = "Program exited with the following attributes:\n"
    info_line = "\t{}:\n\t\t{}\n"
    for cls in args:
        for attr in dir(cls):
            value = getattr(cls, attr)
            if not callable(value) and not attr.startswith("__"):
                info += info_line.format("{}.{}".format(type(cls), attr),
                                         value)
    mylog.info(info)


class Super401(Exception):
    def __init__(self):
        self.err = 'Error Unauthorized. please login in again'
        Exception.__init__(self, self.err)


class glob():
    def __init__(self, dic):
        self.dic = dic
        self.set_value('jira', 'lnvusjira.lenovonet.lenovo.local')
        self.set_value('cookie_path', '')
        self.set_value('cookie', '')
        self.set_value('timeout', 10)

    def set_value(self, key, value):
        self.dic[key] = value

    def get_value(self, key, defValue=None):
        try:
            return self.dic[key]
        except KeyError:
            return defValue


def read_cookie():
    return read_from_config().get("credential").get("cookie")

def read_url():
    return read_from_config().get("domain")

def prepare(action, extend=None):
    if action != 'login':
        headers_book.get(action)['cookie'] = read_cookie()
    url = read_url() + address_book.get(action)
    if extend is not None:
        return (url + extend, headers_book.get(action))
    return (url, headers_book.get(action))


glob_dic = glob({})

# domain ='lnvusjira.lenovonet.lenovo.local'

address_book = {
    'login': '/rest/auth/1/session',
    'logout': '/rest/auth/1/session',
    'getProject': '/rest/api/2/project',
    'getBoard': '/rest/agile/1.0/board',
    'getStatus': '/rest/api/2/status',
    'getType': '/rest/api/2/project/type',
    'getIssuetype': '/rest/api/2/issuetype',
    'getAssignee': '/rest/api/2/user/search',
    'getPriority': '/rest/api/2/priority',
    'query': '/rest/api/2/search',
    'query_number': '/rest/agile/1.0/issue',
    'issue': '/rest/api/2/issue',
    'search': '/rest/api/2/user',
    'getVersion': '/rest/api/2/project',
    'getSprint': '/rest/agile/1.0/sprint',
    'assign_sprint': '/rest/agile/1.0/sprint',
    'createmeta': '/rest/api/2/issue/createmeta',
    'getField': '/rest/api/2/field',
    'getEstimation': '/rest/agile/1.0/issue',
    'mypermission': '/rest/api/2/mypermissions'
}

headers_book = {
    'getEstimation': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'createmeta': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': ''
    },
    'permission': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': ''
    },
    'mypermission': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': ''
    },
    'logout': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'getProject': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'getBoard': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'getStatus': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'getSprint': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'getType': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'getAssignee': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'getPriority': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'getIssuetype': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'query': {
        'Content-Type': 'application/json',
        'cookie': ''
    },
    'query_number': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'issue': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': ''
    },
    'search': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'getVersion': {
        'Accept': 'application/json',
        'cookie': ''
    },
    'assign_sprint': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': ''
    },
    'getField': {
        'Accept': 'application/json',
        'cookie': ''
    }
}


def print_err(msg: str, color: str) -> None:
    if sys.platform in ("win32", "cygwin"):
        import colorama
        colorama.init()
    cprint(msg, color=color, file=sys.stderr, end="")
    if sys.platform in ("win32", "cygwin"):
        import colorama
        colorama.deinit()

def exit_prog(code: int, verbose: bool) -> None:
    if verbose:
        print(
            "[Verbose]: Exiting Program with Exit Code: {}".format(code),
            end=""
        )
    sys.exit(code)