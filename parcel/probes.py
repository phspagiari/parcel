#
# probes
#

from fabric.api import put, cd, run

from .distro import debian

def deb_ls(deb):
    base_dir, src_dir, build_dir = debian._setup()
    put(deb,build_dir+"/"+deb)
    with cd(build_dir):
        run("dpkg --contents '%s'"%deb)
                
def deb_install(deb):
    base_dir, src_dir, build_dir = debian._setup()
    put(deb,build_dir+"/"+deb)
    with cd(build_dir):
        run("dpkg --install '%s'"%deb)
