

class SiraController():

    def __init__(self, view, model):
        self.view = view
        self.model = model

    def processInput(self, string):
        # self.view.historyText.insert_text(string + "\n")
        self.view.commandText.insert_text("\n" + string + "\n>")
        return True