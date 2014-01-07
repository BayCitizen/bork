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

        # interface with virtualenv via a command line
        env = CommandReq(
            command='virtualenv %s --distribute' % directory,
            unless='test -s "%s/bin/activate"' % directory)  # env already exists
        self.deps.append(env)
        self.directory = directory
        self.requirements = requirements
        self.requirements_installed = not bool(requirements)

    def satisfied(self):
        #check to see if the python binary is in the right place
        return os.path.exists("%s/bin/python" % self.directory) and self.requirements_installed

    def satisfy(self):
        if self.requirements:
            location = os.path.join(self.directory, 'bin', 'activate')
            command = "bash -c 'source %s && pip install --allow-all-external -r %s'" % (location, self.requirements)
            print 'executing: %s' % command
            process = subprocess.Popen(command, shell=True)
            process.wait()
            self.requirements_installed = True


class VirtualenvCommandReq(CommandReq):
    def __init__(self, directory=None, command=None, *args, **kwargs):
        kwargs['command'] = ("source %sbin/activate &&" % directory) + command
        super(VirtualenvCommandReq, self).__init__(*args, **kwargs)
