import requests
from threading import Thread
domain = '10.176.111.32:8080'
cookie_path = ''

def stringtolist(s):
    return s.split(',')

def get_session_info(tup):
    t1 = tup[0].split('"')
    t2 = tup[1].split('"')
    return t1[5]+'='+ t2[3]

def login(lst):
    un = lst[0]
    pw = lst[1]
    url = 'http://'+domain+'/rest/auth/1/session'
    data = '{"username":"'+str(un)+'","password":"'+str(pw)+'"}'
    headers = {'Content-Type':'application/json'}
    try:
        r = requests.post(url,headers=headers,data=data,timeout = 3)
        if(r.status_code == 200):
            s = stringtolist(r.text)
            cookie = get_session_info((s[0],s[1]))
            f = open(cookie_path+"cookie.txt","w")
            f.write(cookie)
            f.close
            print("success")
        return r.text
    except requests.exceptions.RequestException as err:
        print(err)
        return err
login(["admin","admin"])