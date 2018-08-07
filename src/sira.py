import sys,keyring,msvcrt
import func
from keyring.backends import Windows
from argparse import Action, ArgumentParser, Namespace
from subprocess import run

from utils import print_err, exit_prog

keyword_dict = {
    "query": ["type", "mode", "limit", "order", "key"],
    "update": []
}


class Ignore(Action):
    def __init__(self, option_strings, **kwargs):
        super(Ignore, self).__init__(option_strings, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        pass


class Store_Const_and_Ignore(Ignore):
    def __init__(self, option_strings, **kwargs):
        super(Store_Const_and_Ignore, self).__init__(option_strings, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)


def Store_Const_and_Store_to(dest):
    class Store_Const_and_Store(Action):
        def __init__(self, option_strings, **kwargs):
            super(Store_Const_and_Store, self).__init__(
                option_strings, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, self.const)
            setattr(namespace, dest, values)
    return Store_Const_and_Store


def build_parser() -> ArgumentParser:
    sira = ArgumentParser(
        prog="sira",
        description="TODO",
        epilog="TODO",
        add_help=False,
        allow_abbrev=False
    )
    sira.add_argument(
        "--init","-i",
        action = "store_true",
    )
    sira.add_argument(
        "dummy",
        action=Ignore,
        nargs="*",
        default=None,
        help="TODO",
        metavar="DUMMY"
    )
    sira.add_argument(
        "-h", "--help",
        action="store_true",
        default=False,
        required=False,
        help="TODO",
        dest="help"
    )
    sira.add_argument(
        "-v", "--verbose",
        action=Store_Const_and_Ignore,
        nargs="*",
        default=None,
        const=True,
        required=False,
        help="TODO",
        dest="verbose",
        metavar="DUMMY"
    )
    sira.add_argument(
        "-s", "--silent",
        action=Store_Const_and_Ignore,
        nargs="*",
        default=None,
        const=False,
        required=False,
        help="TODO",
        dest="verbose",
        metavar="DUMMY"
    )
    sira.add_argument(
        "-q", "--query",
        action=Store_Const_and_Store_to("exprs"),
        nargs="*",
        default=None,
        const="query",
        type=str,
        required=False,
        help="TODO",
        dest="action"
    )
    sira.add_argument(
        "-u", "--update",
        action=Store_Const_and_Store_to("exprs"),
        nargs="*",
        default=None,
        const="update",
        type=str,
        required=False,
        help="TODO",
        dest="action"
    )
    return sira


def extract_values(namespace: Namespace, verbose: bool) -> None:
    if not hasattr(namespace, "exprs") or not hasattr(namespace, "action"):
        return
    exprs = getattr(namespace, "exprs")
    action = getattr(namespace, "action")
    if not action or not exprs:
        return
    for expression in exprs:
        if "=" in expression and expression.count("=") == 1:
            key, value = expression.split("=")
            if key and key in keyword_dict[action]:
                setattr(namespace, key, value)
            elif verbose:
                print('[Verbose]: Unrecognized Keyword "{}" ...'.format(key))
                print('[Verbose]: Ignored Keyword "{}" ...'.format(key))

    # convert limit and key to int
    int_values = ["limit", "key"]
    for entry in int_values:
        if entry in dir(namespace):
            value = getattr(namespace, entry)
            try:
                value = int(float(value))
            except ValueError:
                value = None
            else:
                setattr(namespace, entry, value)


def preprocess_args(args: list) -> list:
    i = 0
    # can be optimized to one loop
    # truncate serial args (eg. ['-ab'] to ['-a', '-b'])
    while i < len(args):
        if args[i].startswith("-") and not args[i].startswith("--"):
            string = args[i]
            del args[i]
            for j in range(len(string) - 1, 0, -1):
                args.insert(i, "-{}".format(string[j]))
        i += 1
    global_switches = ["-v", "--verbose", "-s", "--silent"]
    positional_switches = ["-q", "--query", "-u", "--update"]
    # move all global switches before last positional switches
    cache = list()
    for i in range(len(args) - 1, -1, -1):
        value = args[i]
        if value in global_switches:
            cache.append(value)
            del args[i]
        elif value in positional_switches:
            break
    for element in cache:
        args.insert(i, element)


# expr_dict[action][type][mode]
expr_dict = {
    "default": None,
    "str": "sira-%(action)s",
    "entry": "action",
    "query": {
        "default": None,
        "str": "%(type)s",
        "entry": "type",
        "issue": {
            "default": "mine",
            "str": "",
            "entry": "mode",
            "mine": "-a mine",
            "reported": "-r mine",
            "recent": "-o recent",
            "board": {
                "default": None,
                "str": "",
                "entry": "key",
                "any": "-b %(key)s"
            }
        },
        # hard code here, pay attention!
        # doesn't check the confilict between "-k" and "-l"
        "board": {
            "default": "empty",
            "str": "",
            "entry": "key",
            "any": "-k %(key)s",
            "empty": "-o recent"
        },
        "project": {
            "default": None,
            "str": "",
            "entry": "mode",
            "all": "",
            "current": "-l 1",
            "recent": "-o recent"
        }
    }
}


def process(namespace: Namespace, parser: ArgumentParser, verbose: bool) -> int:
    if namespace.action is None or namespace.help:
        if verbose:
            print("[Verbose]: Printing Help Manual ...")
        parser.print_help()
        exit_prog(0, verbose)
    current_dic = expr_dict
    command = list()
    while 1:
        # check whether there are expressions missing
        entry = current_dic["entry"]
        if not hasattr(namespace, entry):
            default = current_dic["default"]
            if default:
                setattr(namespace, entry, default)
            else:
                # print error msg
                print_err("{} needs to be specified\n".format(entry), "red")
                if verbose:
                    print("[Verbose]: Problematic Command, Aborting ...")
                exit_prog(2, verbose)
        try:
            element = current_dic[getattr(namespace, entry)]
        except KeyError:
            try:
                element = current_dic["any"]
            except KeyError:
                print_err("{} is not a valid {}\n"\
                    .format(getattr(namespace, entry), entry), "red")
                exit_prog(2, verbose)
        if type(element) == str:
            command.append(element)
            break
        else:
            command.append(current_dic["str"])
            current_dic = element
    if hasattr(namespace, "limit"):
        if [s for s in command if "-l" in s]:
            if verbose:
                print('[Verbose]: Keyword "limit" Conflicted with '
                      + 'Other Keywords ...')
                print('[Verbose]: Ignored "limit" ...')
        else:
            command.append("-l %(limit)s")
    if hasattr(namespace, "order"):
        if [s for s in command if "-o" in s]:
            if verbose:
                print('[Verbose]: Keyword "order" Conflicted with '
                      + 'Other Keywords ...')
                print('[Verbose]: Ignored "order" ...')
        else:
            command.append("-o %(order)s")
    if hasattr(namespace, "verbose"):
        verbose = getattr(namespace, "verbose")
        if verbose is not None:
            command.append("-v" if verbose else "-s")
    command.append("-f")
    command = " ".join([s for s in command if s]) % vars(namespace)
    return command

def pwd_input(): 
    chars = []   
    while True:  
        try:  
            newChar = msvcrt.getch().decode(encoding="utf-8")  
        except:  
            return input("the password will not be hidden:")  
        if newChar in '\r\n':                
             break   
        elif newChar == '\b':    
             if chars:    
                 del chars[-1]   
                 msvcrt.putch('\b'.encode(encoding='utf-8'))   
                 msvcrt.putch( ' '.encode(encoding='utf-8'))
                 msvcrt.putch('\b'.encode(encoding='utf-8'))                  
        else:  
            chars.append(newChar)  
            msvcrt.putch('*'.encode(encoding='utf-8')) 
    return (''.join(chars) ) 

def initUser():
    userName=input("Please input your username:")
    print("Please input your password:")
    passWord=pwd_input()
    keyring.set_keyring(Windows.WinVaultKeyring())
    keyring.set_password("sira", userName, passWord)
    jiraUrl=input("\nPlease input Jira domain(including protocol):")
    func.write_to_config(["credential"],["username","jiraUrl"],[userName,jiraUrl])

def main():
    parser = build_parser()
    args = sys.argv[1:]
    preprocess_args(args)
    namespace = parser.parse_args(args)
    verbose = getattr(namespace, "verbose")
    init = getattr(namespace, "init")
    if init:
        initUser()
        return 
    if verbose:
        print("[Verbose]: Finished Analyzing Command Arguments ...")
        print("[Verbose]: A Verbose mode was Detected ...")
        print("[Verbose]: Extracting Values after the Last Query Flag ...")
    extract_values(namespace, verbose)
    if verbose:
        print("[Verbose]: Finished Extracting Values ...")
        print(
            "[Verbose]: Interpreting Your Input and Assembling Subcommand ...")
    command = process(namespace, parser, verbose)
    if verbose:
        print("[Verbose]: Finished Interpreting Your Input ...")
        print('[Verbose]: Running Subcommand "{}" ...'.format(command))
    sub_process = run(command)
    if verbose:
        print("[Verbose]: Finished Running Subcommand ...")
    exit_prog(sub_process.returncode, verbose)


if __name__ == '__main__':
    func.login(["admin", "admin"])
    main()
