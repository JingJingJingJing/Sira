from utils import issue_create_args

''' Optional field filled out below
    
'''
def addfield(dic, lst):
    
    return dic

''' Requried field filled out below '''
def issue_create_data():
    project = issue_create_args.get('project')
    summary = issue_create_args.get('summary')
    issuetype = issue_create_args.get('issuetype')
    return_dic = {
        "fields": {
            "project": {
                "key": project
            },
            "summary": summary,
            "issuetype": {
                "name": issuetype
            }
        }
    }
    return return_dic
