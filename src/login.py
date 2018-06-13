import json
import logging

import requests

domain = '10.176.111.32:8080'
cookie_path = ''

logformat = '%(asctime)s,%(msecs)d %(levelname)-8s\r\n [%(filename)s:%(lineno)d] %(message)s\r\n'
logging.basicConfig(
    filename='user.log',
    format=logformat,
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.ERROR)


def login(lst):
    un = lst[0]
    pw = lst[1]
    url = 'http://' + domain + '/rest/auth/1/session'
    data = '{"username":"' + str(un) + '","password":"' + str(pw) + '"}'
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post(url, headers=headers, data=data, timeout=3)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(err)
            return (
                False,
                "Login failed! Please make sure that your username and password are correct!"
            )
        j = r.json()
        try:
            cookie = j['session']['name'] + '=' + j['session']['value']
        except KeyError:
            logging.error('No session information from HTTP response\r\n' +
                          r.text)
            return (False, 'session info not found!')
        f = open(cookie_path + "cookie.txt", "w")
        f.write(cookie)
        f.close
        return (True, "Success")
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return (False, 'Login failed due to an internet error!')


def logout():
    f = open(cookie_path + "cookie.txt", "w")
    f.write('')
    f.close
    logging.info("Successfully logged out")
