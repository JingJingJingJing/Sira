import sys
from termcolor import colored
if sys.platform in ("win32", "cygwin"):
    import colorama
    colorama.init()
sys.stdout.write(colored('xxx\n', color="red", on_color="on_red"))
sys.stdout.write(colored('xxx\n', color="red", on_color="on_yellow"))
sys.stdout.write(colored('xxx\n', color="red", on_color="on_green"))
sys.stdout.write(colored('xxx\n', color="red", on_color="on_cyan"))
sys.stdout.write(colored('xxx\n', color="red", on_color="on_blue"))
sys.stdout.write(colored('xxx\n', color="red", on_color="on_magenta"))
CURSOR_UP_ONE = '\033[1A'
ERASE_LINE = '\033[2K'
sys.stdout.write(CURSOR_UP_ONE)
sys.stdout.write(ERASE_LINE)
if sys.platform in ("win32", "cygwin"):
    import colorama
    colorama.deinit()