class Requirement(object):
    """docstring for Requirement"""
    def __init__(self, deps=None):
        super(Requirement, self).__init__()
        self.deps = deps

    def satisfied(self):
        if self.deps:
            for dep in self.deps:
                if not dep.satisfied():
                    return False
        return True

    def satisfy(self):
        print 'satisfying:', self
        if self.deps:
            for dep in self.deps:
                #if not dep.satisfied():
                dep.satisfy()


