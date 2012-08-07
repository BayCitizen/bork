import os

from . import Requirement


class Service(Requirement):
    service_name = str()
    """Service is a wrapper for upstarts service protocol"""
    def __init__(self, service_name=None, *arg, **kwargs):
        self.service_name = service_name
        super(Service, self).__init__()

    def start_service(self):
        print 'starting '
        result = os.popen('/sbin/start %s start' % self.service_name).read()
        print result

    def is_running(self):
        result = os.popen('/sbin/status %s' % self.service_name).read()
        if 'running' in result:
            return True
        return False

    def start_on_boot(self):
        result = os.popen('/sbin/initctl show-config %s').read()
        if 'start on runlevel [2345]' in result:
            return True
        return False

    def make_start_on_boot(self):
        raise NotImplementedError('havent made start on boot work for upstart')

    def execute(self):
        super(Service, self).execute()
        if not self.is_running():
            self.start_service()
        if not self.start_on_boot():
            self.make_start_on_boot()

