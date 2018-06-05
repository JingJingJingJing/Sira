import json
from token import Token, Token_Type

global tables
global records
global separater
global parma_name
records = []
separater = " "

def cal(command):
    tokens = parse(command)

    if(len(tokens) <= 0):
        return [">>>"]

    for token in tokens:
        records.append(token)
    method = records[0].value
    for record in records:
        if(records.index(record) != 0):
            method += ("_" + record.value)
    method_exist = hasattr(json,method)
    if(method_exist):
        #return [func(),">>>"]
        records.clear()
        # TODO(xiapeng): deal with args
        return [method+"()",">>>"]
    else:
        last_token = records[len(records)-1.value + ":"]
        if(last_token.value in tables):
            if(isinstance(tables[last_token.value],list)):
                return tables[last_token.value]
            else:
                keys = []
                for key in tables[last_token.value]:
                    keys.append(key + ":")
                    return keys

        else:
            return [""]

def parse(command):
    tokens = list()
    words = command.split(separater)
    for word in words:
        tokens.append(get_token(word))
    return tokens

def get_token(word):
    if(word in tables['reserved']):
        return Token(word,Token_Type.reserved)
    else:
        if word.isdigit():
            return Token(word, Token_Type.number)
        else:
            return Token(word, Token_Type.identify)

def initial_tables():
    global tables
    gs = open("res/glossary.json", encoding="utf-8")
    tables = json.load(gs)

initial_tables()
print(cal("create"))