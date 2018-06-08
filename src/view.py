from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import kivy.properties as kp

from advancedtextinput import AdvancedTextInput


class SiraApp(App):

    info = kp.ListProperty([])
    # option = kp.ListProperty([])

    def __init__(self, **kwargs):
        super(SiraApp, self).__init__(**kwargs)

    def setController(self, controller):
        self.controller = controller
        self.info = []

    def on_tab(self, instance):
        pass
        
    def on_command(self, instance):
        string = instance._lines[len(instance._lines) - 1]\
                [instance.protected_len:]
        if string == "exit":
            self.stop()
            return True
        if instance.password_mode:
            string = instance.password_cache
            instance.password_mode = False
        elif instance.command_mode:
            instance.history_stack.push(string)
        instance.history_stack.reset_traversal()
        self.controller.processInput(instance, string)
        return True

    def on_info(self, instance, info):
        # import pdb; pdb.set_trace()
        self.commandText.do_cursor_movement("cursor_end")
        self.commandText.protected_len = len(info[-1])
        for s in info:
            self.commandText.insert_text("\n" + str(s))

    def set_pwd_mode(self):
        self.commandText.password_mode = True

    def set_command_mode(self, value):
        self.commandText.command_mode = value

    def build(self):
        self.commandText = Builder.load_file("../res/sira.kv")
        return self.commandText

    def build_settings(self, settings):
        pass