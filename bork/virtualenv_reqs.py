import os
import subprocess
from .base_req import Requirement
from . import CommandReq, PipReq


class VirtualenvReq(Requirement):
    def __init__(self, directory=None, requirements=None, *args, **kwargs):
        super(VirtualenvReq, self).__init__(*args, **kwargs)
        if not self.deps:
            self.deps = []
        try:
            import virtualenv
        except ImportError:
            self.deps.append(PipReq(packages=['virtualenv']))
        #interface with virtual env via a command line
        self.deps.append(CommandReq(command='virtualenv %s --distribute' % directory))
        self.directory = directory
        self.requirements = requirements

    def satisfied(self):
        #check to see if the python binary is in the right place
        return os.path.exists("%s/bin/python" % self.directory)

    def satisfy(self):
        import pdb; pdb.set_trace()
        if self.requirements:
            location = os.path.join(self.directory, 'bin/activate')
            command = "bash -c 'source %s && pip install -r %s'" % (location, self.requirements)
            process = subprocess.Popen(command, shell=True)
            process.wait()


class VirtualenvCommandReq(CommandReq):
    def __init__(self, directory=None, command=None, *args, **kwargs):
        kwargs['command'] = ("source %sbin/activate &&" % directory) + command
        super(VirtualenvCommandReq, self).__init__(*args, **kwargs)
