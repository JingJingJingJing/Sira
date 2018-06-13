import json
defaultList = ['summary','issuetype','assignee','status','fixVersions','project']
def getIssue(s, key):
    j = json.loads(s)
    issue = []
    try:
        issue = j['issues']
    except KeyError:
        pass
    if key is None:
        return issue
    else:
        for i in range(0,len(issue)):
            if issue[i]['key'] == key:
                return [issue[i]]

        return None

'''
type | number | title | assignee | sprint | status | fixed version | project
'''
def getField(issue, field):
    if field is None:
        return defaultField(issue)
    if isinstance(issue['fields'][field], dict):
        return {field:issue['fields'][field]['name']}
    return {field:issue['fields'][field]}

def defaultField(issue):
    defaultList = ['summary','issuetype','assignee','status','fixVersions','project']
    dic = {}
    for i in defaultList:
        dic.update(getField(issue,i))
    return dic

def dtos(dic,issue):
    string ='Issue {}: '.format(issue)
    for i in dic:
        string += ' {} '.format(dic[i])
    return string