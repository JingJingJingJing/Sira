from kivy.app import App
from kivy.config import ConfigParser
from kivy.lang import Builder
from kivy.uix.settings import Settings, SettingsWithSidebar
from kivy.uix.widget import Widget

from controller import SiraController
from features.autocompletion import Completable
from features.cmdreaction import CommandReactive
from features.sirasettings import Mutative
from utils import asserts, func_log, overrides, write_memo_log, glob_dic


class SiraApp(App, CommandReactive, Completable, Mutative):

    """The application class for Sira application, working as a view.

    Extends:
        kivy.app.App
        features.autocompletion.Completable
        features.cmdreaction.CommandReactive
        features.sirasetting.Mutative

    Instance Variables:
        Method-established Variables:
            commandText -- advancedtextinput.AdvancedTextInput
            config -- kivy.config.ConfigParser
            config_func_dict -- dict((str, str) : callable)
            controller -- controller.SiraController

    Public Methods:
        Overrided from kivy.app.App:
            __init__(self, **kwargs) -> None
            build(self) -> advancedtextinput.AdvancedTextInput()
            build_config(self, config.ConfigParser) -> None
            build_settings(self, kivy.uix.settings.Settings) -> None
            on_config_change(self, config.ConfigParser, str, str, str) -> None
            on_stop(self) -> None
            stop(self) -> (True, None)

        Original:
            set_controller(self, controller.SiraController) -> None
    """

    @overrides(App)
    def __init__(self, **kwargs) -> None:
        """Constructor of SiraApp.

        [ensures]:  isinstance(self.__events__, list),
                    isinstance(self.config_func_dict)
        [calls]:    super(SiraApp, self).__init__
        """
        super(SiraApp, self).__init__(**kwargs)
        self.__events__ = ["on_info", "on_option", "on_username"]
        # Element Constraint: {(section, key): func}
        self.config_func_dict = {
            ("Text", "cmd_identifier"): self._on_cmd_idf,
            ("Text", "font_size"): self._on_font_size,
            ("Text", "font_name"): self._on_font_name,
            ("Jira", "url"): self._on_url,
            ("Jira", "timeout"): self._on_timeout,
            ("Jira", "protocol"): self._on_protocol,
            ("Option", "space_completion"): self._on_space_completion,
            ("Option", "tab_completion"): self._on_tab_completion,
            ("Option", "options_per_line"): self._on_options_per_line,
            ("Result", "max_result"): self._on_max_result
        }

    @overrides(App)
    def build(self) -> Widget:
        """Builder of the application interface, called after build_config().

        [requires]: isinstance(self.config, kivy.config.Config)
                    [see [ensures] of build_config]
        [ensures]:  self.header = self.config.get("Text", "username")
                                  + self.config.get("Text", "cmd_identifier)
                    isinstance(self.commandText, Widget)
                    self.commandText.text = self.header
                    self.protected_text = self.header
        [calls]:    _reset_header
                    [reset self.commandText.protected_len]
        """
        if not asserts(isinstance(self.config, ConfigParser),
                       "self.config is not initialized."):
            return

        self.settings_cls = SettingsWithSidebar
        self.username = self.config.get("Text", "username")
        self.options_per_line = max(
            int(self.config.get("Option", "options_per_line")), 1)
        self.space_completion = self.config.get(
            "Option", "space_completion") == "1"
        self.tab_completion = self.config.get(
            "Option", "tab_completion") == "1"
        self._reset_header(self.username,
                           self.config.get("Text", "cmd_identifier"))
        self.protected_text = self.header
        self.commandText = Builder.load_file("res/sira.kv")
        self._on_url(self.config.get("Jira", "url"))
        self._on_timeout(self.config.get("Jira", "timeout"))
        self._on_protocol(self.config.get("Jira", "protocol"))
        return self.commandText

    @overrides(App)
    def build_config(self, config: ConfigParser) -> None:
        """Public function builds self.config from src/sira.ini if it exists,
        otherwise sets self.config with default values and writes in
        src/sira.ini.

        [ensures]:  self.config is not None
                    [self.config has all attributes in its source file]
                    [At least, the following attributes exist:
                        ("Text", "user_name"),
                        ("Text", "cmd_identifier"),
                        ("Text", "font_size"),
                        ("Text", "font_name"),
                        ("Jira", "url"),
                        ("Jira", "timeout"),
                        ("Jira", "protocol"),
                        ("Option", "space_completion"),
                        ("Option", "tab_completion"),
                        ("Option", "options_per_line"),
                        ("Result", "max_result)
                    ]
        """
        text = {
            "cmd_identifier": ">",
            "font_size": "14",
            "font_name": "Monaco",
            "username": ""
        }
        jira = {
            "url": "lnvusjira.lenovonet.lenovo.local",
            "timeout": "5",
            "protocol": "https"
        }
        option = {
            "space_completion": "1",
            "tab_completion": "1",
            "options_per_line": "7"
        }
        result = {
            "max_result": "10"
        }
        config.setdefaults("Text", text)
        config.setdefaults("Jira", jira)
        config.setdefaults("Option", option)
        config.setdefaults("Result", result)

    @overrides(App)
    def build_settings(self, settings: Settings) -> None:
        """Builds and adds custom setting pannels to original settings,
        called when the user open settings for the first time.

        [requires]: isinstance(self.config, kivy.config.Config)
                    [see [ensures] of build_config]
        """
        if not asserts(isinstance(self.config, ConfigParser),
                       "self.config is not initialized."):
            return
        settings.add_json_panel("Sira", self.config,
                                filename="res/sira.json")
        settings.add_json_panel("Jira", self.config,
                                filename="res/jira.json")

    @func_log
    @overrides(App)
    def on_config_change(self,
                         config: ConfigParser,
                         section: str,
                         key: str,
                         value: str) -> None:
        """Fires when configs change.

        [requires]: config = self.config
                    (for all config where config = self.config, ((section, key)
                        in self.config_func_dict.keys()))
        [calls]:    [corresponding functions in self.config_func_dict]
        """

        if config == self.config:
            if not asserts((section, key) in self.config_func_dict.keys(),
                           "({}, {}) is not a key pair in self.config_func_dict".format(section, key)):
                return
            self.config_func_dict[(section, key)](value)

    @overrides(App)
    def on_start(self) -> None:
        """TODO: both here and class doc
        """
        self.controller.on_start(self.username)

    @overrides(App)
    def on_stop(self) -> None:
        """Fires on successful exit.

        [ensures]:  self.commandText.password_cache = ""
        [calls]:    utils.write_memo_log
                    utils.glob_dic.tips.write_file
        """
        if self.commandText.password_mode:
            self.commandText.password_mode = False
        write_memo_log(self, self.commandText, glob_dic, glob_dic.tips)
        if self.username != "":
            glob_dic.tips.write_file(self.username)
        return None

    @overrides(App)
    def stop(self) -> (True, None):
        """Public function to exit the application.

        [calls]:    super(SiraApp, self).stop
                    on_stop
        """
        super(SiraApp, self).stop()
        return True, None

    def set_controller(self, controller: SiraController) -> None:
        """Public function to set self.controller to controller.

        [ensures]:  self.controller = controller
        """
        self.controller = controller
