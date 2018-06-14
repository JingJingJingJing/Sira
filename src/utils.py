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
mylog.setLevel(logging.INFO)

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