import xml.etree.ElementTree as ET
import threading
import re
import login
import query

class SiraController():

    """The controller class which can handle input command and return the corresponding function result

    public methods:
        processInput(self, instance, string) -> None
        cal(self,command) -> None
        closeinteractive -> None

    """
    normal_cursor = ">"
    no_need_login = ["sira", "sira login", "login", "exit", "clear"]

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.separater = re.compile("\\s+")    # command separater
        self.position = None    # the current position of tree
        self.paras = []         # hold the paras of command
        self.tree = ET.parse("res/glossary.xml").getroot()

    def processInput(self, string):
        try:
            self.cal(string)
        except Exception:
            self.sendinfo("error while processing")

    def cal(self, command): 
        # return when command is empty in non-interactive mode
        if(len(command) <= 0 and (self.position is None or self.position == self.tree)):
            self.view.set_command_mode(True)
            self.view.print_header()
            return

        tokens = self.separater.split(command.strip())

        if(self.position is None):
            self.position = self.tree

        for token in tokens:
            pre_position = self.position
            for child in self.position.getchildren():
                if(child.tag == "keyword" and child.attrib['name'] == token):
                    # exclude keywords need to login
                    if((not self.view.username) and (token not in self.no_need_login)):
                        return self.sendinfo("Please login first")
                    # exclude login keyword if have logged in
                    elif(self.view.username and token == "login"):
                        return self.sendinfo("already logged in as " + self.view.username)
                    else:
                        self.position = child
                        break
                elif(child.tag == "optional" or child.tag == "required"):
                    self.position = child
                    self.paras.append(token)
                    break
            # do not extend deep
            if(pre_position == self.position):
                if(pre_position.tag != "keyword" and self.paras):
                    para = self.paras.pop()
                    para = para + " " + token
                    self.paras.append(para)
                else:
                    return self.sendinfo("error command")
        # return if has sub-node ,exec function if has't
        if(self.position.find("./required") is not None):
            # call function first if exist
            func = self.position.find("./function")
            if(func is not None):
                if(func.attrib['object']):
                    getattr(eval(func.attrib['object']),func.attrib['name'])()
                else:
                    getattr(self,func.attrib['name'])()
            # display intseractive text
            interactive = self.position.find("./interactive")
            self.view.set_command_mode(False)
            if(interactive is not None):
                self.view.info = [interactive.text]
            else:
                self.view.info = [""]
            return
        elif(self.position.find("./keyword") is not None):
            # display intseractive text
            interactive = self.position.find("./interactive")
            if(interactive is not None):
                self.view.set_command_mode(False)
                self.view.info = [interactive.text, "-"]
                return
            else:
                return self.sendinfo("error command")
        else:
            self.view.commandText.readonly = True
            functag = self.position.find("./function")
            if(functag.attrib['multi-thread'] == 'True'):
                threading.Thread(None,self.execfunc).start()
            else:
                if(functag.attrib['name'] == "on_clear"):
                    self.view.commandText.readonly = False
                    self.view.print_header()
                    self.view.on_clear()
                    self.clearcache()
                else:
                    self.execfunc()
            return

    def execfunc(self):
        functag = self.position.find("./function")
        obj = functag.attrib['object']
        name = functag.attrib['name']
        if(self.paras):
            result = getattr(eval(obj), name)(self.paras)
        else:
            result = getattr(eval(obj), name)()
        # set cursor value to username when login successd
        if(name == "login" and result[0]):
            self.view.username = self.paras[0]
        elif((name == "login" and not result[0]) or name == "logout"):
            self.view.username = ""
        result = result[1] if (name == "login") else result
        # display result
        self.sendinfo(result)

    def sendinfo(self, msg):
        self.clearcache()
        self.view.commandText.readonly = False
        self.view.set_command_mode(True)
        if(msg):
            self.view.info = [msg]
        self.view.print_header()

    def closeinteractive(self):
        if(self.position is None or self.position == self.tree):
            pass
        self.clearcache()
        self.view.commandText.readonly = False
        self.view.info = ["interactive mode closed"]
        self.view.print_header()

    def clearcache(self):
        self.position = None
        self.paras.clear()

