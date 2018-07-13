from argparse import ArgumentParser, MetavarTypeHelpFormatter
from subprocess import run

def main():
    sira = ArgumentParser(
        prog="sira",
        description="TODO",
        epilog="TODO",
        formatter_class=MetavarTypeHelpFormatter
    )
    sira_sub = sira.add_subparsers(
        title="TODO",
        description="TODO"
    )
    query = sira_sub.add_parser(
        "query",
        help="TODO",
    )
    update = sira_sub.add_parser(
        "update",
        help="TODO",
    )

if __name__ == '__main__':
    main()