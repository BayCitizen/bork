import shutil
import os
import hashlib
import subprocess

from .base_req import Requirement


class FileReq(Requirement):
    """Basically enforces a file copy and provides a parrent class for the other file operations"""
    def __init__(self, src=None, target=None, perms=None, owner=None, *args, **kwargs):
        super(FileReq, self).__init__(*args, **kwargs)
        self.src = src
        self.target = target
        self.perms = perms
        self.owner = owner
        #verify permissions

    def satisfy(self):
        Requirement.satisfy(self)
        shutil.copy2(self.src, self.target)
        self.set_perms()

    def set_perms(self):
        if self.owner:
            os.chown(self.target, self.owner)
        if self.perms:
            os.chmod(self.target, self.perms)

    @property
    def source_contents(self):
        return open(self.src).read()

    def satisfied(self):
        self.src_hash = hashlib.sha1(self.source_contents).hexdigest()

        try:
            if hashlib.sha1(open(self.target).read()).hexdigest() == self.src_hash:
                return True
        except Exception:
            pass
        return False


class TemplatedFileReq(FileReq):
    """Provides templated file writing. Useful for config files"""
    def __init__(self, template=None, context=None, *args, **kwargs):
        self.template = template
        self.context = context
        super(TemplatedFileReq, self).__init__(*args, **kwargs)

    @property
    def source_contents(self):
        if os.path.exists(self.template) and os.path.isfile(self.template):
            template = open(self.template, 'r').read()
        else:
            template = self.template
        return template % self.context

    def satisfy(self):
        Requirement.satisfy(self)
        dFile = open(self.target, 'w')
        dFile.write(self.source_contents)
        dFile.close()
        self.set_perms()


class FileExistsReq(FileReq):
    def __init__(self, directory=False, *args, **kwargs):
        self.directory = directory
        super(FileExistsReq, self).__init__(*args, **kwargs)

    def satisfied(self):
        if os.path.exists(self.target):
            if os.path.isfile(self.target):
                return not self.directory
            else:
                return self.directory
        return False

    def satisfy(self):
        Requirement.satisfy(self)
        raise NotImplementedError


class FileDoesNotExistReq(FileReq):
    def __init__(self, force=False, *args, **kwargs):
        self.force = force
        super(FileDoesNotExistReq, self).__init__(*args, **kwargs)

    def satisfied(self):
        if os.path.exists(self.target):
            return False
        else:
            return True

    def satisfy(self):
        Requirement.satisfy(self)
        #delete file
        #hack! dont worry about force for now
        os.remove(self.target)


class LinkedFileReq(FileReq):
    """Sets up a link from target to src, hard or soft. """
    def __init__(self, symbolic=True, *args, **kwargs):
        self.symbolic = symbolic
        super(LinkedFileReq, self).__init__(*args, **kwargs)
        #check if exists

    def satisfied(self):
        if self.symbolic:
            try:
                #test for existing link
                if os.readlink(self.src) == self.target:
                    return True
            except Exception, e:
                return False
        #testing hard links is hard, test file contents instead for now
        #HACK!
        return super(LinkedFileReq, self).satisfied()

    def satisfy(self):
        Requirement.satisfy(self)
        if self.symbolic:
            os.symlink(self.target, self.src)
        else:
            os.link(self.target, self.src,)
        self.set_perms()


class DirectoryReq(FileExistsReq):
    def __init__(self, mode=None, *args, **kwargs):
        self.mode = mode
        kwargs['directory'] = True
        super(DirectoryReq, self).__init__(*args, **kwargs)

    def satisfy(self):
        Requirement.satisfy(self)
        os.makedirs(self.target)


class CommandReq(Requirement):
    """Runs a command, stores the result in self.result"""
    def __init__(self, command=None, unless=None, cwd=None, *args, **kwargs):
        super(CommandReq, self).__init__(*args, **kwargs)
        self.command = command
        self.unless = unless
        self.cwd = cwd

    def satisfied(self):
        if self.unless:
            if not subprocess.call(self.unless, shell=True):
                return True
        return False

    def satisfy(self):
        Requirement.satisfy(self)
        print "executing command: ", self.command
        self.result = subprocess.Popen(self.command, shell=True, cwd=self.cwd)
        self.result.wait()
        print self.result.stdout
        print self.result.stderr
        print self.result.returncode
