import kivy.properties as kp
from kivy.app import App

from advancedtextinput import AdvancedTextInput
from utils import func_log


class Completable(object):

    """TODO

    Instance Variables:
        Class-scope Variables:
            completion_start -- kivy.properties.NumericProperty (default 0)
            from_space -- kivy.properties.BooleanProperty (default True)
            option -- kivy.properties.ListProperty (default [])
            options_per_line -- kivy.properties.NumericProperty (default 7)
            page_index -- kivy.properties.NumericProperty (default 0)
            start_indices -- kivy.properties.ListProperty (default [])
            tab_index -- kp.NumericProperty (default -1)

        Method-established Variables:
            (initialized by subclasses)
            commandText -- advancedtextinput.AdvancedTextInput (default None)
            controller -- controller.SiraController

    Public Methods:
        Overrided from object:
            __init__(self) -> None

    Private Methods:
        _clear_options(self, advancedtextinput.AdvancedTextInput) -> None
        _on_display_options(self,
                            advancedtextinput.AdvancedTextInput,
                            str,
                            list) -> bool
        _on_reduce_option(self, advancedtextinput.AdvancedTextInput) -> bool
        _on_space(self, advancedtextinput.AdvancedTextInput) -> bool
        _on_switch_option(self,
                          advancedtextinput.AdvancedTextInput,
                          str) -> bool
        _on_tab(self, advancedtextinput.AdvancedTextInput) -> None
        _select_next_option(self, str) -> None
        _stop_completion(self, advancedtextinput.AdvancedTextInput) -> None
    
    Events:
        `on_option`
            Fired when option is changed. This will print everything, one
            element per line, in the {@code info} to the command window without
            moving the cursor.
    
    Property Driven Methods:
        on_option(self, advancedtextinput.AdvancedTextInput, list) -> None

    Conventions:
        {
            TODO
        }
    """

    completion_start = kp.NumericProperty(0)
    """TODO: here
    """
    
    from_space = kp.BooleanProperty(True)
    """TODO: here
    """

    option = kp.ListProperty([])
    """TODO
    """

    options_per_line = kp.NumericProperty(7)
    """TODO: both here
    """

    page_index = kp.NumericProperty(0)
    """TODO: both here
    """
    
    start_indices = kp.ListProperty([])
    """TODO: both here
    """

    tab_index = kp.NumericProperty(-1)
    """TODO: both here
    """

    ###
    controller = None
    commandText = None

    def __init__(self):
        """TODO
        """
        pass

    def _clear_options(self, instance: AdvancedTextInput) -> None:
        """TODO: both here
        """
        instance.cancel_selection()
        start = instance.text.rindex('\n')
        end = len(instance.text)
        instance.select_text(start, end)
        instance.delete_selection()

    @func_log
    def _on_display_options(self,
                            instance: AdvancedTextInput,
                            behavior: str,
                            option: list) -> bool:
        """TODO: here
        """
        # display options based on behavior
        instance.do_cursor_movement("cursor_end", control=True)
        cursor = instance.cursor
        if behavior == "init":
            self.page_index = 0
        else:
            self._clear_options(instance)
            self.tab_index = -1
            next_index = self.page_index + self.options_per_line\
                         if behavior == "next"\
                         else self.page_index - self.options_per_line
            self.page_index = max(0, next_index)\
                              if next_index < len(option)\
                              else self.page_index
        end_index = self.page_index + self.options_per_line\
                    if self.page_index + self.options_per_line <= len(option)\
                    else len(option)
        instance.insert_text("\n" + " ".join(option[self.page_index:end_index]))
        instance.cursor = cursor
        # calc start indices of displayed options
        index = 0
        self.start_indices.clear()
        for s in option[self.page_index:end_index]:
            self.start_indices.append(index)
            index += len(s) + 1
        return True

    def _on_reduce_option(self, instance: AdvancedTextInput) -> bool:
        """TODO: both here
        """
        copy = list()
        instance.do_cursor_movement("cursor_end", control=False)
        end = instance.cursor_index(instance.cursor)
        word_truc = instance.text[self.completion_start:end]
        for s in self.option:
            if s.lower().startswith(word_truc.lower()):
                copy.append(s)
        self._stop_completion(instance)
        self.option = copy

    @func_log
    def _on_space(self, instance: AdvancedTextInput) -> bool:
        """TODO: both here
        """
        if instance.completion_mode:
            self._stop_completion(instance)
        c_index = instance.cursor_index(instance.cursor) - 1
        if instance.last_row_start + instance.protected_len != c_index\
                and instance.text[c_index - 1] != " ":
            string = instance._lines[instance.last_row][instance.protected_len:]
            self.from_space = True
            self.controller.auto_complete(string)
        return True

    def _on_switch_option(self,
                          instance: AdvancedTextInput,
                          direction: str) -> bool:
        """TODO: here
        """
        self._select_next_option(direction)

    @func_log
    def _on_tab(self, instance: AdvancedTextInput) -> bool:
        """TODO
        """
        if instance.password_mode:
            return True
        if instance.completion_mode:
            self._select_next_option("tab")
        else:
            string = instance._lines[instance.last_row][instance.protected_len:]
            self.from_space = False
            self.controller.auto_complete(string)
        return True

    def _select_next_option(self, direction: str) -> None:
        """TODO
        """
        instance = self.commandText
        # update self.tab_index according to direction
        if direction == "tab":
            self.tab_index = self.tab_index + 1\
                             if self.tab_index < len(self.start_indices) - 1\
                             else 0
        elif direction == "left":
            self.tab_index = self.tab_index - 1\
                             if self.tab_index > 0\
                             else 0
        elif direction == "right":
            self.tab_index = self.tab_index + 1\
                             if self.tab_index < len(self.start_indices) - 1\
                             else len(self.start_indices) - 1
        # delete and insert next option
        instance.cancel_selection()
        start = self.completion_start
        end = instance.last_row_start + len(instance._lines[instance.last_row])
        instance.select_text(start, end)
        instance.delete_selection()
        instance.do_cursor_movement("cursor_end", control=True)
        instance.insert_text(self.option[self.page_index + self.tab_index])
        # select next option
        last_char_return = instance.text.rindex("\n")
        start = last_char_return + self.start_indices[self.tab_index] + 1
        end = start + len(self.option[self.page_index + self.tab_index])
        instance.select_text(start, end)

    def _stop_completion(self, instance: AdvancedTextInput) -> None:
        """TODO: here
        """
        self._clear_options(instance)
        instance.completion_mode = False
        self.tab_index = -1
        self.option = []
        self.start_indices = []

    @func_log
    def on_option(self, instance: App, option: list) -> None:
        """TODO
        """
        obj = self.commandText
        if option == []:
            obj.completion_mode = False
            return
        obj.completion_mode = True
        self._on_display_options(obj, "init", option)
        # calc the start index of the completion part
        search_start = obj.last_row_start + obj.protected_len
        search_end = obj.last_row_start\
                     + len(obj._lines[obj.last_row])
        try:
            self.completion_start = obj.text.rindex(" ",
                                                    search_start,
                                                    search_end) + 1
        except ValueError:
            self.completion_start = search_start
        if not self.from_space:
            self._select_next_option("tab")
