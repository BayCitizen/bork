import shutil
import os
from stat import S_IMODE
from pwd import getpwnam
from grp import getgrnam
import hashlib
import subprocess

from .base_req import Requirement


class FileReq(Requirement):
    """Basically enforces a file copy and provides a parrent class for the other file operations"""
    def __init__(self, src=None, target=None, *args, **kwargs):
        super(FileReq, self).__init__(*args, **kwargs)
        self.src = src
        self.target = target


    def satisfy(self):
        print("copying file %s to %s" % (self.src, self.target))
        shutil.copy2(self.src, self.target)

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


class FilePermReq(Requirement):
    def __init__(self, target=None, perms=None, owner=None, group=None, *args, **kwargs):
        super(FilePermReq, self).__init__(*args, **kwargs)
        self.target = target
        self.perms = perms
        self.owner = owner
        if owner:
            self.uid = getpwnam(owner).pw_uid
        self.group = group
        if group:
            self.gid = getgrnam(group).gr_gid
        

    def satisfied(self):
        stats = os.stat(self.target)
        if self.perms:
            if(self.perms != int(S_IMODE(stats.st_mode))):
                return False
        if self.owner:
            if(self.uid != stats.st_uid):
                return False
        if self.group:
            if(self.gid != stats.st_gid):
                return False
        return True

    def satisfy(self):
        stats = os.stat(self.target)
        if self.perms:
            print "changing perms to", self.perms
            os.chmod(self.target, self.perms)
        if self.owner or self.group:
            args = [
                self.target,
                stats.st_uid,
                stats.st_gid,
            ]
            if self.owner:
                args[1] = self.uid
            if self.group:
                args[2] = self.gid
            print args
            os.chown(*args)


class TemplatedFileReq(FileReq):
    """Provides templated file writing. Useful for config files"""
    def __init__(self, template=None, context=None, *args, **kwargs):
        self.template = template
        self.context = context
        super(TemplatedFileReq, self).__init__(*args, **kwargs)

    @property
    def source_contents(self):
        template_path =  os.path.join(os.getcwd(), self.template)
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        print template_path
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        if os.path.exists(template_path) and os.path.isfile(template_path):
            template = open(template_path, 'r').read()
        else:
            template = self.template
        return template % self.context

    def satisfy(self):
        print("writing file %s with template %s using context %s" % (self.target, self.template, self.context))
        dFile = open(self.target, 'w')
        dFile.write(self.source_contents)
        dFile.close()


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
        print("File exists: %s \n Aborting!!!!!" % self.target)
        raise NotImplementedError


class DirectoryReq(FileExistsReq):
    def __init__(self, mode=None, *args, **kwargs):
        self.mode = mode
        kwargs['directory'] = True
        super(DirectoryReq, self).__init__(*args, **kwargs)

    def satisfy(self):
        print "making the directory %s" % self.target
        os.makedirs(self.target)


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
        #delete file
        #hack! dont worry about force for now
        print("deleteing %s" % self.target)
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
                else:
                    return False
            except:
                return False
        #testing hard links is hard, test file contents instead for now
        #HACK!
        return super(LinkedFileReq, self).satisfied()

    def satisfy(self):
        if self.symbolic:
            print("creating symlink %s to %s" % (self.target, self.src))
            os.symlink(self.target, self.src)
        else:
            print("hard link %s" % self.target)
            os.link(self.target, self.src,)


class CommandReq(Requirement):
    """Runs a command, stores the result in self.result"""
    def __init__(self, command=None, run_once=True, unless=None, cwd=None, *args, **kwargs):
        super(CommandReq, self).__init__(*args, **kwargs)
        self.command = command
        self.unless = unless
        self.cwd = cwd
        self.run_once = run_once


    def __str__(self):
        return "CommandReq %s " % self.command+ self.deps_str()

    def satisfied(self):
        if self.unless:
            if not subprocess.call(self.unless, shell=True):
                return True
        if hasattr(self, 'result'):
            if self.run_once and not self.result.returncode:
                return True
        return False

    def satisfy(self):
        print "executing command: ", self.command
        self.result = subprocess.Popen(self.command, shell=True, cwd=self.cwd)
        self.result.wait()