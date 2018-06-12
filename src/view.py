import kivy.properties as kp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.settings import Settings, SettingsWithSidebar
from kivy.uix.widget import Widget
from kivy.utils import boundary

from advancedtextinput import AdvancedTextInput


class SiraApp(App):

    """The application class for Sira application, working as a view.

    extends:
        kivy.app.App

    Instance Variables:
        Class-scope Variables:
            info --  kivy.properties.ListProperty (default [])
            [TODO] option -- kivy.properties.ListProperty (default [])
            username -- kivy.properties.StringPorperty (default ""s)

        Method-established Variables:
            commandText -- advancedtextinput.AdvancedTextInput (default None)
            config_func_dict -- dict((str, str) : callable)

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
        _on_cmd_idf(self, str) -> None
        _on_font_size(self, str) -> None
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
        on_username(self, kivy.uix.widget.Widget(), str) -> None

    Conventions:
        {
               info = []
            && option = []
        }
    """
<<<<<<< HEAD
  
=======

>>>>>>> master
    info = kp.ListProperty([])
    """
    """

    # option = kp.ListProperty([])

    username = kp.StringProperty(None)

    def __init__(self, **kwargs):
        super(SiraApp, self).__init__(**kwargs)
<<<<<<< HEAD
        self.__events__ = ["on_info", "on_option", "on_username"]
        # Element Constraint: {(section, key): func}
        self.config_func_dict = {
            ("Text", "cmd_identifier") : self._on_cmd_idf,
            ("Text", "font_size") : self._on_font_size
        }
        
 
=======
        self.__events__ = ["on_info", "on_option"]

>>>>>>> master
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.commandText = Builder.load_file("res/sira.kv")
        self.username = self.config.get("Text", "username")
        self.controller.cursor = self.username + self.controller.normal_cursor
        self.commandText.protected_len = len(self.username) + 1
        self.commandText.text = self.username + ">"
        return self.commandText

    def build_config(self, config):
        config.read("src/sira.ini")

    def build_settings(self, settings):
        settings.add_json_panel("Text Option", self.config,
                                filename="res/sira.json")

    def on_config_change(self, config, section, key, value):
        if config == self.config:
            self.config_func_dict[(section, key)](value)

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

    def _on_cmd_idf(self, value):
        self.controller.normal_cursor = value

    def _on_font_size(self, value):
        value = boundary(int(value), 1, 40)
        self.commandText.font_size = value

    def _on_tab(self, instance):
        pass

    def _on_command(self, instance):
        string = instance._lines[len(
            instance._lines) - 1][instance.protected_len:]
        if instance.password_mode:
            string = instance.password_cache
            instance.password_mode = False
        elif instance.command_mode:
            instance.history_stack.push(string)
        instance.history_stack.reset_traversal()
        self.controller.processInput(instance, string)
        return True

    def _stop_interaction(self, instance):
        if not self.commandText.command_mode:
            self.controller.closeinteractive()
            instance.password_mode = False

    def on_info(self, instance, info):
        if self.info == []:
            return
        self.commandText.do_cursor_movement("cursor_end", control=True)
        self.commandText.protected_len = len(info[-1])
        for s in info:
            self.commandText.insert_text("\n" + str(s))
        self.info = []

    def on_option(self, instance, info):
        pass

    def on_username(self, instance, value):
        self.config.set("Text", "username", value)
        self.config.write()
