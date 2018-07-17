import sys
from argparse import Action, ArgumentParser, Namespace
from subprocess import run

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
            super(Store_Const_and_Store, self).__init__(option_strings, **kwargs)

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


def extract_values(namespace: Namespace) -> None:
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
    ### can be optimized to one loop
    i = 0
    while i < len(args):
        if args[i].startswith("-") and not args[i].startswith("--"):
            string = args[i]
            del args[i]
            for j in range(len(string) - 1, 0, -1) :
                args.insert(i, "-{}".format(string[j]))
        i += 1
    global_switches = ["-v", "--verbose", "-s", "--silent"]
    positional_switches = ["-q", "--query", "-u", "--update"]
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

def main():
    parser = build_parser()
    args = sys.argv[1:]
    preprocess_args(args)
    namespace = parser.parse_args(args)
    extract_values(namespace)
    print(namespace)


if __name__ == '__main__':
    main()
