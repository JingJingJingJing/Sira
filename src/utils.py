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
        
    def set_value(self,key,value):
        self.dic[key] = value

    def get_value(self,key,defValue=None):
        try:
            return self.dic[key]
        except KeyError:
            return defValue

glob_dic = glob({})