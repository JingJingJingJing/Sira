import os
import json

config = {}
config_path = ''
build_in_config = {
    "verbose": "False",
    "credential": {
        "domain":"https://lnvusjira.lenovonet.lenovo.local"
    },
    "query_field": {
        "issue_default": [
            "assignee",
            "reporter",
            "priority",
            "status",
            "labels",
            "fixVersions",
            "summary"
        ],
        "project_default": [
            "name",
            "key",
            "lead"
        ],
        "board_default": [
            "id",
            "name"
        ]
    },
    "query_mode": {
        "issue_default": "mine",
        "project_default": "",
        "board_default": ""
    }
}

def read_from_config():
    # cache
    global config
    global config_path
    if config:
        return config
    if config_path == "bulit-in":
        return build_in_config
    if config_path and os.path.isfile(config_path):
        return read_file(config_path)
    # local
    cwd = os.getcwd()
    while cwd:
        filepath = cwd + "//.sirarc"
        if os.path.isfile(filepath):
            content = read_file(filepath)
            if content:
                config_path = filepath
                config = json.loads(read_file(filepath))
                return config
        dir = os.path.dirname(cwd)
        if cwd == dir:
            break
        cwd = dir
    # global
    userpath = os.path.expanduser('~')
    filepath = userpath + "//.sirarc"
    if os.path.isfile(filepath):
        content = read_file(filepath)
        if content:
            config_path = filepath
            config = json.loads(read_file(filepath))
            return config
    # bulit-in
    config_path = "bulit-in"
    config = build_in_config
    return build_in_config

def write_to_config(dic_path, field, info, init=False):
    global config
    global config_path
    if not config_path and not init:
        read_from_config()
    if config_path == "bulit-in" or init:
        config_path = os.getcwd() + "//.sirarc"
        data = build_in_config
    else:
        fh = open(config_path, 'r')
        content = fh.read()
        data = json.loads(content) if content else {}
    dic = data
    for x in dic_path:
        dic = dic[x]
    if isinstance(field, list):
        for i in range(len(field)):
            if isinstance(info, list):
                if len(field) != len(info):
                    fh.close()
                    raise "Field and Info length need to be equal"
                dic[field[i]] = info[i]
            else:
                dic[field[i]] = info
    else:
        dic[field] = info
    config = data
    fh = open(config_path, 'w')
    ret = json.dumps(data,indent=4)
    fh.write(ret)
    fh.close()
    return ret

def read_file(filepath):
    file = open(filepath, "r")
    content = file.read()
    file.close()
    return content


if __name__ == '__main__':
    read_from_config()
    