'''
usage:
from myLog import mylog

...
mylog.info('msg')
mylog.debug('msg')
mylog.error('msg')
...

'''
import logging

logformat = '%(asctime)s,%(msecs)d %(levelname)-8s\r\n [%(filename)s:%(lineno)d] %(message)s\r\n'
logging.basicConfig(
    filename='user.log', format=logformat, datefmt='%d-%m-%Y:%H:%M:%S')

mylog = logging.getLogger(__name__)
mylog.setLevel(logging.ERROR)
