import sys
from argparse import ArgumentParser

from func import query_board, query_issue, query_project, query_jql
from utils import print_err, exit_prog

issue_opts_list = ["assignee", "board", "creator", "id", "key", "label",
                   "priority", "reporter", "type", "watcher"]

user_opts = ["assignee", "creater", "reporter", "watcher"]

jql_ignore = ["sub_command", "order", "limit", "constraint", "from_sira",
              "board", "verbose", "verbose_new", "auth"]


def build_parser():
    query = ArgumentParser(
        prog="sira-query",
        description="Querying issue/project/board information from JIRA"
    )
    query.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=None,
        required=False,
        help="output more information with the command execution.",
        dest="verbose"
    )
    query.add_argument(
        "-s", "--silent",
        action="store_false",
        default=None,
        required=False,
        help="reduce unnecessary information output.",
        dest="verbose"
    )
    sub = query.add_subparsers(
        title="issue, project, board are options to be queried",
        description="",
        parser_class=ArgumentParser,
        help="[ -l ${num} for limit numbers of result | -o ${order} for order the result | -a mine for only showing your info ]",
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
    jql = sub.add_parser(
        "jql",
        prog="jql",
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

    jql.add_argument(
        "-q", "--query",
        action="store",
        default=None,
        type=str,
        required=False,
        help="TODO",
        dest="query"
    )

    # add from-sira, limit, and order to each sub-command
    for sub_command in [issue, project, board, jql]:
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
            "-u", "--user",
            action="store",
            type=str,
            default=None,
            required=False,
            help="TODO",
            dest="auth"
        )
        sub_command.add_argument(
            "-v", "--verbose",
            action="store_true",
            default=None,
            required=False,
            help="output more information with the command execution.",
            dest="verbose_new"
        )
        sub_command.add_argument(
            "-s", "--silent",
            action="store_false",
            default=None,
            required=False,
            help="reduce unnecessary information output.",
            dest="verbose_new"
        )
    return query


def main():
    parser = build_parser()
    namespace = parser.parse_args()
    verbose = namespace.verbose if not hasattr(namespace,"verbose_new") or namespace.verbose_new is None\
                                else namespace.verbose_new
    setattr(namespace, "verbose", verbose)
    if verbose:
        print("[Verbose]: Finished Analyzing Command Arguments ...")
        print("[Verbose]: A Verbose mode was Detected ...")
    if not namespace.sub_command:
        if verbose:
            print("[Verbose]: No Subcommand was Specified ...")
            print("[Verbose]: Printing Help Manual ...")
        parser.print_help()
        exit_prog(0, verbose)
    # floor limit
    if "limit" in dir(namespace):
        setattr(namespace, "limit", int(getattr(namespace, "limit")))
    sub_command = namespace.sub_command
    if verbose:
        print('[Verbose]: A Subcommand "{}" was Detected ...'\
        .format(sub_command))
        print('[Verbose]: Continuing Processing with Subcommand "{}" ...'\
        .format(sub_command))
    if sub_command == "issue":
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
    elif sub_command == "project":
        status, msg = query_project(**vars(namespace))
    elif sub_command == "board":
        status, msg = query_board(**vars(namespace))
    elif sub_command == "jql":
        status, msg = query_jql(**vars(namespace))
    if status:
        print(msg, end="")
    else:
        print_err(msg, "red")
    if getattr(namespace, "from_sira") or verbose:
        print()
    exit_prog(0 if status else 1, verbose)


if __name__ == '__main__':
    main()
