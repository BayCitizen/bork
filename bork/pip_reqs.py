from . import Requirement 
from .command_reqs import CommandReq

class PipReq(Requirement):
    def __init__(self, target=None, *args, **kwargs):
        super(PipReq, self).__init__(*args, **kwargs)
        self.target = target

        try:
            import pip
        except ImportError:
            if not self.deps:
                self.deps=[]
            self.deps.append(CommandReq(command='easy_install pip'))

    def satisfied(self):
        #vefifes that the package is installed
        for dist in get_installed_distributions(local_only=True):
            if dist.key.startswith(self.target) and dist.key :
                return True
        return False

    def satisfy(self):
    	import pip
    	pip.main(initial_args=['install', self.target])

