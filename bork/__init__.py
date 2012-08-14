from .apt_reqs import AptReq
from .git_reqs import GitRepoReq
from .os_reqs import FileReq, TemplatedFileReq, LinkedFileReq, CommandReq
from .pip_reqs import PipReq
from .service_req import ServiceReq


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
