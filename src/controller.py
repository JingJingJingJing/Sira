

class SiraController():

    def __init__(self, view, model):
        self.view = view
        self.model = model

    def processInput(self, instance, string):
        # self.view.set_pwd_mode(instance)
        # import pdb; pdb.set_trace()
        # self.view.request_input("sample:", instance)
        return [string, ">>>"]