from .base_req import Requirement 
from .os_reqs import CommandReq
import subprocess
            

#todo :
#add support for requirement files

class PipReq(Requirement):
    def __init__(self, packages=None, upgrade=False, *args, **kwargs):
        self.packages = packages
        self.upgrade = upgrade
        super(PipReq, self).__init__(*args, **kwargs)

        try:
            import pip
        except ImportError:
            if not self.deps:
                self.deps = []
            self.deps.append(CommandReq(command='easy_install pip'))

    def __str__(self):
        return "Pip requirement with packages %s " % ', '.join(self.packages) + self.deps_str()

    def satisfied(self):
        if self.upgrade:
            return False
        #vefifes that the package is installed
        #try pip freeze 
        process = subprocess.Popen(
            "pip freeze",
            shell=True,
            stdout=subprocess.PIPE
        )
        process.wait()
        pkg_list = process.stdout

        import pip
        #doesnt seem to reload, hence pip freeze.
        for pkg in self.packages:
            exists = False
            if pkg in pkg_list:
                exists = True
            else:
                for dist in pip.get_installed_distributions(local_only=True):
                    if dist.key.startswith(pkg) and dist.key:
                        exists = True
            if not exists:
                return False
        return True

    def satisfy(self):
        import pip
        args = ['install',]
        if self.upgrade:
            args.append('--upgrade')
        args.extend(self.packages)
        exit = pip.main(initial_args=args)

        def exit_status():
            return not exit
        self.satisfied = exit_status
