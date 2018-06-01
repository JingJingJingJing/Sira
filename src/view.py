from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from advancedtextinput import AdvancedTextInput

class DemoApp(App):

    def __init__(self, **kwargs):
        super(DemoApp, self).__init__(**kwargs)

    def setController(self, controller):
        self.controller = controller

    def on_command(self, instance):
        self.controller.processInput(
            instance.text[instance.text.rindex('>') + 1:])

    def build(self):

        self.commandText = AdvancedTextInput()
        self.commandText.text = ">"
        # self.commandText.multiline = False
        self.commandText.background_color = [0, 0, 0, 1]
        self.commandText.focus = True
        self.commandText.cursor_color = [1, 1, 1, 1]
        self.commandText.foreground_color = [1, 1, 1, 1]
        self.commandText.padding = [20, 20, 20, 0]
        self.commandText.bind(on_text_validate=self.on_command)

        return self.commandText
