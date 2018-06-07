import xml.etree.ElementTree as ET
import re
import login

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
        # instance.set_pwd_mode()
        # self.view.set_pwd_mode()
        return self.cal(string)

    def cal(self, command):
        tokens = self.separater.split(command.strip())
        print(tokens)

        if(len(tokens) <= 0):
            self.view.set_command_mode(True)
            return [self.cursor]

        if(self.position is None):
            self.position = self.tree

        for token in tokens:
            pre_position = self.position
            for child in list(self.position):
                if(child.tag == "keyword" and child.attrib['name'] == token):
                    self.position = child
                    break
                elif (child.tag == "optional" or child.tag == "required"):
                    self.position = child
                    self.paras.append(token)
                    break
            # no keyword paired, return error
            if(pre_position == self.position):
                self.clearcache()
                self.view.set_command_mode(True)
                return ["error command", self.cursor]

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
                return [interactive.text]
            else:
                return [""]
        elif(self.position.find("./keyword") is not None):
            interactive = self.position.find("./interactive")
            self.view.set_command_mode(True)
            if(interactive is not None):
                return [interactive.text, self.interactive_cursor]
            else:
                self.clearcache()
                return ["error command", self.cursor]
        else:
            functag = self.position.find("./function")
            result = getattr(eval(functag.attrib['object']), functag.attrib['name'])(self.paras)
            # set cursor value to username when login successd
            if(functag.attrib['object'] == "login" and result == 1):
                self.cursor = self.paras[0] + " > "
            self.clearcache()
            self.view.set_command_mode(True)
            return [result, self.cursor]

    def clearcache(self):
        self.position = None
        self.paras.clear()

def main():
    print(SiraController(None,None).cal("sira query number TAN-6148"))

if __name__ == '__main__':
    main()
