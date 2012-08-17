from .base_req import Requirement 
from .os_reqs import CommandReq

#todo :
#add support for requirement files

class PipReq(Requirement):
    def __init__(self, packages=None, *args, **kwargs):
        super(PipReq, self).__init__(*args, **kwargs)
        self.packages = packages

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
        Requirement.satisfy(self)
    	import pip
        for package in self.packages:
    	   pip.main(initial_args=['install', package])

