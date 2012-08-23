class Requirement(object):
    """docstring for Requirement"""
    def __init__(self, deps=None):
        self.deps = deps

    def satisfied(self):
        if self.deps:
            for dep in self.deps:
                if not dep.satisfied():
                    return False
        return True

    def __str__(self):
        string = self.__class__.__name__
        return string + self.deps_str()


    def deps_str(self):
        if self.deps:
            string = " with deps:"
            for dep in self.deps:
                dep_str = str(dep)
                #indent children farther
                dep_str = "\t\t".join(dep_str.split("\t"))
                string = string + "\n\t%s" % dep_str
            return string
        return ""

    def satisfy(self):
        if self.deps:
            for dep in self.deps:

                if not dep.satisfied():
                    print 'satisfying: ', self
                    dep.satisfy()
                    print "[OK]"
                else:
                    print 'skipping: ', self


