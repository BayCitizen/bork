import os
from .base_req import Requirement
from .os_reqs import CommandReq


class GitRepoReq(Requirement):
    def __init__(self, repo=None, target=None, branch="Master", *args, **kwargs):
        super(GitRepoReq, self).__init__(*args, **kwargs)
        self.target = target
        self.repo = repo
        self.branch = branch
        
        if not self.deps:
            self.deps = []

        self.deps.append(CommandReq(command="git clone -b %s %s %s" % (branch, repo, target)))

    def __str__(self):
        return "git repo requirement %s branch %s is going to %s" % (self.repo, self.branch, self.target) + self.deps_str()

    def satisfied(self):
        #does a git statis on the repo dir, to check that its there
        try:
            if os.path.exists(self.target + '/.git'):
                return True
        except:
            pass
        return False
