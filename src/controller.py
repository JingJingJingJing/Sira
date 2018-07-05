import re
import threading
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher

import issueOps
import login
import query
from prompter import Prompter
from utils import Super401, func_log, glob_dic


class SiraController():
    """The controller class which can handle input command and pass the corresponding function result

    public methods:
        processInput(self, instance, string) -> None
        closeinteractive -> None

    *view* is the UI object.
    *separater* is a regular expression to split command.
    *tree* holds the xml DOM struture.
    *position* holds the current node of xml
    *args* holds parsed parameters
    *no_need_login" contains the commands that user can call without login

    """
    normal_cursor = ">"
    no_need_login = ["sira", "login", "exit", "clear"]

    def __init__(self, view):
        self.view = view
        self.separater = re.compile("\\s+")  # command separater
        self.args = []  # hold the args of command
        self.interactive = False
        self.tree = ET.parse("res/glossary.xml").getroot()
        self.position = self.tree  # the current position of tree
        self.prompter = Prompter()
        self.tp = {}
        self.updateMode = False
        self.updateDepth = 0
        self.updateIndex = 0
        self.updateField = ['', '', '', '', '', '', '', '', '']
        self.updateIndexes = []
        self.updateIssue = ''

    def on_start(self, username):
        login.tryload(username)

    def processInput(self, string):
        """According to the xml DOM structure, parser the input from UI, exec function and display the result

        *string* is the command from UI

        """

        if self.updateMode and self.interactive:
            self.view.commandText.readonly = True
            threading.Thread(
                target=self._update_special, args=(None, string)).start()
        else:
            if not self.interactive:
                ''' if it is not interactive mode '''
                update = re.compile(r'\Asira update(\s(\w*-\d*\S*)*)*$')

                if update.search(string) is not None:
                    ''' if it is sira update commond '''
                    if not self.view.username:
                        self.view.info = ['Please Login First!']
                        self.view.print_header()
                        return
                    issue = re.compile(r'\w*-\d*\S*')
                    if issue.search(string) is not None:
                        ''' if issue is provided '''
                        self.view.commandText.readonly = True
                        thr = threading.Thread(
                            target=self._display_wrapper,
                            args=(None, string.split(' ')[2]))
                        thr.start()
                        return

                    else:
                        ''' If issue is not provided '''
                        self.updateDepth = 1
                        self.view.set_command_mode(False)
                        self.view.info = ["Please Enter Issue's Key: "]
                        self.interactive = True
                        self.updateMode = True
                        return
            self._cal(string)

        # try:
        #     self._cal(string)
        # except Exception as err:
        #     mylog.error(err)
        #     self._sendinfo("error while processing")

    def closeinteractive(self):
        """Close the interactive mode by clear cache and display "interactive mode closed"

        This function only work in interactive mode.

        """
        if (self.position is None or self.position == self.tree):
            pass
        self._quit_updateMode('', True)
        self._clearcache()
        self.view.set_command_mode(True)
        self.view.commandText.readonly = False
        self.view.info = ["interactive mode closed"]
        self.view.print_header()

    def _cal(self, command):
        # pass when command is empty in non-interactive mode
        if len(command) <= 0:
            if self.position == self.tree:
                self.view.print_header()
                return

        tokens = self.separater.split(command.strip())
        for i, token in enumerate(tokens):
            pre_position = self.position
            for child in self.position.getchildren():
                # 如果在keyword里找到func
                if child.tag == "keyword" and child.attrib['name'] == token:
                    # exclude keywords need to login
                    if (not self.view.username) and (
                            token not in self.no_need_login):
                        self._sendinfo("Please login first")
                        return
                    # exclude login keyword if have logged in
                    elif self.view.username and token == "login":
                        self._sendinfo("already logged in as " +
                                       self.view.username)
                        return
                    else:
                        self.position = child
                        break
                elif child.tag == "optional" or child.tag == "required":  # 如果child是optional或者required
                    # required field can't be empty
                    if child.tag == "required" and not token:  # 如果required field 没有填
                        return
                    if pre_position.tag != "keyword" and self.interactive and i != 0:  #
                        break
                    else:
                        self.position = child
                        self.tp[token] = self.position.attrib.get(
                            'name') if token not in self.tp.keys(
                        ) else self.tp[token]
                        self.args.append(token)
                    break
            # do not extend deep
            if pre_position == self.position:
                if pre_position.tag != "keyword" and self.args:
                    self._increpara(token)
                else:
                    keywords = [child.attrib['name']
                                for child in self.position.getchildren()]
                    self._on_error_command(token, keywords)
                    return
        # pass if has sub-node ,exec function if has't
        if self.position.find("./required") or self.position.find(
                "./optional"):
            # call function first if exist
            func = self.position.find("./function")
            if func is not None:
                if func.attrib['object']:
                    getattr(eval(func.attrib['object']), func.attrib['name'])()
                else:
                    getattr(self, func.attrib['name'])()
            # display intseractive text
            interactive = self.position.find("./interactive")
            self.interactive = True
            self.view.set_command_mode(False)
            self.view.info = [interactive.text
                              ] if interactive is not None else [""]

        elif self.position.find("./keyword"):  # 交互模式
            # display intseractive text
            interactive = self.position.find("./interactive")
            if interactive is not None:
                self.interactive = True
                self.view.set_command_mode(False)
                self.view.info = ["-"]
            else:
                self._sendinfo("error command")
        else:
            self.view.commandText.readonly = True
            functag = self.position.find("./function")
            if functag.attrib['multi-thread'] == 'True':
                threading.Thread(None, self._execfunc).start()
            else:
                if functag.attrib['name'] == "on_clear":
                    self.view.commandText.readonly = False
                    self.view.print_header()
                    self.view.on_clear()
                    self._clearcache()
                else:
                    self._execfunc()

    def _execfunc(self):
        """Call the function after parsing

        It will change the value of username which view holds if the function is login.
        Login function will pass 2 args contains status and result(str).

        """
        try:
            functag = self.position.find("./function")
            obj = functag.attrib['object']
            name = functag.attrib['name']
            if self.args:
                f, result = getattr(eval(obj), name)(self.args)
            else:
                f, result = getattr(eval(obj), name)()

            # set cursor value to username when login successd
            if name == "login" and f:
                self.view.username = self.args[0]
            elif (name == "login" and not f) or name == "logout":
                glob_dic.tips.write_file(self.view.username)
                glob_dic.tips.dic = dict()
                self.view.username = ""
            # result = result[1]
            # display result
            if f:
                for i in range(0, len(self.args)):
                    if self.tp.get(self.args[i]) == 'project':
                        glob_dic.tips.update_priority('project', self.args[i])
                    elif self.tp.get(self.args[i]) == 'sprint':
                        glob_dic.tips.update_priority('sprint', self.args[i])
                    elif self.tp.get(self.args[i]) == 'assignee':
                        glob_dic.tips.update_priority('assignee', self.args[i])

            self._sendinfo(result)

        except Super401 as autherr:
            self.view.username = ""
            login.logout()
            self._sendinfo(autherr.err)
        # except Exception as err:
        #     mylog.error(err)

    def _sendinfo(self, msg):
        self._clearcache()
        self.view.commandText.readonly = False
        self.view.set_command_mode(True)
        if msg:
            if isinstance(msg, str):
                msg = [msg]
            self.view.info = msg
        self.view.print_header()

    def _clearcache(self):
        self.position = self.tree
        self.interactive = False
        self.args.clear()
        self.tp = {}

    def _increpara(self, s):
        # if self.args:
        arg = self.args.pop()
        arg = arg + " " + s
        self.args.append(arg)
        self.tp[arg] = self.position.attrib.get(
            'name') if arg not in self.tp.keys() else self.tp[arg]
        # else:
        #     self.args.append(s)

    def auto_complete(self, command):
        if not self.updateMode:
            self.view.option = self.prompter.auto_complete(
                self.position, self.interactive, command)
        else:
            if self.updateDepth > 2:
                try:
                    lst = [
                        'status', 'issuetype', 'summary', 'reporter',
                        'priority', 'lable', 'description', 'assignee',
                        'sprint'
                    ]
                    info = []
                    for tips in glob_dic.tips.dic[lst[self.updateIndex]]:
                        if tips[1].startswith(command):
                            info.append(tips[1])
                    if info:
                        self.view.option = info
                except KeyError:
                    pass

    def _update_special(self, dum, s):
        lst = [
            'status', 'issuetype', 'summary', 'reporter', 'priority', 'lable',
            'description', 'assignee', 'sprint'
        ]
        x = s.split(' ')
        try:
            s = ' '.join(list(filter(list.remove(x, ''), x)))
        except ValueError:
            s = ' '.join(x)
        if self.updateDepth == 1:
            ''' user need to give an issue '''
            f, r = issueOps.issue_display_info(s)
            if f:
                self.updateIssue = s
            else:
                self._quit_updateMode(r)
                return
            self.view.commandText.readonly = False
            self.view.info = r

        elif self.updateDepth == 2:
            ''' user need to choose from 8 fields and enter numbers '''
            valid = re.compile(r'\A[1-9](,[1-9])*$')
            if not valid.search(s):
                self.view.commandText.readonly = False
                self.view.info = ['Please enter numbers separated by ",": ']
                return

            def decrease(e):
                return int(e) - 1

            try:
                self.updateIndexes = list(map(decrease, s.split(',')))
                if not len(self.updateIndexes):
                    self.view.commandText.readonly = False
                    return
                self.updateIndexes.sort(reverse=True)
                index = self.updateIndexes.pop()
                self.updateIndex = index
                self.view.commandText.readonly = False
                self.view.info = ['{}: '.format(lst[index])]

            except ValueError:
                self.view.commandText.readonly = False
                self.view.info = [
                    'Input not valid, please enter numbers between 1 to 8 and separate them by " "'
                ]
                return

        elif (self.updateDepth > 2) and (len(self.updateIndexes) > 0):
            ''' user start to update one by one '''
            if not s:
                self.view.commandText.readonly = False
                return
            self.updateField[self.updateIndex] = s

            index = self.updateIndexes.pop()

            def delete_element(e):
                if e != index:
                    return True
            output = lst[index]
            self.updateIndexes = list(
                filter(delete_element, self.updateIndexes))
            self.updateIndexes.sort(reverse=True)
            self.updateIndex = index
            self.view.commandText.readonly = False
            self.view.info = ['{}: '.format(output)]

        else:
            ''' the last updated field '''
            self.updateField[self.updateIndex] = s
            self._quit_updateMode(
                issueOps.issue_edit([self.updateIssue] + self.updateField)[1])
            return

        self.updateDepth += 1

    def _display_wrapper(self, dum, issue):
        f, r = issueOps.issue_display_info(issue)
        if f:
            ''' displayed the issue info successfully '''
            self.view.commandText.readonly = False
            self.updateIssue = issue
            self.view.set_command_mode(False)
            self.view.info = r
            self.updateDepth = 2
            self.interactive = True
            self.updateMode = True
            return

        else:
            ''' If the cmd is sira update but the given issue not found '''
            self._quit_updateMode(r)
            return

    def _quit_updateMode(self, msg, c=False):
        self.updateMode = False
        self.updateDepth = 0
        self.updateIndex = 0
        self.updateField = ['', '', '', '', '', '', '', '', '']
        self.updateIndexes = []
        self.updateIssue = ''
        if not c:
            self._sendinfo(msg)

    def _diff(self, string_1, string_2):
        sm = SequenceMatcher(None, string_1, string_2)
        return sm.ratio()

    def _on_error_command(self, token, keywords):
        choices = [
            c for c in keywords if self._diff(c, token) > 0.5]
        if choices:
            self._sendinfo(
                ["error command",
                    "Do you mean {}?".format(" or ".join(choices))])
        else:
            self._sendinfo("error command")