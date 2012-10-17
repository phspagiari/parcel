import os.path

from fabric.api import settings, run, cd, lcd, put, get, local, env, with_settings
from fabric.contrib.files import sed

from . import versions

#
# Used to represent the remote build distribution
#

class Debian(object):
    def __init__(self):
        pass

    def update_packages(self):
        run("apt-get update -qq")

    def build_deps(self, deps):
        run("apt-get install -qq %s"%(' '.join(deps)))

    def version(self,package):
        return versions.Version(run('apt-cache 2>/dev/null show %s | sed -nr "s/^Version: ([0-9]+)(-.+)?/\\1/p"'%(package)))
		
	
