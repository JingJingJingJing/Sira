import requests
from query import method, read_cookie
import logging
domain = '10.176.111.32:8080'
cookie_path = ''
def create_issue():
    cookie = ''
    try:
        cookie = read_cookie()
    except FileNotFoundError as err:
        logging.error(err)
        return (False, "Please log in first")
    url = 'http://' + domain + '/rest/api/issue'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'cookie': cookie
        }

    pass