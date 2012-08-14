import os

from .base_req import Requirement


class ServiceReq(Requirement):
    service_name = str()
    """Service is a wrapper for upstarts service protocol"""
    def __init__(self, service_name=None, restart_on_boot=None, *arg, **kwargs):
        self.service_name = service_name
        self.restart_on_boot
        super(Service, self).__init__(*args, **kwargs)

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
        result = os.popen('/sbin/initctl show-config %s' % self.service_name).read()
        if self.service_name in result:
            if 'start on runlevel [2345]' in result:
                return True
        else:
            result = os.popen('ls /etc/rc*.d/S**%s' % self.service_name)
            if self.service_name in result:
                return True
        return False

    def make_start_on_boot(self):
        if self.use_upstart:
            f = open('/etc/init/%s.conf'%self.service_name, 'r+')
            f.write("""#Start when system enters runlevel 2 (multi-user mode).
start on runlevel [2345]
start on runlevel [!2345]

# Start delayed_job via the daemon control script.
exec /etc/init.d/%s start

# Restart the process if it dies with a signal
# or exit code not given by the 'normal exit' stanza.
respawn

# Give up if restart occurs 10 times in 90 seconds.
respawn limit 5 90
""" % self.service_name)
            f.close()
        else:
            os.popen("update-rc.d %s defaults" % self.service_name)


    def execute(self):
        super(Service, self).execute()
        if not self.is_running():
            self.start_service()
        if not self.start_on_boot() and self.restart_on_boot:
            self.make_start_on_boot()

