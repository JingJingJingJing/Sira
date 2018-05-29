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

    def add_child(self, child: Node):
        assert child is not None, "None child is not allowed"
        existence = child.keyword in self.children.keys()
        error_msg = "Identity keyword {} under {}".format(child.keyword, 
                                                           self.keyword)
        assert not existence, error_msg

        self.children[child.keyword] = child
        child.parent = self
        return False

    def del_child(self, child: Node):
        assert child is not None, "None child is not allowed"
        existence = child.keyword in self.children.keys()
        error_msg = "{} does not exist".format(child.keyword)
        assert existence, error_msg

        self.children.pop(child.keyword)
        child.parent = None
        return True
    
    def set_tgt(self, func: FunctionType = error_func):
        pass