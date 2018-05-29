from syntax_interpreter.functions import error_func
from types import FunctionType

class Node:
    """ TODO
    """

    def __init__(self,
                 tgt_func: FunctionType = error_func,
                 parent: Node = None,
                 keyword: str = "",
                 is_extentable: bool = False):
        self.tgt_func = tgt_func
        self.parent = parent
        self.keyword = keyword
        self.is_extentable = is_extentable
        self.children = dict()

    def add_child(self, child: Node = None):
        key = child.keyword
        if key not in self.children.keys():
            self.children[key] = child
        else:
            raise ValueError("Identity keyword {} under {}".format                               (child.keyword, self.keyword))
