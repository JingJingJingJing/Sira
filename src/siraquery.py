from argparse import ArgumentParser
from sys import exit, stderr, stdin, stdout, platform

from termcolor import colored

from func import query_board, query_issue, query_project

issue_opts_list = ["assignee", "board", "creator", "id", "key", "label",
                   "priority", "reporter", "type", "watcher"]

user_opts = ["assignee", "creater", "reporter", "watcher"]

jql_ignore = ["sub_command", "order", "limit", "constraint", "from_sira",
              "board", "verbose"]


def build_parser():
    query = ArgumentParser(
        prog="sira-query",
        description="TODO",
        epilog="TODO"
    )
    sub = query.add_subparsers(
        title="TODO",
        description="TODO",
        parser_class=ArgumentParser,
        help="TODO",
        dest="sub_command"
    )
    issue = sub.add_parser(
        "issue",
        prog="issue",
        description="TODO",
        epilog="TODO"
    )
    project = sub.add_parser(
        "project",
        prog="project",
        description="TODO",
        epilog="TODO"
    )
    board = sub.add_parser(
        "board",
        prog="board",
        description="TODO",
        epilog="TODO"
    )

    # add options in issue
    issue_opts = dict()
    for opt in issue_opts_list:
        issue_opts[opt] = issue.add_argument(
            "-{}".format(opt[0] if opt[0] != "l" else "L"),
            "--{}".format(opt),
            action="store",
            default=None,
            type=str,
            required=False,
            help="TODO",
            dest=opt
        )
    issue_opts["id"].type = int
    issue_opts["board"].type = int
    issue.add_argument(
        "constraint",
        action="store",
        nargs="?",
        default=None,
        type=str,
        help="TODO",
        metavar="CONSTR"
    )

    # add key in board
    board.add_argument(
        "-k", "--key",
        action="store",
        default=None,
        type=int,
        required=False,
        help="TODO",
        dest="key"
    )

    # add from-sira, limit, and order to each sub-command
    for sub_command in [issue, project, board]:
        sub_command.add_argument(
            "-f", "--from-sira",
            action="store_true",
            default=False,
            required=False,
            help="TODO",
            dest="from_sira"
        )
        sub_command.add_argument(
            "-l", "--limit",
            action="store",
            default=0,
            type=float,
            required=False,
            help="TODO",
            dest="limit"
        )
        sub_command.add_argument(
            "-o", "--order",
            action="store",
            default="recent",
            type=str,
            choices=["desc", "asc", "recent", "DESC", "ASC", "RECENT"],
            required=False,
            help="TODO",
            dest="order"
        )
        sub_command.add_argument(
            "-v", "--verbose",
            action="store_true",
            default=None,
            required=False,
            help="TODO",
            dest="verbose"
        )
        sub_command.add_argument(
            "-s", "--silent",
            action="store_false",
            default=None,
            required=False,
            help="TODO",
            dest="verbose"
        )
    return query


def print_err(msg: str, color: str) -> None:
    if platform in ("win32", "cygwin"):
        import colorama
        colorama.init()
    print(colored(msg + "\n", color=color))
    if platform in ("win32", "cygwin"):
        import colorama
        colorama.deinit()


def main():
    parser = build_parser()
    namespace = parser.parse_args()
    if not namespace.sub_command:
        parser.print_help()
        return
    # floor limit
    if "limit" in dir(namespace):
        setattr(namespace, "limit", int(getattr(namespace, "limit")))
    if namespace.sub_command == "issue":
        kwargs = vars(namespace)
        jql = kwargs["constraint"] if kwargs["constraint"] else ""
        for element in kwargs:
            value = "currentUser()"\
                    if element in user_opts and kwargs[element] == "mine"\
                    else kwargs[element]
            if element not in jql_ignore and value:
                jql += " and {} = {}".format(element, value) if jql\
                       else "{} = {}".format(element, value)
        kwargs["constraint"] = jql
        status, msg = query_issue(**kwargs)
    elif namespace.sub_command == "project":
        status, msg = query_project(**vars(namespace))
    elif namespace.sub_command == "board":
        status, msg = query_board(**vars(namespace))
    if getattr(namespace, "from_sira") or status:
        print(msg, file=stdout)
    else:
        print_err(msg, "red")
    exit(0 if status else 1)


if __name__ == '__main__':
    # import func
    # func.login(["admin", "admin"])
    main()
