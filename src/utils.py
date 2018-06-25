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
from os import listdir, remove, access, F_OK, mkdir
from time import localtime, strftime, strptime


def read_cookie():
    if glob_dic.get_value('cookie', '') == '':
        try:
            with open(glob_dic.get_value('cookie_path') + "cookie.txt",
                      "r") as f:
                glob_dic.set_value('cookie', f.read())
                f.close()
        except FileNotFoundError as err:
            mylog.error(err)
            raise Super401
    return glob_dic.get_value('cookie')
        
log_directory = "log/"
if not access(log_directory, F_OK):
    mkdir(log_directory)
time_format = '%H-%M-%S %d(%b)%Y'
logformat = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d]\r%(message)s\r\n'
min_time = localtime()
logging.basicConfig(
    filename='{}{}.log'.format(log_directory,
                               strftime(time_format, min_time)),
    format=logformat,
    datefmt=time_format
)
log_list = listdir(log_directory)
if len(log_list) > 10:
    for s in listdir(log_directory):
        try:
            log_time = strptime(s, time_format + ".log")
            if log_time < min_time:
                min_time = log_time
        except ValueError as ve:
            remove(log_directory + s)
    remove('{}{}.log'.format(log_directory,
                                strftime(time_format, min_time)))
mylog = logging.getLogger(__name__)
mylog.setLevel(logging.DEBUG)

func_enter_log_format = \
"""\tEntered method {}.{} with the following positional arguments:
\t\t{},
\tand the following keyword arguments:
\t\t{}"""

func_return_log_format = \
"""\tExited method {}.{} with the following return value(s):
\t\t{}"""

def func_log(method):
    def log(*args, **kwargs):
        info = func_enter_log_format.format(method.__module__,
                                            method.__name__,
                                            args,
                                            kwargs)
        mylog.info(info)
        result = method(*args, **kwargs)
        info = func_return_log_format.format(method.__module__,
                                            method.__name__,
                                            result)
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
    info = "Program exited with the following attributes:"
    info_line = "{}:\n\t\t{}\n"
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
        self.set_value('domain', '10.176.111.32:8080')
        self.set_value('jira', 'lnvusjira.lenovonet.lenovo.local')
        self.set_value('cookie_path', '')
        self.set_value('cookie', '')
        self.set_value('timeout', 5)
        self.set_value('protocol', 'http://')
        self.tips = tips({})

    def set_value(self, key, value):
        self.dic[key] = value

    def get_value(self, key, defValue=None):
        try:
            return self.dic[key]
        except KeyError:
            return defValue


class tips():
    def __init__(self, dic):
        self.dic = dic

    def set_value(self, key, value):
        self.dic[key] = [[0.5, x] for x in value]

    def get_value(self, key, defValue=None):
        try:
            return [x[1] for x in self.dic[key]]
        except KeyError:
            return defValue

    def update_priority(self, section, key):
        tgt_list = self.dic[section]
        index = -1
        for i in range(len(tgt_list)):
            if tgt_list[i][1] == key:
                tgt_list[i][0] *= 1.05
                index = i
            else:
                tgt_list[i][0] *= 0.95
        if index == -1:
            raise KeyError
        element = tgt_list.pop(index)
        start_index = 0
        last_index = index
        while start_index < last_index:
            mid_index = int((start_index + last_index) / 2)
            if element[0] > tgt_list[mid_index][0]:
                last_index = mid_index
            elif element[0] < tgt_list[mid_index][0]:
                start_index = mid_index + 1
            else:
                start_index = mid_index
                break
        tgt_list.insert(start_index, element)

    def write_file(self, file_name):
        f = open(file_name, 'w+')
        f.write(json.dumps(self.dic))
        f.close()
    
    def add_new_key(self, section, key):
        tgt_list = self.dic[section]
        tgt_list.insert(1, [tgt_list[1][0], key])

glob_dic = glob({})
domain = glob_dic.get_value('domain')
protocol = glob_dic.get_value('protocol')
address_book = {
    'logout': protocol + domain + '/rest/auth/1/session',
    'getProject': protocol + domain + '/rest/api/2/project',
    'getBoard': protocol + domain + '/rest/agile/1.0/board',
    'getStatus': protocol + domain + '/rest/api/2/status',
    'getType': protocol + domain + '/rest/api/2/project/type',
    'getIssuetype': protocol + domain + '/rest/api/2/issuetype',
    'getAssignee': protocol + domain + '/rest/api/2/user/search?username=.',
    'getPriority': protocol + domain + '/rest/api/2/priority',
    'query': protocol + domain + '/rest/api/2/search',
    'query_number': protocol + domain + '/rest/api/2/issue',
    'issue': protocol + domain + '/rest/api/2/issue',
    'search': protocol + domain + '/rest/api/2/user',
    'getVersion': protocol + domain + '/rest/api/2/project',
    'getSprint':protocol + domain + '/rest/agile/1.0/sprint',
    'assign_sprint': protocol + domain + '/rest/agile/1.0/sprint'
}

headers_book = {
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
        'Content-Type': 'application/json',
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
    }
}


def prepare(s, extend=None):
    headers_book.get(s)['cookie'] = read_cookie()
    if extend is not None:
        return (address_book.get(s) + extend, headers_book.get(s))
    return (address_book.get(s), headers_book.get(s))
