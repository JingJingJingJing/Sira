import json
import sys

import kivy.properties as kp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.settings import Settings, SettingsWithSidebar
from kivy.uix.widget import Widget

from advancedtextinput import AdvancedTextInput


class SiraApp(App):

    """The application class for Sira application, working as a view.

    extends:
        kivy.app.App
    
    Instance Variables:
        Class-scope Variables:
            info --  kivy.properties.ListProperty (default [])
            [TODO] option -- kivy.properties.ListProperty (default [])
        
        Method-established Variables:
            commandText -- advancedtextinput.AdvancedTextInput (default None)

    Public Methods:
        Overrided from kivy.app.App:
            build(self) -> kivy.uix.widget.Widget()
            build_config(self, config) -> None
            build_settings(self, kivy.uix.settings.Settings()) -> None
            on_config_change(self, config, section, key, value) -> None
        
        Original:
            on_clear(self) -> None
            set_command_mode(self, bool) -> None
            set_controller(self, controller.SiraController()) -> None
            set_pwd_mode(self) -> None


    Private Methods:
        __init__(self, **kwargs) -> None
        _on_tab(self, kivy.uix.widget.Widget()) -> None
        _on_command(self, kivy.uix.widget.Widget()) -> None
        _stop_interaction(self, kivy.uix.widget.Widget()) -> None

    Events:
        `on_info`
            Fired when info is changed. This will print everything, one element
            per line, in the {@code info} to the command window and move the
            cursor to the end of text.

        `on_option`
            Fired when option is changed. This will print everything, one
            element per line, in the {@code info} to the command window without
            moving the cursor.

    Event Driven Methods:
        on_info(self, kivy.uix.widget.Widget(), list()) -> None
        on_option(self, kivy.uix.widget.Widget(), list()) -> None

    Conventions:
        {
               info = []
            && option = []
        }
    """
    
    info = kp.ListProperty([])
    """
    """

    # option = kp.ListProperty([])

    def __init__(self, **kwargs):
        super(SiraApp, self).__init__(**kwargs)
 
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.commandText = Builder.load_file("res/sira.kv")
        return self.commandText

    def build_config(self, config):
        config.read("res/sira.ini")

    def build_settings(self, settings):
        settings.add_json_panel("Text Option", self.config,
            filename="res/sira.json")

    def on_config_change(self, config, section, key, value):
        if config == self.config:
            on_cmd_idtf = lambda value: print(value)
            on_font_size = lambda value: print(value)
            switch_dict = {
                ("Text", "cmd_identifier") : on_cmd_idtf,
                ("Text", "font_size") : on_font_size
            }
            switch_dict[(section, key)](value)

    def on_clear(self):
        instance = self.commandText
        instance.scroll_y = (len(instance._lines) - 1) * instance.line_height

    def set_pwd_mode(self):
        self.commandText.password_mode = True

    def set_command_mode(self, value):
        self.commandText.command_mode = value

    def set_controller(self, controller):
        self.controller = controller
        self.info = []

    def _on_tab(self, instance):
        pass
        
    def _on_command(self, instance):
        string = instance._lines[len(instance._lines) - 1]\
                [instance.protected_len:]
        if string == "clear":
            self.info = [">"]
            self.on_clear()
            return
        if instance.password_mode:
            string = instance.password_cache
            instance.password_mode = False
        elif instance.command_mode:
            instance.history_stack.push(string)
        instance.history_stack.reset_traversal()
        self.controller.processInput(instance, string)
        return True

    def _stop_interaction(self, instance):
        self.controller.closeinteractive()
        instance.password_mode = False

    def on_info(self, instance, info):
        if self.info == []:
            return
        self.commandText.do_cursor_movement("cursor_end")
        self.commandText.protected_len = len(info[-1])
        for s in info:
            self.commandText.insert_text("\n" + str(s))
        self.info = []

    def on_option(self, instance, info):
        pass
