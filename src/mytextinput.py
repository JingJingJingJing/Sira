from kivy.uix.textinput import TextInput

class MyTextInput(TextInput):

    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)

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
            # Move cursor one char to the right. If that was successful,
            # do a backspace (effectively deleting char right of cursor)
            cursor = self.cursor
            self.do_cursor_movement('cursor_right')
            if cursor != self.cursor:
                self.do_backspace(mode='del')
        elif internal_action == 'backspace':
            self.do_backspace()
        elif internal_action == 'enter':
            self.dispatch('on_enter')
        elif internal_action == 'escape':
            self.focus = False
        if internal_action != 'escape':
            # self._recalc_size()
            pass