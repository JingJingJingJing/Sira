import sys
from stack import CommandStack

import kivy.properties as kp
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.utils import platform


class AdvancedTextInput(TextInput):

    # Additional instance variables:

    history_stack = kp.ObjectProperty(None)

    password_mode = kp.BooleanProperty(False)

    password_cache = kp.StringProperty("")

    protected_len = kp.NumericProperty(1)

    command_mode = kp.BooleanProperty(True)

    __events__ = ('on_text_validate', 'on_double_tap', 'on_triple_tap',
                  'on_quad_touch', 'on_tab')

    def __init__(self, **kwargs):
        super(AdvancedTextInput, self).__init__(**kwargs)
        self.history_stack = CommandStack()

    def _key_down(self, key, repeat=False):
        displayed_str, internal_str, internal_action, scale = key
        if internal_action is None:
            if self._selection:
                self.delete_selection()
            self.insert_text(displayed_str)
        elif internal_action in ('shift', 'shift_L', 'shift_R'):
            if not self._selection:
                self._selection_from = self._selection_to = self.cursor_index()
                self._selection = True
            self._selection_finished = False
        elif internal_action == 'ctrl_L':
            self._ctrl_l = True
        elif internal_action == 'ctrl_R':
            self._ctrl_r = True
        elif internal_action == 'alt_L':
            self._alt_l = True
        elif internal_action == 'alt_R':
            self._alt_r = True
        elif internal_action.startswith('cursor_'):
            cc, cr = self.cursor
            self.do_cursor_movement(internal_action,
                                    self._ctrl_l or self._ctrl_r,
                                    self._alt_l or self._alt_r)
            if self._selection and not self._selection_finished:
                self._selection_to = self.cursor_index()
                self._update_selection()
            else:
                self.cancel_selection()
        elif self._selection and internal_action in ('del', 'backspace'):
            self.delete_selection()
        elif internal_action == 'del':
            if self._get_cursor_col() != 0:
                # Move cursor one char to the right. If that was successful,
                # do a backspace (effectively deleting char right of cursor)
                cursor = self.cursor
                self.do_cursor_movement('cursor_right')
                if cursor != self.cursor:
                    self.do_backspace(mode='del')
        elif internal_action == 'backspace':
            if self.password_mode:
                self.password_cache = self.password_cache[:-1]
            if self._get_cursor_col() > self.protected_len:
                self.do_backspace()
        elif internal_action == 'enter':
            self.dispatch('on_text_validate')
        elif internal_action == 'escape':
            self.focus = False
        if internal_action != 'escape':
            # self._recalc_size()
            pass

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # Keycodes on OS X:
        ctrl, cmd = 64, 1024
        key, key_str = keycode
        win = EventLoop.window

        # cache the result
        _is_osx = sys.platform == 'darwin'

        # This allows *either* ctrl *or* cmd, but not both.
        is_shortcut = (modifiers == ['ctrl'] or (
            _is_osx and modifiers == ['meta']))
        is_interesting_key = key in (list(self.interesting_keys.keys()) + [27])

        if not self.write_tab and super(AdvancedTextInput,
                                        self).keyboard_on_key_down(window, keycode, text, modifiers):
            return True

        if not self._editable:
            # duplicated but faster testing for non-editable keys
            if text and not is_interesting_key:
                if is_shortcut and key == ord('c'):
                    self.copy()
            elif key == 27:
                self.focus = False
            return True

        if text and not is_interesting_key:

            self._hide_handles(win)
            self._hide_cut_copy_paste(win)
            win.remove_widget(self._handle_middle)

            # check for command modes
            # we use \x01INFO\x02 to get info from IME on mobiles
            # pygame seems to pass \x01 as the unicode for ctrl+a
            # checking for modifiers ensures conflict resolution.

            first_char = ord(text[0])
            if not modifiers and first_char == 1:
                self._command_mode = True
                self._command = ''
            if not modifiers and first_char == 2:
                self._command_mode = False
                self._command = self._command[1:]

            if self._command_mode:
                self._command += text
                return

            _command = self._command
            if _command and first_char == 2:
                from_undo = True
                _command, data = _command.split(':')
                self._command = ''
                if self._selection:
                    self.delete_selection()
                if _command == 'DEL':
                    count = int(data)
                    if not count:
                        self.delete_selection(from_undo=True)
                    end = self.cursor_index()
                    self._selection_from = max(end - count, 0)
                    self._selection_to = end
                    self._selection = True
                    self.delete_selection(from_undo=True)
                    return
                elif _command == 'INSERT':
                    self.insert_text(data, from_undo)
                elif _command == 'INSERTN':
                    from_undo = False
                    self.insert_text(data, from_undo)
                elif _command == 'SELWORD':
                    self.dispatch('on_double_tap')
                elif _command == 'SEL':
                    if data == '0':
                        Clock.schedule_once(lambda dt: self.cancel_selection())
                elif _command == 'CURCOL':
                    self.cursor = int(data), self.cursor_row
                return

            if is_shortcut:
                if key == ord('x'):  # cut selection
                    self._cut(self.selection_text)
                elif key == ord('c'):  # copy selection
                    self.copy()
                elif key == ord('v'):  # paste selection
                    self.paste()
                elif key == ord('a'):  # select all
                    self.select_all()
                elif key == ord('z'):  # undo
                    self.do_undo()
                elif key == ord('r'):  # redo
                    self.do_redo()
            else:
                if EventLoop.window.__class__.__module__ == \
                        'kivy.core.window.window_sdl2':
                    if not (text == ' ' and platform == 'android'):
                        return
                if self._selection:
                    self.delete_selection()
                self.insert_text(text)
            # self._recalc_size()
            return

        if is_interesting_key:
            self._hide_cut_copy_paste(win)
            self._hide_handles(win)

        if key == 27:  # escape
            self.focus = False
            return True
        elif key == 9:  # tab
            if self.command_mode:
                self.dispatch('on_tab')
            else:
                self.insert_text(u"\t")
            return True

        k = self.interesting_keys.get(key)
        if k:
            key = (None, None, k, 1)
            self._key_down(key)

    def delete_selection(self, from_undo=False):
        '''Delete the current text selection (if any).
        '''
        if self.readonly:
            return
        # changes start from here

        # If the selection includes protected parts, cancel selection.
        index = -1 if len(self._lines) < 2 else self.text.rindex('\n')

        ### when user selected both protected texts and the command
        if self.selection_from < index + self.protected_len + 1:
            self.cancel_selection()
            self.do_cursor_movement("cursor_end")
            if self._get_cursor_col() > self.protected_len:
                self.do_backspace()
            return

        # changes start from here
        self._hide_handles(EventLoop.window)
        scrl_x = self.scroll_x
        scrl_y = self.scroll_y
        cc, cr = self.cursor
        if not self._selection:
            return
        v = self._get_text(encode=False)
        a, b = self._selection_from, self._selection_to
        if a > b:
            a, b = b, a
        self.cursor = cursor = self.get_cursor_from_index(a)
        start = cursor
        finish = self.get_cursor_from_index(b)
        cur_line = self._lines[start[1]][:start[0]] +\
            self._lines[finish[1]][finish[0]:]
        lines, lineflags = self._split_smart(cur_line)
        len_lines = len(lines)
        if start[1] == finish[1]:
            self._set_line_text(start[1], cur_line)
        else:
            self._refresh_text_from_property('del', start[1], finish[1], lines,
                                             lineflags, len_lines)
        self.scroll_x = scrl_x
        self.scroll_y = scrl_y
        # handle undo and redo for delete selection
        self._set_unredo_delsel(a, b, v[a:b], from_undo)
        self.cancel_selection()

    def do_cursor_movement(self, action, control=False, alt=False):
        '''Move the cursor relative to it's current position.
        Action can be one of :

            - cursor_left: move the cursor to the left
            - cursor_right: move the cursor to the right
            - cursor_up: display and select the previous command
            - cursor_down: display and select the next command
            - cursor_home: move the cursor at the start of the current line
            - cursor_end: move the cursor at the end of current line
            - cursor_pgup: move one "page" before
            - cursor_pgdown: move one "page" after

        In addition, the behavior of certain actions can be modified:

            - control + cursor_left: move the cursor one word to the left
            - control + cursor_right: move the cursor one word to the right
            - control + cursor_up: scroll up one line
            - control + cursor_down: scroll down one line
            - control + cursor_home: go to beginning of text
            - control + cursor_end: go to end of text
            - alt + cursor_up: shift line(s) up
            - alt + cursor_down: shift line(s) down

        .. versionchanged:: 1.9.1

        '''
        if not self._lines:
            return
        pgmove_speed = int(self.height /
                           (self.line_height + self.line_spacing) - 1)
        col, row = self.cursor
        if action == 'cursor_up':
            # enable history search when on command_mode
            if self.command_mode:
                self.history_stack.step_back()
                col, row = self.display_command(self.history_stack.peak())
        elif action == 'cursor_down':
            # enable history search when on command_mode
            if self.command_mode:
                self.history_stack.step_forward()
                col, row = self.display_command(self.history_stack.peak())
        elif action == 'cursor_left':
            if not self.password and control:
                col, row = self._move_cursor_word_left()
            elif self._get_cursor_col() > self.protected_len:
                col, row = col - 1, row
        elif action == 'cursor_right':
            if not self.password and control:
                col, row = self._move_cursor_word_right()
            else:
                if col == len(self._lines[row]):
                    if row < len(self._lines) - 1:
                        col = 0
                        row += 1
                else:
                    col, row = col + 1, row
        elif action == 'cursor_home':
            col = 0
            if control:
                row = 0
        elif action == 'cursor_end':
            if control:
                row = len(self._lines) - 1
            col = len(self._lines[row])
        elif action == 'cursor_pgup':
            row = max(0, row - pgmove_speed)
            col = min(len(self._lines[row]), col)
        elif action == 'cursor_pgdown':
            row = min(row + pgmove_speed, len(self._lines) - 1)
            col = min(len(self._lines[row]), col)
        self.cursor = (col, row)

    def display_command(self, text):
        self.cancel_selection()
        index = -1 if len(self._lines) < 2 else self.text.rindex('\n')
        start = index + self.protected_len + 1
        end = len(self.text)
        self.select_text(start, end)
        self.delete_selection()
        self.insert_text(text)
        col, row = self.cursor
        return len(self._lines[row]), row

    def on_cursor(self, instance, value):
        # When the cursor is moved, reset cursor blinking to keep it showing,
        # and update all the graphics.
        if self.focus:
            self._trigger_cursor_reset()
            if self._get_cursor_row() != len(self._lines) - 1 or \
                    self._get_cursor_col() < self.protected_len:
                self._editable = False
            else:
                self._editable = True
        self._trigger_update_graphics()

    def keyboard_on_textinput(self, window, text):
        if self._editable:
            if self._selection:
                self.do_cursor_movement("cursor_end")
                self.cancel_selection()
            if self.password_mode:
                self.password_cache += text
            else:
                self.insert_text(text, False)
        return

    def select_all(self):
        ''' Select all of the text displayed in this TextInput.

        .. versionadded:: 1.4.0
        '''
        self.select_text(0, len(self.text))

    # custom functions:

    def on_password_mode(self, instance, value):
        if not value:
            self.password_cache = ''

    def on_tab(self):
        pass
