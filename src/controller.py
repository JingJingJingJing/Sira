from analyzer import Parser

class SiraController():

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.parser = Parser()

    def processInput(self, instance, string):
        # instance.set_pwd_mode()
        return self.parser.cal(string)
