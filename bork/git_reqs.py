import os


from . import Requirement
from .pip_reqs import PipReq

class GitRepoReq(Requirement):
    def __init__(self, repo=None, dest=None, branch=None,  *args, **kwargs):
        super(GitRepoReq, self).__init__(*args, **kwargs)
        self.repo = repo
        self.dest = dest
        self.branch = branch
        
        try:
            import dulwich
        except ImportError:
            if not self.deps:
                self.deps=[]
            self.deps.append(PipReq('dulwich'))

    def satisfied(self):
        #does a get statis on the repo dir, to check that its there
        from dulwich.repo import Repo
        try:
             Repo(self.dest)
             return True
        except:
            return False

    def satisfy(self):
        Requirement.satisfy(self)
        print 'checking out %s to %s' % (self.src, self.dest)
        from dulwich.client import get_transport_and_path
        from dulwich.repo import Repo
        client = get_transport_and_path(self.repo)
        local = Repo.init(self.dest, mkdir=True)
        client.fetch("/", local)
        print "has index: ", local.has_index()
