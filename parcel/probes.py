#
# probes
#

from fabric.api import put, cd, run

from .distro import Debian

def deb_ls(deb):
    base_dir, src_dir, build_dir = Debian()._setup()
    put(deb,build_dir+"/"+deb)
    with cd(build_dir):
        run("dpkg --contents '%s'"%deb)
                
