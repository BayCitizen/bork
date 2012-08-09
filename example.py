import os

from bork.apt_reqs import AptReq, AptUpgrade
from bork.os_reqs import CommandReq
from bork import Requirement


lsb_release = os.popen('lsb_release -sc').read().rstrip()


print "running on ubuntu %s" % lsb_release

install_dropbox_key = CommandReq(command='sudo apt-key adv --keyserver pgp.mit.edu --recv-keys 5044912E')
install_oracle_key = CommandReq(command='wget -q -O - http://download.virtualbox.org/virtualbox/debian/oracle_vbox.asc | sudo apt-key add -')
install_cairo_key = CommandReq(command='sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E80D6BF5')

Requirement(deps=(
    #desktop stuff
    AptReq(source="deb http://archive.canonical.com/ %s partner" % lsb_release, packages=['skype']),
    AptReq(source="ppa:otto-kesselgulasch/gimp", packages=['gimp']),
    AptReq(source="deb http://dl.google.com/linux/chrome/deb/ stable main", packages=['google-chrome-stable']),
    AptReq(source="deb http://download.tuxfamily.org/glxdock/repository/ubuntu %s cairo-dock" % lsb_release,
             packages=['cairo-dock','cairo-dock-plug-ins'],  deps=[install_cairo_key]),
    AptReq(source="deb http://linux.dropbox.com/ubuntu/ %s main" % lsb_release, deps=[install_dropbox_key], packages=['dropbox']),  
    AptReq(source="deb http://download.virtualbox.org/virtualbox/debian %s non-free contrib" % lsb_release, deps=[install_oracle_key]),
    AptReq(source="ppa:webupd8team/java", packages=['oracle-java7-installer']),
    AptReq(packages=['banshee', 'terminator', 'gmrun']),
    #dev stuff
    AptReq(source="ppa:webupd8team/sublime-text-2", packages=['sublime-text']),
    AptReq(packages=['tig', 'vim-nox', 'build-essential', 'autotools-dev', 'virtualenvwrapper', 'libmysqlclient-dev',
                                'nodejs', 'virtualbox', 'mercurial', 'subversion', 'thunar-vcs-plugin', 'meld', 'mysql-workbench', 
                                'autoconf', 'libtool'
                                ]),
    #network stuff
    AptReq(packages=['netcat', 'nmap', 'wireshark' ]),
    #untrustworthy crap
    AptReq(exclude=['apport', 'apport-gtk', 'apport-symptoms']),
    #upgrade!
    AptUpgrade(),
)).satisfy()