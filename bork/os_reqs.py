import shutil
import os
import hashlib

from . import Requirement


class FileReq(Requirement):
    """Basically enforces a file copy and provides a parrent class for the other file operations"""
    def __init__(self, src=None, dest=None, perms=None, owner=None,  *args, **kwargs):
        super(FileReq, self).__init__(*args, **kwargs)
        self.src = src
        self.dest = dest
        self.perms = perms
        self.owner = owner
        #verify permissions

    def satisfy(self):
        Requirement.satisfy(self)
        shutil.copy2(self.src, self.dest)
        self.set_perms()

    def set_perms(self):
        if self.owner:
            os.chown(self.dest, self.owner)
        if self.perms:
            os.chmod(self.dest, self.perms)

    @property
    def source_contents(self):
        return open(self.src).read()

    def satisfied(self):
        self.src_hash = hashlib.sha1(self.source_contents).hexdigest()

        try:
            if hashlib.sha1(open(self.dest).read()).hexdigest() == self.src_hash:
                return True
        except Exception:
            pass
        return False


class TemplatedFileReq(FileReq):
    """Provides templated file writing. Useful for config files"""
    def __init__(self, template=None, dest=None, context=None, perms=None, *args, **kwargs):
        self.template = template
        self.context = context
        super(TemplatedFileReq, self).__init__(*args, **kwargs)

    @property
    def source_contents(self):
        return template % context

    def satisfy(self):
        Requirement.satisfy(self)
        dFile = open(self.dest, 'w')
        print dFile self.source_contents
        self.set_perms()


class LinkedFileReq(FileReq):
    """Sets up a link from dest to src, hard or soft. """
    def __init__(self, symbolic=True,  *args, **kwargs):
        super(LinkedFileReq, self).__init__(*args, **kwargs)
        #check if exists

    def satisfied(self):
        if self.symbolic:
            try:
                #test for existing link 
                if os.readlink(self.dest) == self.src:
                    return True
            except Exception, e:
                print e
                return False
        #testing hard links is hard, test file contents instead for now
        #HACK!
        return super(LinkedFileReq, self).satisfied()

    def satisfy(self):
        if self.symbolic:
            os.symlink(self.src, self.dest)
        else:
            os.link(self.src, self.dest)
        self.set_perms()


class CommandReq(Requirement):
    """Runs a command, stores the result in self.result"""
    def __init__(self, command=None, *args, **kwargs):
        super(CommandReq, self).__init__(*args, **kwargs)
        self.command = command

    def satisfied(self):
        return False

    def satisfy(self):
        Requirement.satisfy(self)
        print "executing command: ", self.command
        self.result = os.popen(self.command)
