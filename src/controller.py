class SiraController():

    def __init__(self, view, model):
        self.view = view
        self.model = model

    def processInput(self, instance, string):
        # self.view.set_pwd_mode(instance)
        if string == "test":
            import pdb; pdb.set_trace()
        return [string, ">>>"]