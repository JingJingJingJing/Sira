import xml.etree.ElementTree as ET
import login

class Parser():
    def __init__(self):
        self.position = None
        self.records = []
        self.separater = " "
        self.tree = ET.parse("res/glossary.xml").getroot()

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
                    break
            if(pre_position == self.position):
                self.records.clear()
                self.position = None
                return ["error command", ">>>"]
        if(self.position.find("./optional") is not None):
            return [self.position.find("./interactive").text]
        else:
            method = self.position.find("./function").attrib['name']
            para = self.position.find("./function").attrib['para']
            if(para is not None):
                para_count = len(para.split(self.separater))
            paras = []
            while(para_count > 0):
                paras.append(self.records[len(self.records) - para_count])
                para_count=para_count-1

            print(paras)
            self.records.clear()
            self.position = None
            return [getattr(login, method)(paras),">>>"]

    def parse(self, command):
        return command.split(self.separater)

def main():
    print(Parser().cal("sira login zhengxp woaixiaojing38"))

if __name__ == '__main__':
    main()