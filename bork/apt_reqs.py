import apt

from .base_req import Requirement
from .os_reqs import CommandReq


def cache_update():
    """reloads the apt cache. think of it as a apt-get update"""
    #print "updateing the apt cache"
    apt.apt_pkg.init_config()
    apt.apt_pkg.init_system()
    apt_cache = apt.Cache()
    apt_cache.update()
    apt_cache.open(None)
    return apt_cache


class AptUpgrade(Requirement):
    result = False
    """ runs a apt get upgrade in the software."""
    def satisfied(self):
        #upgrade allways must be run
        return bool(self.result)

    def satisfy(self):
        Requirement.satisfy(self)
        print "begining apt-get update"
        apt_cache = cache_update()
        print "packages to be upgraded"
        apt_cache.upgrade()
        for pkg in apt_cache.getChanges():
            print pkg.sourcePackageName,
        print "\nbegining apt-get upgrade"
        self.result = apt_cache.commit()


class AptReq(Requirement):
    """AptReq handles package adding and removing on debian based systems"""
    def __init__(self, source=None, packages=None, exclude=None, *args, **kwargs):
        super(AptReq, self).__init__(*args, **kwargs)
        self.source=source
        if source:
            if source.split(':', 1)[0] == 'ppa':
                self.ppa = source
            elif('deb ' in source):
                if not self.deps:
                    self.deps = []
                #hack!
                self.deps.append(
                    CommandReq(command="""grep -q  "%s"  /etc/apt/sources.list||
                        echo "%s" >> /etc/apt/sources.list""" % (source, source))
                    )
        self.packages = packages
        self.exclude = exclude
        try:
            __import__('softwareproperties.SoftwareProperties')
        except ImportError:
            if not "python-software-properties" in self.packages:
                if not self.deps:
                        self.deps = []
                self.deps.append(
                    AptReq(packages=["python-software-properties"]))

    def __str__(self):
        return "AptReq with packages %s " % ', '.join(self.packages) + self.deps_str()

    def satisfied(self):
        apt_cache = cache_update()
        #check for installed package[s]
        for pkg_name in self.packages:
            try:
                pkg = apt_cache[pkg_name]
            except KeyError:
                return False
            if not pkg.isInstalled or pkg.isUpgradable:
                print self, " not satisfied"
                print pkg.sourcePackageName, ' not up to date'
                return False
        return True

    def satisfy(self):
        if hasattr(self, 'ppa'):
            print self.ppa
            #hack!
            from softwareproperties.SoftwareProperties import SoftwareProperties
            print "adding ppa: %s" % self.ppa
            sp = SoftwareProperties()
            sp.add_source_from_line(self.ppa)
            sp.sourceslist.save()
            print "finished adding ppa"

        if self.packages:
            apt_cache = cache_update()
            for pkg_name in self.packages:
                print "adding %s to the install list" % pkg_name
                pkg = apt_cache[pkg_name]
                pkg.mark_install(auto_inst=True, from_user=True)
            apt_cache.commit()
        if self.exclude:
            apt_cache = cache_update()
            for pkg_name in self.exlude:
                print "adding %s to the remove list" % pkg_name
                pkg = apt_cache[pkg_name]
                pkg.mark_delete()
            apt_cache.commit()
