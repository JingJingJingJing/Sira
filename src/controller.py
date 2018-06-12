import xml.etree.ElementTree as ET
import threading
import re
import login
import query
import time

class SiraController():

    normal_cursor = ">"
    interactive_cursor = "-"

    def __init__(self, view, model):
        self.cursor = self.normal_cursor
        self.view = view
        self.model = model
        self.separater = re.compile("\\s+")    # command separater
        self.position = None    # the current position of tree
        self.paras = []         # hold the paras of command
        self.tree = ET.parse("res/glossary.xml").getroot()

    def processInput(self, instance, string):
        try:
            self.cal(string)
        except Exception:
            self.view.info = ["error while processing", self.cursor]

    def cal(self, command):
        # return when command is empty in non-interactive mode
        if(len(command) <= 0 and (self.position is None or self.position == self.tree)):
            self.view.set_command_mode(True)
            self.view.info = [self.cursor]
            return

        tokens = self.separater.split(command.strip())

        if(self.position is None):
            self.position = self.tree

        for token in tokens:
            pre_position = self.position
            for child in list(self.position):
                if(child.tag == "keyword" and child.attrib['name'] == token):
                    self.position = child
                    break
                elif (child.tag == "optional" or child.tag == "required"):
                    if(token):
                        self.position = child
                        self.paras.append(token)
                    break
            # no keyword paired, return error
            if(pre_position == self.position and token):
                self.clearcache()
                self.view.set_command_mode(True)
                self.view.info = ["error command", self.cursor]
                return

        if(self.position.find("./required") is not None):
            # call function first if exist
            func = self.position.find("./function")
            if(func is not None):
                if(func.attrib['object']):
                    getattr(eval(func.attrib['object']),func.attrib['name'])()
                else:
                    getattr(self,func.attrib['name'])()
            # return intseractive text
            interactive = self.position.find("./interactive")
            self.view.set_command_mode(False)
            if(interactive is not None):
                self.view.info = [interactive.text]
            else:
                self.view.info = [""]
            return
        elif(self.position.find("./keyword") is not None):
            interactive = self.position.find("./interactive")
            if(interactive is not None):
                self.view.set_command_mode(False)
                self.view.info = [interactive.text, self.interactive_cursor]
                return
            else:
                self.view.set_command_mode(True)
                self.clearcache()
                self.view.info = ["error command", self.cursor]
                return
        else:
            self.view.commandText.readonly = True
            functag = self.position.find("./function")
            if(functag.attrib['multi-thread'] == 'True'):
                threading.Thread(None,self.execfunc).start()
            else:
                if(functag.attrib['name'] == "on_clear"):
                    self.view.commandText.readonly = False
                    self.view.info = [self.cursor]
                    self.view.on_clear()
                else:
                    self.execfunc()
            return

    def execfunc(self):
        functag = self.position.find("./function")
        funcobj = functag.attrib['object']
        if(self.paras):
            result = getattr(eval(funcobj), functag.attrib['name'])(self.paras)
        else:
            result = getattr(eval(funcobj), functag.attrib['name'])()
        # set cursor value to username when login successd
        if(funcobj == "login" and result[0]):
            self.view.username = self.paras[0]
            self.cursor = self.paras[0] + self.normal_cursor
        elif((funcobj == "login" and not result[0]) or funcobj == "logout"):
            self.view.username = ""
            self.cursor = self.normal_cursor
        self.view.commandText.readonly = False
        if(result):
            if(funcobj == "login"):
                self.view.info = [result[1], self.cursor]
            else:
                self.view.info = [result, self.cursor]
        else:
            self.view.info = [self.cursor]
        self.clearcache()
        self.view.set_command_mode(True)

    def closeinteractive(self):
        if(self.position is None or self.position == self.tree):
            pass
        self.clearcache()
        self.view.set_command_mode(True)
        self.view.commandText.readonly = False
        self.view.info = ["interactive mode closed", self.cursor]

    def clearcache(self):
        self.position = None
        self.paras.clear()

