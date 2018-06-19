
class Prompter:

    def __init__(self):
        pass

    def auto_complete(self, position, tokens):
        result = []
        complete = False
        for token in tokens:
            pre_position = position
            # traverse every chlid nodes
            for child in position.getchildren():
                if child.tag == "keyword" and child.attrib['name'] == token:
                    position = child
                    break
                elif child.tag == "optional" or child.tag == "required":
                    position = child
                    break
            if position == pre_position:
                if(token != tokens[-1]):
                    return []
                complete = True

        keywords = position.findall("./keyword")
        if keywords:
            if complete:
                for keyword in keywords:
                    if keyword.attrib['name'].startswith(tokens[-1]):
                        result.append(keyword.attrib['name'])
                        break
            else:
                for keyword in keywords:
                    result.append(keyword.attrib['name'])
        else:
            result = ["tips about project/sprint/status"]

        return result





