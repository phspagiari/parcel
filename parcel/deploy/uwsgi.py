# -*- coding: utf-8 -*-
import os.path

from fabric.api import settings, run, cd, lcd, put, get, local, env, with_settings
from fabric.colors import green

from .. import versions
from .. import distro
from .. import tools
from .. import defaults
from .deploy import Deployment

##
## supervisord + uwsgi container deployment
##
class uWSGI(Deployment):
    def add_supervisord_uwsgi_service(self,program_name,port=80,user=None):
        # add the config file
        self.add_data_to_root_fs("""[program:%s]
command=/usr/local/bin/uwsgi --ini=/etc/uwsgi/%s.uswgi
process_name=%s
numprocs=1
directory=/tmp
umask=022
priority=999
autostart=true
autorestart=true
startsecs=10
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=10
user=%s
redirect_stderr=false
stdout_logfile=/var/log/%s.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
serverurl=AUTO
"""%(program_name, program_name, program_name, user or env.user, program_name), "etc/supervisor/conf.d/uwsgi.conf")
        
        # add the postinstall lines
        self.add_postinst(['/etc/init.d/supervisor stop','sleep 1','/etc/init.d/supervisor start'])
        
        # add the prerm lines
        self.add_prerm(['supervisorctl stop %s'%program_name])
        
        # add the supervisor install dependency
        self.run_deps.append('supervisor')              # also uwsgi on systems with it in packaging (redhat? ubuntu?)

        # write out our uwsgi config
        self.write_uwsgi_file(port=port, path=self.app_path, module='%s.wsgi'%(self.app_name), program_name=program_name)
        
        # also in postinst is to start this app
        self.add_postinst(['supervisorctl start %s'%program_name])
        
    def write_uwsgi_file(self,port,path,module,program_name):
        data = """[uwsgi]
# set the http port
http = :%d
# change to django project directory
chdir = %s/%s
# load django
module = %s
home = %s
"""%(port,path,self.app_name,module,self.venv_root)
        self.add_data_to_root_fs(data,'/etc/uwsgi/%s.uswgi'%program_name)
