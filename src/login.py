import requests
domain = '10.176.111.32:8080'
cookie_path = ''

def stringtolist(s):
    return s.split(',')

def get_session_info(tup):
    t1 = tup[0].split('"')
    t2 = tup[1].split('"')
    return t1[5]+'='+ t2[3]

def read_cookie():
    cookie = ''
    with open(cookie_path+"cookie.txt","r") as f:
        cookie = f.read()
    return cookie

""" This function sign a user if un and pw are both correct
    Return 1 on success, 0 on failure """

def login(lst):
    print(lst)
    un = lst[0]
    pw = lst[1]
    url = 'http://'+domain+'/rest/auth/1/session'
    data = '{"username":"'+str(un)+'","password":"'+str(pw)+'"}'
    headers = {'Content-Type':'application/json'}
    r = requests.post(url,headers=headers,data=data)
    if(r.status_code == 200):
        s = stringtolist(r.text)
        cookie = get_session_info((s[0],s[1]))
        f = open(cookie_path+"cookie.txt","w")
        f.write(cookie)
        f.close
        print(r.text)
        return 1
    print("Error Occured! Status Code:",r.status_code)
    print(r.text)
    return 0
