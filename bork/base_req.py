def satisfy_deps(deps, make_satisfied=False):
    for dep in deps:
        if dep.deps:
            satisfy_deps(dep.deps, make_satisfied=make_satisfied)
        print 'checking: %s' % dep
        if not dep.satisfied():
            if make_satisfied:
                dep.satisfy()
                if dep.satisfied():
                    print "[OK]"
                else:
                    print "Something went wrong! Could not satisfy %s" % dep
                    raise Exception
            else:
                return False
    return True


class Requirement(object):
    """docstring for Requirement"""
    def __init__(self, deps=None):
        self.deps = deps

    def satisfied(self):
        return satisfy_deps(self.deps)

    def __str__(self):
        string = self.__class__.__name__
        return string + self.deps_str()

    def deps_str(self):
        if self.deps:
            string = " with deps:"
            for dep in self.deps:
                dep_str = str(dep)
                #indent children farther
                dep_str = "\n\t".join(dep_str.split("\n"))
                string = string + "\n\t%s" % dep_str
            return string
        return ""

    def satisfy(self):
        if self.deps:
            satisfy_deps(self.deps, make_satisfied=True)
