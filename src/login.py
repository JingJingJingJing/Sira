import requests
from threading import Thread
domain = '10.176.111.32:8080'
cookie_path = ''
return_val = 0
finish = 0
def stringtolist(s):
    return s.split(',')

def get_session_info(tup):
    t1 = tup[0].split('"')
    t2 = tup[1].split('"')
    return t1[5]+'='+ t2[3]

def send_request(url, data, headers):
    try:
        r = requests.post(url,headers=headers,data=data,timeout = 10)
        if(r.status_code == 200):
            s = stringtolist(r.text)
            cookie = get_session_info((s[0],s[1]))
            f = open(cookie_path+"cookie.txt","w")
            f.write(cookie)
            f.close
            print(r.text)
            global return_val
            return_val = 1
        else:
            print("Error Occured! Status Code:",r.status_code)
            print(r.text)
    except requests.exceptions.ConnectTimeout as err:
        print(err)
    global finish
    finish = 1
""" This function sign a user if un and pw are both correct
    Return 1 on success, 0 on failure """

def login(lst):
    un = lst[0]
    pw = lst[1]
    url = 'http://'+domain+'/rest/auth/1/session'
    data = '{"username":"'+str(un)+'","password":"'+str(pw)+'"}'
    headers = {'Content-Type':'application/json'}
    thread = Thread(target = send_request, args=(url, data, headers))
    thread.start()
    global finish
    while not finish:
        print("in while")
    return return_val
