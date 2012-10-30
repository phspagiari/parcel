#
# probes
#

from fabric.api import put, cd, run, task
from fabric.colors import green

from .distro import debian
from .tools import read_contents_from_remote, quiet_run, rsync

@task
def deb_ls(deb):
    """List the contents of the given package."""
    base_dir, src_dir, build_dir = debian._setup(clean=False)
    #put(deb,build_dir+"/"+deb)
    rsync(deb,build_dir)
    with cd(build_dir):
        print green(quiet_run("dpkg --contents '%s'"%deb))

@task                
def deb_install(deb):
    """Install the given package."""
    base_dir, src_dir, build_dir = debian._setup(clean=False)
    #put(deb,build_dir+"/"+deb)
    rsync(deb,build_dir)
    with cd(build_dir):
        print green(run("dpkg --install '%s'"%deb))

@task
def deb_control(deb):
    base_dir, src_dir, build_dir = debian._setup(clean=False)
    #put(deb,build_dir+"/"+deb)
    rsync(deb,build_dir)
    with cd(build_dir):
        run("dpkg --control '%s'"%deb)
        files = run("find DEBIAN -type f -print").strip().splitlines()
        for fname in files:
            data = read_contents_from_remote(fname)
            print green(fname,True)
            print green("="*len(fname),True)
            print green(data)

@task
def deb_tree(deb):
    """Output tree listing of package contents."""
    base_dir, src_dir, build_dir = debian._setup(clean=False)
    #put(deb,build_dir+"/"+deb)
    rsync(deb,build_dir)
    with cd(build_dir):
        run("dpkg --extract '%s' root"%deb)
        with cd('root'):
            print green(quiet_run("tree"))
        
