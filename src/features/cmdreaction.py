import kivy.properties as kp
from kivy.app import App

from advancedtextinput import AdvancedTextInput
from utils import asserts, func_log


class CommandReactive(object):

    """TODO

    Instance Variables:
        Class-scope Variables:
            header -- kivy.properties.StringPorperty (default None)
            info -- kivy.properties.ListProperty (default [])
            protected_text -- kivy.properties.StringPorperty (default None)

        Method-established Variables:
            (initialized by subclasses)
            commandText -- advancedtextinput.AdvancedTextInput (default None)
            controller -- controller.SiraController
    
    Public Methods:
        Overrided from object:
            __init__(self) -> None

        Original:
            on_clear(self) -> None
            set_command_mode(self, bool) -> None
            set_pwd_mode(self) -> None

    Private Methods:
        _on_command(self, advancedtextinput.AdvancedTextInput) -> None
        _stop_interaction(self, advancedtextinput.AdvancedTextInput) -> None

    Events:
        `on_info`
            Fired when info is changed. This will print everything, one element
            per line, in the {@code info} to the command window and move the
            cursor to the end of text.

    Property Driven Methods:
        on_info(self, advancedtextinput.AdvancedTextInput, list) -> None
    
    Conventions:
        {
            TODO
        }
    """

    header = kp.StringProperty(None)
    """Kivy string property to store the command header.

    [convention #1]: {
        (self.header = (self.username
            + self.config.get("Text", "cmd_identifier")))           #1.1
        }
    
    [callback]: None
    """

    info = kp.ListProperty([])
    """Kivy list property to store buffered results. When info changes,
    function on_info will be dispatched, and self.commandText will print
    every element in info on seperate lines.

    [convention #2]: {
            (for line in self.info: isinstance(line, str))          #2.1
        &&  (self.info = []) after self.on_info                     #2.2
    }

    [callback]: on_info
    """

    protected_text = kp.StringProperty(None)
    """Kivy string property to store the protected_text of the current
    command line.

    [convention #3]: {
        (self.protected_text = self.commandText._lines[instance.last_row])         #3.1
    }

    [callback]: self.commandText.protected_len (from res/sira.kv)
    """

    ###
    commandText = None
    controller = None

    def __init__(self):
        """TODO
        """
        pass

    def on_clear(self) -> None:
        """Public function to clear the screen. This methods essentially
        scrolls all historical texts above the window.
        """
        instance = self.commandText
        instance.scroll_y = (instance.last_row) * instance.line_height

    def set_command_mode(self, value: bool) -> None:
        """Public function to set self.commandText.command_mode to value.

        [ensures]:  self.commandText.command_mode = value
        """
        self.commandText.command_mode = value

    def set_pwd_mode(self) -> None:
        """Public function to set self.commandText.password_mode to True.

        [ensures]:  self.commandText.password_mode = True
        """
        self.commandText.password_mode = True

    @func_log
    def _on_command(self, instance: AdvancedTextInput) -> bool:
        """"Privated function fired when self.commandText.on_text_validate is
        called, in other words, when users hit the 'enter' key. This property
        is established by res/sira.kv.

        [ensures]:  instance.last_row > 0
                    instance.protected_len <= len(instance._lines[instance.last_row])
                    instance.password_mode = False
                    instance.history_stack.traversal =
                        instance.history_stack.traversal_dummy
        [calls]:    instance.history_stack.reset_traversal
                    self.controller.processInput
        """
        string = instance._lines[instance.last_row][instance.protected_len:]
        if instance.password_mode:
            string = instance.password_cache
            instance.password_mode = False
        elif instance.command_mode and string != "":
            instance.history_stack.push(string)
        instance.history_stack.reset_traversal()
        self.controller.processInput(string)
        instance.on_cursor(instance, instance.cursor)
        return True

    def _stop_interaction(self, instance: AdvancedTextInput) -> None:
        """Private function to interrupt interactive mode. This function will
        be fired when the user hit control-C.

        [ensures]:  instance.password_mode = False
                    instance.command_mode = True
        [calls]:    self.controller.closeinteractive
        """
        if not instance.command_mode:
            if instance.completion_mode:
                if "_stop_completion" not in dir(self):
                    self._stop_completion = lambda x: x
                self._stop_completion(instance)
            self.controller.closeinteractive()
            instance.password_mode = False
            instance.command_mode = True

    @func_log
    def on_info(self, instance: App, info: list) -> None:
        """Property driven function, fired when info is changed. This function
        automatically prints all elements in info on seperate lines in
        this.commandText.

        [requires]: [convention #2.1]
        [ensures]:  [convention #2.2]
                    (self.commandText.text = $self.commandText.text + '\n' 
                                             + \n'.join(info))
        [calls]:    on_info (recursively once)
        """
        if self.info == []:
            return
        obj = self.commandText
        for s in info:
            if not asserts(isinstance(s, str),
                           "(for line in self.info: isinstance(line, str))."):
                return
        obj.do_cursor_movement("cursor_end", control=True)
        self.protected_text = info[-1]
        for s in info:
            obj.insert_text("\n" + str(s))
        obj.last_row = len(obj._lines) - 1
        obj.last_row_start = len(obj.text) - len(obj._lines[obj.last_row])
        obj.on_cursor(obj, obj.cursor)
        self.info = []
