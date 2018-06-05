import json
from token import Token, Token_Type

global tables
global separater
separater = " "

def cal(command):
    tokens = parse(command)

    if(len(tokens) <= 0):
        return [">>>"]

    cmt = tokens[0]     #command type
    if(len(tokens) > 1):
        method = ""
        if(cmt.type == Token_Type.reserved and cmt.value in tables):
            method = (cmt.value)
            for token in tokens:
                if token.value in tables[cmt.value]:
                    method += ("_"+token.value)
                if (tokens.index(token) == len(tokens)-1):
                    if(token.type == Token_Type.identify or token.type == Token_Type.number):
                         return ["getattr(api,\""+method+"\")("+token.value+")",">>>"]
                    else:
                        return ["getattr(api,\""+method+"\")",">>>"]
    else:
        if cmt.value == 'login':
            # username = request_input("name:")
            # set_pwd_mode()
            # pwd = request_input("pwd:")
            # return [login(username,pwd), ">>>"]
            return ["login(username,pwd)",">>>"]
            

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
print(cal("show projesct"))