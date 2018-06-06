import xml.etree.ElementTree as ET
import login

class SiraController():

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.records = []
        self.separater = " "    # command separater
        self.position = None    # the current position of tree
        self.paras = []         # hold the paras of command
        self.tree = ET.parse("res/glossary.xml").getroot()

    def processInput(self, instance, string):
        # instance.set_pwd_mode()
        # self.view.set_pwd_mode()
        
        return self.cal(string)

    def cal(self, command):
        tokens = self.parse(command)

        if(len(tokens) <= 0):
            return [">>>"]

        if(self.position is None):
            self.position = self.tree

        for token in tokens:
            self.records.append(token)
            pre_position = self.position
            for child in list(self.position):
                if(child.tag == "keyword" and child.attrib['name'] == token):
                    self.position = child
                    break
                elif (child.tag == "optional"):
                    self.position = child
                    self.paras.append(token)
                    break
            if(pre_position == self.position):
                self.records.clear()
                self.paras.clear()
                self.position = None
                return ["error command", ">>>"]
        if(self.position.find("./optional") is not None):
            # call function first if exist
            func = self.position.find("./function")
            if(func is not None):
                getattr(eval(func.attrib['object']),func.attrib['name'])()
            # return intseractive text
            interactive = self.position.find("./interactive")
            if(interactive is not None):
                return [interactive.text]
            else:
                return [""]
        else:
            method = self.position.find("./function").attrib['name']

            self.records.clear()
            
            self.position = None
            result = getattr(eval("login"), method)(self.paras)
            self.paras.clear()
            return [result, ">>>"]

    def parse(self, command):
        return command.split(self.separater)

def main():
    print(SiraController(None,None).cal("sira login zhengxp"))

if __name__ == '__main__':
    main()
