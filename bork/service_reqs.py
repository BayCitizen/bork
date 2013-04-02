import os
import subprocess
from subprocess import PIPE

from .base_req import Requirement


#still needs a lot of work
class ServiceReq(Requirement):
    """Service is a wrapper for upstarts service protocol"""
    def __init__(self, service_name=None, restart_on_boot=None, use_upstart=False, is_running_text=None, *args, **kwargs):
        self.service_name = service_name
        self.restart_on_boot = restart_on_boot
        self.use_upstart = use_upstart
        self.is_running_text = is_running_text or 'running'

        super(ServiceReq, self).__init__(*args, **kwargs)

    def __str__(self):
        return "ServiceReq for service %s" % self.service_name + self.deps_str()

    def start_service(self):
        if self.use_upstart:
            result = subprocess.Popen('/sbin/start %s start' % self.service_name, shell=True, stdout=PIPE, stderr=PIPE)
        elif(os.path.exists('/etc/init.d/%s' % self.service_name)):
            result = subprocess.Popen('/etc/init.d/%s start' % self.service_name, shell=True, stdout=PIPE, stderr=PIPE)
        else:
            pass
            #wtf?
        stdout, stderr = result.communicate()
        print stdout

    def is_running(self):
        stdout, stderr = None, None
        if self.use_upstart:
            result = subprocess.Popen('/sbin/status %s' % self.service_name, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = result.communicate()
            if self.is_running_text in stdout:
                return True
            print stdout, stderr
            return False
        else:
            if(os.path.exists('/etc/init.d/%s' % self.service_name)):
                status = subprocess.Popen('/etc/init.d/%s status' % self.service_name, shell=True, stdout=PIPE, stderr=PIPE)
                stdout, stderr = status.communicate()
                if self.is_running_text in stdout and not status.returncode:
                    return True
            #status didnt work
            print stdout, stderr

            #in the weeds, use ps aux or maybe use
            ps = subprocess.Popen('ps aux', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = ps.communicate()
            if self.service_name in stdout:
                return True
        return False

    def start_on_boot(self):
        if self.use_upstart:
            result = subprocess.Popen('/sbin/initctl show-config %s' % self.service_name, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = result.communicate()

            if self.service_name in stdout:
                if 'start on runlevel [2345]' in result:
                    return True
        else:
            result = subprocess.Popen('ls /etc/rc*.d/S**%s' % self.service_name, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = result.communicate()
            if self.service_name in stdout:
                return True
        return False

    def make_start_on_boot(self):
        if self.use_upstart:
            f = open('/etc/init/%s.conf' % self.service_name, 'r+')
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
            result = subprocess.Popen("update-rc.d %s defaults" % self.service_name, shell=True)
            result.wait()

    def satisfied(self):
        if self.is_running():
            if self.restart_on_boot:
                if self.start_on_boot():
                    return True
            else:
                return True
        return False

    def satisfy(self):
        if not self.is_running():
            self.start_service()
        if not self.start_on_boot() and self.restart_on_boot:
            self.make_start_on_boot()
