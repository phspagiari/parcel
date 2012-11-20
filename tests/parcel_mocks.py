import os
import shutil
import tempfile
from functools import partial

import mock
from fabric.colors import blue
from fabric.api import local, lcd

from parcel.deploy import Deployment
from parcel.versions import Version


# fabric.api
run = mock.MagicMock(name='run')
local = partial(local, capture=True)
cd = lcd
with_settings = mock.MagicMock(name="with_settings")

def mock_put(local_path=None, remote_path=None, use_sudo=False, mirror_local_mode=False, mode=None):
    base_path = os.path.join(os.path.expanduser('~/'), Deployment.build_dir)
    if local_path and remote_path:
        shutil.copy(local_path, os.path.join(base_path, remote_path))

def mock_get(remote_path, local_path=None):
    if remote_path and local_path:
        shutil.copy(remote_path, local_path)

version_run = mock.MagicMock(name="version_run")  # used in test_distro

# used in test_deploy for test_build_deb
def build_deb_local():
    def func(command):
        if command.startswith('fpm'):
            tmpdir = tempfile.mkdtemp()
            test_deb = os.path.join(os.path.dirname(__file__),"data", "test.deb")
            deb = os.path.join(tmpdir, 'testapp_0.1.2_all.deb')
            shutil.copy(test_deb, deb)
            return 'Created deb package {{"path":"{0}"}}'.format(deb)
        return local(command)
    return func

# fabric.colors
green = mock.MagicMock(name='green')
blue = mock.MagicMock(name='blue')

# fabric.contrib.files
append = mock.MagicMock(name="append")

# rsync
rsync = mock.MagicMock(name='rsync')

# parcel.distro
update_packages = mock.MagicMock(name="update_packages")
build_deps =  mock.MagicMock(name="build_deps")

# parcel.versions
version_mock = mock.Mock(spec=Version)
version_mock.return_value = Version("0.1.1")

# rsync
def rsync(sources,dest,rsync_ignore=None,color_files=True):
    if type(sources)==str:
        sources = [sources]

    dest = os.path.join(os.path.expanduser('~/'), dest)

    print "DEST>>>>>>>>>>>>>>>>>" + dest

    local('mkdir -p "%s"'%dest)
    data = ''

    print sources
    print dest

    for s in sources:
        data += local('cp -R {0} {1}/'.format(s, dest))

    print data


    ## lines = data.splitlines()
    ## lines = lines[1:]
    ## i=0
    ## while lines[i]:
    ##     print blue(lines[i])
    ##     i+=1
    ## for line in lines[i:]:
    ##     print line     

    return

    command = []
    command.append('rsync')
    command.append('-av')
    command.extend("'%s'"%s for s in sources)
    command.append("'%s'"%(dest))
                
    if rsync_ignore:
        if os.path.isfile(rsync_ignore):
            command.append('--exclude-from=%s'%rsync_ignore)
    
    
    if not color_files:   
        return local(" ".join(command))

    print " ".join(command)
        
    data = local(" ".join(command),capture=True)
    lines = data.splitlines()
    lines = lines[1:]
    i=0
    while lines[i]:
        print blue(lines[i])
        i+=1
    for line in lines[i:]:
        print line     

# from fabric code, used to allow arbitrary attribute access
class _AttributeString(str):
    """
    Simple string subclass to allow arbitrary attribute access.
    """
    @property
    def stdout(self):
        return str(self)
