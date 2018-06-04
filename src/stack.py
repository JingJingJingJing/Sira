class Node(object):

    def __init__(self):
        self.data = None
        self.post = None
        self.prev = None

class CommandStack(object):

    def __init__(self):
        self._create_new_ref()
    
    def _create_new_ref(self):
        self.smt_btm = Node()
        self.smt_top = Node()
        self.traversal_dummy = Node()
        self.traversal_dummy.data = ""
        self.smt_top.post = self.traversal_dummy
        self.traversal_dummy.post = self.smt_btm
        self.smt_btm.prev = self.traversal_dummy
        self.traversal_dummy.prev = self.smt_top
        self.traversal = self.traversal_dummy
        self.len = 1

    def reset_traversal(self):
        self.traversal = self.traversal_dummy
    
    def push(self, data):
        new_node = Node()
        new_node.data = data
        new_node.prev = self.traversal_dummy
        new_node.post = self.traversal_dummy.post
        self.traversal_dummy.post.prev = new_node
        self.traversal_dummy.post = new_node
        self.len += 1
    
    def peak(self):
        return self.traversal.data

    def step_back(self):
        if self.traversal.post != self.smt_btm:
            self.traversal = self.traversal.post

    def step_forward(self):
        if self.traversal.prev != self.smt_top:
            self.traversal = self.traversal.prev

    def _pop(self):
        result = None
        if self.len > 1:
            result = self.traversal_dummy.post.data
            self.traversal_dummy.post.post.prev = self.traversal_dummy
            self.traversal_dummy.post = self.traversal_dummy.post.post
            self.len -= 1
        return result
    
    def clear(self):
        self._create_new_ref()