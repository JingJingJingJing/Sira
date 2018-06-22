import re
from utils import glob_dic

class Prompter:

    blank = " "

    def __init__(self):
        self.separater = re.compile("\\s+")

    def auto_complete(self, position, command):
        result = []
        complete = False

        l = len(command)
        if l > 0 and command[-1] != Prompter.blank:
            complete = True
        elif l > 1 and command[-2] == Prompter.blank:
            return result

        tokens = self.separater.split(command.strip())
        print("tokens:")
        print(tokens)
        for token in tokens:
            pre_position = position
            # traverse every chlid nodes
            for child in position.getchildren():
                if child.tag == "keyword" and child.attrib['name'] == token:
                    position = child
                    break
                elif (child.tag == "optional" or child.tag == "required") and token:
                    position = child
                    break
            if position == pre_position and l > 0:
                if(token != tokens[-1] or not complete):
                    return result

        keywords = position.findall("./keyword")
        if keywords or complete:
            for keyword in keywords:
                name = keyword.attrib['name']
                if complete and name.startswith(tokens[-1]):
                    result.append(name)
                elif not complete:
                    result.append(name)
        else:
            option = position.find("./required")
            if not option:
                option = position.find("./optional")
            if option and option.attrib['name'] in glob_dic.tips.dic:
                result = glob_dic.tips.get_value(option.attrib['name'])
        return result

