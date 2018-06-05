

class SiraController():

    def __init__(self, view, model):
        self.view = view
        self.model = model

    def processInput(self, instance, string):
        # instance.set_pwd_mode()
        # self.view.request_input("sample:", instance)
        return [string, ">>>"]