import kivy.properties as kp
from kivy.app import App

from advancedtextinput import AdvancedTextInput
from utils import asserts, func_log


class Completable(object):

    """Abstract class implemeted compeletion features. This class must be
    extended by a subclass extending kivy.app.App; in other words, its subclass
    must initialize self.commandText as an instance of
    advancedtextinput.AdvancedTextInput and self.controller as
    an instance of controller.SiraController before calling any other functions
    in this abstract class. This class can work as an independent and subscrible
    behavioral class.

    Instance Variables:
        Class-scope Variables:
            completion_start -- kivy.properties.NumericProperty (default 0)
            from_space -- kivy.properties.BooleanProperty (default True)
            option -- kivy.properties.ListProperty (default [])
            options_per_line -- kivy.properties.NumericProperty (default 7)
            page_index -- kivy.properties.NumericProperty (default 0)
            start_indices -- kivy.properties.ListProperty (default [])
            tab_index -- kp.NumericProperty (default -1)

        Function-established Variables:
            (initialized by subclasses)
            commandText -- advancedtextinput.AdvancedTextInput (default None)
            controller -- controller.SiraController

    Public Functions:
        Overrided from object:
            __init__(self) -> None

    Private Functions:
        _clear_options(self, advancedtextinput.AdvancedTextInput) -> None
        _display_options(self,
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

    Property Driven Functions:
        on_option(self, advancedtextinput.AdvancedTextInput, list) -> None

    Conventions:
        {
            [(self.commandText.last_row = $self.commandText.last_row)
                after all function calls in this feature]           #0.1
            [(self.commandText.last_row_start
                = $self.commandText.last_row_start)
                after all function calls this feature]              #0.2
        }
    """

    completion_start = kp.NumericProperty(0)
    """Kivy numeric property to store the start index of the completion part.
    """

    from_space = kp.BooleanProperty(True)
    """Kivy boolean property to distinguish space and tab.

    [convention #1]: {
            (self.from_space = True) iff [entered completion mode from space]
        &&  (self.from_space = False) iff [entered completion mode from tab]
                                                                    #1.1
    }
    """

    option = kp.ListProperty([])
    """Kivy list property to store all options. When option changes,
    function on_option will be dispatched, and self.commandText will display
    the first self.options_per_line options below self.commandText.last_row.

    [convention #2]: {
            (for opt in self.option: isinstance(opt, str))          #2.1
    }

    [callback]: on_option
    """

    options_per_line = kp.NumericProperty(7)
    """Kivy numeric property to store the maximum options displayed per line
    (default 7)
    """

    page_index = kp.NumericProperty(0)
    """Kivy numeric property to store the page number in all options.
    """

    start_indices = kp.ListProperty([])
    """Kivy numeric property to store all text indicies of displayed options.

    [convention #3]: {
            (for i in range(len(start_indices)): start_indices[i] == [the start
            text indcies of all displayed options][i])              #3.1
    }
    """

    tab_index = kp.NumericProperty(-1)
    """Kivy numeric property to store current index in displayed options.
    """

    controller = None
    """Dummy reference to eliminate syntax error. This instance variable should
    be initialized by subclasses before calling any other functions in
    Completable.
    """

    commandText = None
    """Dummy reference to eliminate syntax error. This instance variable should
    be initialized by subclasses before calling any other functions in
    Completable.
    """

    def __init__(self):
        """Constructor of Completable. This function should not be called except
        by its subclasses' constructors.
        """
        pass

    def _clear_options(self, instance: AdvancedTextInput) -> None:
        """Private function to clear all displayed options in self.commandText.

        [requires]: instance.completion_mode
        [ensures]:  len(self.commandText._lines) = self.commandText.last_row
                    [erase all text below self.commandText.last_row]
        """
        if not asserts(instance.completion_mode, "Not in completion mode"):
            return

        instance.cancel_selection()
        start = instance.text.rindex('\n')
        end = len(instance.text)
        instance.select_text(start, end)
        instance.delete_selection()

    @func_log
    def _display_options(self,
                         instance: AdvancedTextInput,
                         behavior: str,
                         option: list) -> bool:
        """Private function to display options under self.commandText.last_row.
        This function is fired when self.commandText.on_next_options or
        self.commandText.on_prev_options is called. Essentially, this function
        will display options based on behavior and calculate start indices of
        displayed options. According to behavior, there are three scenarios:
            [Scenario 1]: When behavior == "init", the function will display the
                first n (n = max(self.options_per_line, [the number of remaining
                options])) options;
            [Scenario 2]: When behavior == "next", the function will display the
                next n options;
            [Scenario 3]: When behavior == "prev", the function will display the
                previous n options.

        [requires]: instance.completion_mode
        [ensures]:  [display n options below self.commandText.last_row]
                    self.tab_index = -1
                    [convention #3.1]
        """
        if not asserts(instance.completion_mode, "Not in completion mode"):
            return True

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
        instance.insert_text(
            "\n" + " ".join(option[self.page_index:end_index]))
        instance.cursor = cursor
        # calc start indices of displayed options
        index = 0
        self.start_indices.clear()
        for s in option[self.page_index:end_index]:
            self.start_indices.append(index)
            index += len(s) + 1
        return True

    def _on_reduce_option(self, instance: AdvancedTextInput) -> bool:
        """Private function to reduce options based on user input. This function
        is fired when self.commandText.on_reduce_option is called.

        [requires]: instance.completion_mode
        [ensures]:  self.option = [opt for all opt in $self.option if
                    opt.lower().startswith(
                        instance.text[self.completion_start:end].lower()
                    )]
        [calls]:    self._stop_completion
        """
        if not asserts(instance.completion_mode, "Not in completion mode"):
            return True

        copy = list()
        instance.do_cursor_movement("cursor_end", control=False)
        end = instance.cursor_index(instance.cursor)
        word_truc = instance.text[self.completion_start:end]
        copy = [opt for opt in self.option
                if opt.lower().startswith(word_truc.lower())]
        self._stop_completion(instance)
        self.option = copy

    def _on_space(self, instance: AdvancedTextInput) -> bool:
        """Private function to start completion mode by entering from space.
        This function is fired when self.commandText._on_space is called.

        [ensures]:  (when this is the first space after a user-input word)
                    self.from_space
                    (otherwise, do nothing)
        [calls]:    (when this is the first space after a user-input word)
                    self.controller.auto_complete
                    (otherwise, do nothing)
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
        """Private function to select next option. This function is fired when
        self.commandText.on_left_option or self.commandText.on_right_option is
        called.

        [requires]: instance.completion_mode
        [calls]:    self._select_next_option
        """
        if not asserts(instance.completion_mode, "Not in completion mode"):
            return True

        self._select_next_option(direction)

    @func_log
    def _on_tab(self, instance: AdvancedTextInput) -> bool:
        """Privated function fired when self.commandText.on_tab is called, in
        other words, when users hit the 'tab' key. According to
        instance.completion_mode, there are two scenarios:
            [Scenario 1]: When instance.completion_mode == True, select
                next option;
            [Scenario 2]: When instance.completion_mode == True,
                call controller.auto_completion

        [ensures]:  (when not instance.completion_mode)
                    not self.from_space
        [calls]:    (when instance.completion_mode)
                    self._select_next_option
                    (otherwise)
                    self.controller.auto_complete
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
        """Private function to replace auto-completion text and selection next
        avaliable option. According to direction, there are three scenarios:
            [Scenario 1]: When direction == "tab", the function will erase any
            text from self.completion_start to the end of
            self.commandText.last_row, and replace it with next option
            avaliable. If the current option is the last displayed options, the
            first option will be print and selected.
            [Scenario 2]: When direction == "left", the function will act like
            Scenario 1 except printing and selecting the previous avaliable
            option. If there does not exist any previous options, this function
            will do nothing.
            [Scenario 3]: When direction == "right". the function will act
            exactly like Scenario 1, except do nothing when there does not exist
            any options avaliable.

        [requires]: self.commandText.completion_mode
        [ensures]:  [function_doc]
                    self.tab_index in range(self.options_per_line)
        """
        instance = self.commandText
        tab_index = self.tab_index
        # update tab_index according to direction
        if direction == "tab":
            tab_index = tab_index + 1\
                if tab_index < len(self.start_indices) - 1\
                else 0
        elif direction == "left":
            tab_index = max(tab_index - 1, 0)
        elif direction == "right":
            tab_index = min(tab_index + 1, len(self.start_indices) - 1)
        # do nothing if tab_index does not changed
        if tab_index != self.tab_index:
            # delete and insert next option
            instance.cancel_selection()
            start = self.completion_start
            end = instance.last_row_start + \
                len(instance._lines[instance.last_row])
            instance.select_text(start, end)
            instance.delete_selection()
            instance.do_cursor_movement("cursor_end", control=True)
            instance.insert_text(self.option[self.page_index + tab_index])
            # select next option
            last_char_return = instance.text.rindex("\n")
            start = last_char_return + self.start_indices[tab_index] + 1
            end = start + len(self.option[self.page_index + tab_index])
            instance.select_text(start, end)
            # update self.tab_index
            self.tab_index = tab_index

    def _stop_completion(self, instance: AdvancedTextInput) -> None:
        """Private function to stop completion mode.

        [requires]: instance.completion_mode
        [ensures]:  not instance.completion_mode
                    self.tab_index = -1
                    self.option = []
                    self.start_indices = []
        [calls]:    self._clear_options
        """
        if not asserts(instance.completion_mode, "Not in completion mode"):
            return
        self._clear_options(instance)
        instance.completion_mode = False
        self.tab_index = -1
        self.option = []
        self.start_indices = []

    @func_log
    def on_option(self, instance: App, option: list) -> None:
        """Property driven function, fired when option is changed. This function
        will initialize completion mode.

        [ensures]:  completion_mode = option != []
                    completion_start = [where the completion starts]
        [calls]:    self._display_options
                    self._select_next_option
        """
        obj = self.commandText
        if option == []:
            obj.completion_mode = False
            return
        obj.completion_mode = True
        self._display_options(obj, "init", option)
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
