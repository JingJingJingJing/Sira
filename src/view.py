from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from advancedtextinput import AdvancedTextInput
#from asyncio import Lock
from multiprocessing.pool import ThreadPool
from threading import Lock


class SiraApp(App):

    def __init__(self, **kwargs):
        super(SiraApp, self).__init__(**kwargs)
        self.lock = Lock()
        self.text_input = ""

    def setController(self, controller):
        self.controller = controller

    def on_command(self, instance):
        string = instance._lines[instance.last_row][instance.protected_len:]
        if instance.pending_request:
            self.text_input = instance.password_cache\
                if instance.password_mode else string
            # self.lock.release()
            return True
        instance.history_stack.push(string)
        instance.history_stack.reset_traversal()
        info = self.controller.processInput(instance, string)
        for s in info:
            instance.insert_text("\n" + s)
        instance.protected_len = len(info[-1])
        return True

    def request_input(self, s:str, instance, mutex):
        instance.insert_text("\n" + s)
        instance.protected_len = len(s)
        instance.pending_request = True



        # yield from self.lock
        # self.lock.acquire()
        # return self.text_input

    def set_pwd_mode(self, instance):
        instance.password_mode = True

    def build(self):
        self.commandText = AdvancedTextInput()
        self.commandText.text = ">>>"
        self.commandText.background_color = [0, 0, 0, 1]
        self.commandText.focus = True
        self.commandText.cursor_color = [1, 1, 1, 1]
        self.commandText.foreground_color = [1, 1, 1, 1]
        self.commandText.padding = [20, 20, 20, 0]
        self.commandText.bind(on_text_validate=self.on_command)

        return self.commandText