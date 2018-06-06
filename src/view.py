from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from advancedtextinput import AdvancedTextInput


class SiraApp(App):

    def __init__(self, **kwargs):
        super(SiraApp, self).__init__(**kwargs)

    def setController(self, controller):
        self.controller = controller

    def on_command(self, instance):
        if instance.password_mode:
            string = instance.password_cache
            instance.password_mode = False
        else:
            string = instance._lines[len(instance._lines) - 1]\
                [instance.protected_len:]
            instance.history_stack.push(string)
        instance.history_stack.reset_traversal()
        info = self.controller.processInput(instance, string)
        for s in info:
            instance.insert_text("\n" + s)
        instance.protected_len = len(info[-1])
        return True

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