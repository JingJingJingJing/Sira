import logging
import requests

domain = '10.176.111.32:8080'
cookie_path = ''

logformat = '%(asctime)s,%(msecs)d %(levelname)-8s\r\n [%(filename)s:%(lineno)d] %(message)s\r\n'
logging.basicConfig(
    filename='user.log',
    format=logformat,
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.INFO)


def login(lst):
    un = lst[0]
    pw = lst[1]
    url = 'http://'+domain+'/rest/auth/1/session'
    data = '{"username":"'+str(un)+'","password":"'+str(pw)+'"}'
    headers = {'Content-Type':'application/json'}
    flag,r = send_request(url, method.Post, headers, None, data)
    if not flag:
        return (False,r)
    j = json.loads(r.text)
    try:
        cookie = j['session']['name'] + '=' + j['session']['value']
    except KeyError:
        return (False, 'session info not found!')
    f = open(cookie_path+"cookie.txt","w")
    f.write(cookie)
    f.close
    return(True, "Success")


def logout():
    f = open(cookie_path + "cookie.txt", "w")
    f.write('')
    f.close
    logging.info("Successfully logged out")
login(['admin','admin'])
