import json
from os import F_OK, access, mkdir
from threading import Thread

import requests

from query import method, send_request
from utils import Super401, glob_dic, mylog, prepare

''' lst = ['username','password'] '''


def login(lst):
    un = lst[0]
    pw = lst[1]
    url = prepare('logout')[0]
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"username": un, "password": pw})
    try:
        r = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=glob_dic.get_value('timeout'),
            verify=False)
        mylog.error(r.text)
        if r.status_code == 401:
            mylog.error("401 Unauthorized")
            raise Super401
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            mylog.error(err)
            try:
                errmsg = r.json()['errorMessages'][0]
                mylog.error(errmsg)
            except KeyError:
                pass
            except json.decoder.JSONDecodeError:
                pass
            return (
                False,
                ['Login failed! Please make sure that your username and password are correct!']
            )
        j = r.json()
        try:
            glob_dic.set_value(
                'cookie', j['session']['name'] + '=' + j['session']['value'])
        except KeyError:
            mylog.error('No session information from HTTP response\r\n' +
                        r.text)
            return (False, ['session info not found!'])
        f = open(glob_dic.get_value('cookie_path') + "cookie.txt", "w")
        f.write(glob_dic.get_value('cookie'))
        f.close()
        mylog.info("Successfully logged in as " + un)
        thr = Thread(target=download, args=(None, un))
        thr.start()
        return (True, ["Success"])
    except requests.exceptions.RequestException as err:
        mylog.error(err)
        return (False, ['Login failed due to an internet error!'])


def logout():
    url, headers = prepare('logout')
    try:
        r = requests.delete(url, headers = headers, timeout=5)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            pass
    except requests.exceptions.RequestException:
        pass
    f = open(glob_dic.get_value('cookie_path') + "cookie.txt", "w")
    f.write('')
    f.close
    glob_dic.set_value('cookie', '')
    mylog.info('Successfully logged out')
    return (True, ['Successfully logged out'])


def goInto(lst, key, field):
    if not lst:
        glob_dic.tips.set_value(key, [lst])
        return True
    target = []
    for element in lst:
        tmp = element.get(field, '')
        if (tmp is not '') and (tmp not in target):
            target.append(tmp)
    if target:
        glob_dic.tips.set_value(key, target)
        return True
    return False


# def getProject():
#     url, headers = prepare('getProject')
#     f, r = send_request(url, method.Get, headers, None, None)
#     if f:
#         return goInto(r, 'project', 'key')

def getProject():
    url, headers = prepare('createmeta')
    f, r = send_request(url, method.Get, headers, None, None)
    if f:
        return goInto(r.get('projects'), 'project', 'key')
    return False

def getBoard():
    url, headers = prepare('getBoard')
    f, r = send_request(url, method.Get, headers, None, None)
    if f:
        return goInto(r.get('values'), 'board', 'id')
    return False
def assignment(sname, sid, lst):
    for issue in lst:
        glob_dic.tips.get_value('issue')[0][issue.get('name').upper()] = sname

def getAll(sname, sid):
    

    url,headers = prepare('assign_sprint','/{}/issue'.format(sid))
    
    f,r = send_request(url, method.Get, headers, None, None)
    
    if f:
        for issue in r.get('issues'):
            glob_dic.tips.get_value('issues')[0][issue.get('key').upper()] = sname
            
    

# getAll('','')
def thread_download(url,headers,lst,sprint=False):
    f, r = send_request(url, method.Get, headers, None, None)
    if f:
        mlst = r.get('values')
        lst += mlst
        if sprint:
            thr = Thread()
            thr_lst = []
            for msg in mlst:
                
                spName = msg.get('name')
                spId = msg.get('id')
                glob_dic.tips.get_value('sid')[0][spName.lower()] = spId

                thr = Thread(target=getAll, args=(spName,spId))
                thr_lst.append(thr)
                thr.start()

            for t in thr_lst:
                t.join()




def getBoardRelated():
    if not getBoard():
        return False
    thrSprint = Thread()
    thrVersion = Thread()
    lstVersion = []
    lstSprint = []
    glob_dic.tips.set_value('sid', [{}])
    glob_dic.tips.set_value('issues', [{}])
    thr_s = []
    thr_v = []
    for boardid in glob_dic.tips.get_value('board'):
        url, headers = prepare('getBoard','/{}/sprint'.format(str(boardid)))
        thrSprint = Thread(target = thread_download, args = (url,headers,lstSprint,True))
        thr_s.append(thrSprint)
        thrSprint.start()
        url, headers = prepare('getBoard','/{}/version'.format(str(boardid)))
        thrVersion = Thread(target = thread_download, args = (url,headers,lstVersion))
        thr_v.append(thrVersion)
        thrVersion.start()
    for t in thr_s:
        t.join()
    
    if lstSprint:
        if not goInto(lstSprint, 'sprint', 'name'):
            return False
    for t in thr_v:
        t.join()
    if not goInto(lstVersion, 'versions', 'name'):
        return False

    return True

# getBoardRelated()
# print(glob_dic.tips.get_value('issues'))
def getStatus():
    url, headers = prepare('getStatus')
    f, r = send_request(url, method.Get, headers, None, None)
    if f:
        return goInto(r, 'status', 'name')


def getType():
    url, headers = prepare('getType')
    f, r = send_request(url, method.Get, headers, None, None)
    if f:
        return goInto(r, 'type', 'key')


def getIssuetype():
    url, headers = prepare('getIssuetype')
    f, r = send_request(url, method.Get, headers, None, None)
    if f:
        return goInto(r, 'issuetype', 'name')


def getUserHelper(lst, url, headers, i):
    param = {'username':'.','maxResults':100,'startAt':i}
    f, r = send_request(url, method.Get, headers, param, None)
    if f:
        lst += r

def getAssignee():
    url, headers = prepare('getAssignee')
    lst=[]
    thr = Thread()
    thr_lst = []
    for i in range(0,10000,100):
        url, headers = prepare('getAssignee')
        thr = Thread(target=getUserHelper, args=(lst,url,headers,i))
        thr_lst.append((thr))
        thr.start()
    for t in thr_lst:
        t.join()
    if goInto(lst, 'assignee', 'key'):
        return goInto(lst, 'reporter', 'key')
    else: 
        return False


def getPriority():
    url, headers = prepare('getPriority')
    f, r = send_request(url, method.Get, headers, None, None)
    if f:
        return goInto(r, 'priority', 'name')


def getVersion():
    getProject()
    lst = []
    for i, p in enumerate(glob_dic.tips.get_value('project')):
        print('Iteration %d' % i)
        url, headers = prepare('getVersion','/{}/versions'.format(p))
        
        f, r = send_request(url, method.Get, headers, None, None)
        if not f:
            return False
        lst += r
    return goInto(lst, 'versions', 'name')

# def ultimate_request(url, headers, i, sname, lst):
#     param = {'startAt':i, 'maxResults':100}
#     f, r = send_request(url, method.Get, headers, param, None)
#     if f:
#         lst += r
# def ultimateGetIssues():
#     id_book = glob_dic.tips.get_value('sid')[0]

#     thr = Thread()
#     thr_lst = []
#     lst = []
#     for sid in id_book:
#         sname = id_book.get(sid)
#         url, headers = prepare('getBoard','/sprint/{}/issue'.format(str(sid)))
#         for i in range(0, 3500, 10):
#             thr = Thread(target=ultimate_request, args=(url,headers,i,sname,lst))
#             thr_lst.append(thr)
#             thr.start()
#     for t in thr_lst:
#         t.join()
#     print('Do I return?')
    
#     return goInto(lst, 'issues', 'key')
        
        # sname = glob_dic.tips.get_value('sid')[]
        # url, headers = prepare('getBoard','/sprint/{}/issue'.format(str(sid)))

def download(dummy, un):
    print('Downloading Sprint...')
    thrb = Thread(target=getBoardRelated,args=())
    print('Downloading Project...')
    thrpro = Thread(target=getProject,args=())
    print('Downloading Issuetype...')
    thri = Thread(target=getIssuetype,args=())
    print('Downloading Status...')
    thrs = Thread(target=getStatus,args=())
    print('Downloading Assignee...')
    thra = Thread(target=getAssignee,args=())
    print('Downloading Priority...')
    thrpri = Thread(target=getPriority,args=())
    threadlst = [thrpro, thrb, thri, thrs, thra, thrpri]
    for thread in threadlst:
        thread.start()
    for thread in threadlst:
        thread.join()
    print('Writing to disc')
    glob_dic.tips.write_file(un)
    # pass


def tryload(username):
    directory = "res/downloads/"
    if not access(directory, F_OK):
        mkdir(directory)
    try:
        filename = '{}{}.json'.format(directory, username)
        f = open(filename, 'r')
        data = json.loads(f.read())
        f.close()

        glob_dic.tips.dic = data
        return True
    except FileNotFoundError as err:
        mylog.error(err)
        return False
    except json.decoder.JSONDecodeError as err:
        mylog.error(err)
        return False

# tryload()
# ultimateGetIssues()
# print(glob_dic.tips.get_value('issues'))
# f = open('issues.json','w')
# f.write(json.dumps(glob_dic.tips.get_value('issues')))
# f.close
# def getIssueFromSprint():
#     getSprint()
#     glob_dic.set_value('issues',{})
#     lst = glob_dic.tips.get_value('sprint')
#     issues = []
#     for sp in lst:
#         sid = glob_dic.tips.get_value('sid')[0].get(sp.lower())
#         url, headers = prepare('getSprint','/{}/issue'.format(sid))

#         f, r = send_request(url, method.Get, headers, None, None)
#         if not f:
#             return False
#         issues += r.get('issues')
        
#         for issue in r.get('issues'):
#             glob_dic.get_value('issues')[issue.get('key')] = sp




# def getPermission():
#     url, headers = prepare('mypermission')

#     print(url)
#     print(headers)

#     f, r = send_request(url, method.Get, headers, None, None)

# def getProjectKey():
#     url, headers = prepare('createmeta')

#     f, r = send_request(url, method.Get, headers, None, None)
#     if not f:
#         return False, r
#     for p in r.get('projects'):
#         print(p.get('key'))
# login(['zhengxp2','bvfp-6217'])
# getProjectKey()
# def getAss():
#     url, headers = prepare('query')
#     data = {}
#     data["jql"] = '{}'.format('project=TAN')
#     data["startAt"] = 0
#     data["maxResults"] = 100
#     dic = {}
#     while data.get("startAt") < 1000:
#         print('DOING {}'.format(data.get("startAt")))
#         tosend = json.dumps(data)
#         f, r = send_request(url, method.Post, headers, None, tosend)
#         print(type(r))
#         dic.update(r)
#         data["startAt"] = data.get("startAt") + 100
#     f = open('jqlexample.json','a')
#     f.write(json.dumps(r))
#     f.close
    # print(url, headers, data)
# getAss()
# print(glob_dic.tips.get_value('assignee'))
# getPermission()

# try:
#     tryload()
# except FileNotFoundError as fe:
# mylog.error(fe)
# download()
# login([
# login(['zhengxp2','bvfp-6217'])
# download()
# print(glob_dic.tips.get_value('assignee'))
# getProject()
# login(['admin', 'admin'])

# login(['admin','admin'])
# getProjectKey()
# login(['zhengxp2', 'bvfp-6217'])
