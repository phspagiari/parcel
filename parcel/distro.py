import os.path

from fabric.api import settings, run, cd, lcd, put, get, local, env, with_settings

from . import versions
from .cache import cache

#
# Used to represent the remote build distribution
#

class Distro(object):
    space = '.parcel-build-temp'
    pip_download_cache = '/tmp/pip-download-cache/'

    def __init__(self):
        pass

    def _cleanup(self):
        run("rm -rf '%s'"%self.space)  

    def _setup(self):
        # first cleanup any broken stale previous builds
        self._cleanup()

        # make fresh directories
        base_dir = self.mkdir(self.space)
        src_dir = self.mkdir(self.space+"/src")
        build_dir = self.mkdir(self.space+"/build")
        return base_dir, src_dir, build_dir
        
    @property
    def build_base(self):
        return '/tmp/'
        
    def mkdir(self, remote):
        return run('mkdir "%s" && cd "%s" && pwd'%(remote,remote))

    def update_packages(self):
        with settings(user='root'):
            run("apt-get update -qq")

    def build_deps(self, deps):
        with settings(user='root'):
            run("apt-get install -qq %s"%(' '.join(deps)))

    def version(self,package):
        """Look at the debian apt package system for a package with this name and return its version.
        Return None if there is no such package.
        """
        with settings(warn_only=True):
            vstring = run('apt-cache show %s 2>/dev/null | sed -nr "s/^Version: ([0-9]+)(-.+)?/\\1/p"'%(package))
            if vstring.return_code:
                # error fetching package info. Assume there is no such named package. Return None
                return None
            return versions.Version(vstring)
	
    def push_files(self,pathlist,dst):
        for path in pathlist:
            put(path, os.path.join(dst,os.path.basename(path)))
    	
    def check(self):
        """Check the remote build host to see if the relevant software to build packages is installed"""
        with settings(warn_only=True):
            # check for fpm
            result = run('which fpm')
            if result.return_code:
                raise Exception("Build host does not have fpm installed and on the executable path")
            
            # check for checkinstall
            result = run('which checkinstall')
            if result.return_code:
                raise Exception("Build host does not have checkinstall installed and on the executable path")
        
    def setup(self):
        """This method should set up a remote box for parcel package building.
        It should install fpm.
        """
        raise NotImplementedError

    
class Debian(Distro):

    def setup(self):
        """this method sets up a remote debian box for parcel package building.
        Installs fpm, easyinstall and some libraries

        there must be a a directory called archives
        and in it a file rubygems-1.8.24.tgz

        TODO: remove this requirement. get the file we need.
        """
        with settings(user='root'):
            self.build_deps(['libyaml-ruby','libzlib-ruby','ruby','ruby-dev','checkinstall'])

            base_dir, src_dir, build_dir = self._setup()
            
            # get rubygems and copy it across
            path = cache.get("http://production.cf.rubygems.org/rubygems/rubygems-1.8.24.tgz")
            self.push_files([path],src_dir)
            filename = os.path.basename(path)
            
            with cd(build_dir):
                run("tar xvfz ../src/%s"%filename)
            with cd(build_dir+"/rubygems-1.8.24"):
                run("ruby setup.rb")
            run("gem1.8 install fpm")


class Ubuntu(Distro):

    def setup(self):
        """this method sets up a remote ubuntu box for parcel package building.
        Installs fpm and also rubygems if not present.
        """
        with settings(user='root'):
            run("apt-get install rubygems -y")
            run("gem install fpm")


# the distribution module instances
debian = Debian()
ubuntu = Ubunut()
