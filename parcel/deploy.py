import os.path

from fabric.api import settings, run, cd, lcd, put, get, local, env, with_settings
from fabric.contrib.files import sed

from . import versions
from . import distro

class Deployment(object):
    virtual = "vp"

    def __init__(self, app_name, build_deps=[], run_deps=[], path="./", base="/usr/local/webapps/",arch=distro.Debian()):
        """app_name: the package name
        build_deps: a list of packages that need to be installed to build the software
        run_deps: a list of packages that must be installed to run
        path: the directory to end up being the base level directory.
        arch: the architecture of the build host
        """
        # update and install missing build dependency packages
        self.arch = arch
        arch.update_packages()
        if build_deps:
            arch.build_deps(build_deps)
            
        # the version in the archives of this package if we have been built and uploaded before.
        self.version = arch.version(app_name)
        
        self.app_name = app_name
        self.run_deps = run_deps
        self.build_deps = build_deps
        self.pkg_name = app_name.lower()

        self.path = os.path.realpath(path)

	    # the path we build everything on on the remote host
        self.base_path = base+'%s-%s'%(             # '/ca/buildbot/build/%s-%s'
            self.pkg_name,
            self.version
        )
        self.app_path = os.path.join(self.base_path, app_name)
        
        #self.current_branch = local('git symbolic-ref HEAD', capture=True)[11:]

    def prepare_app(self, branch=None, requirements="requirements.txt"):
        """creates the necessary directories on the build server, checks out the desired branch (None means current),
        creates a virtualenv and populates it with dependencies from requirements.txt. 
        As a bonus it also fixes the shebangs ("#!") of all scripts in the virtualenv to point the correct Python path on the target system."""
        
        # theres no revision control atm so... just copy directory over
        #put(self.path, self.app_path)
        run('mkdir -p "%s"'%self.app_path)
        local("rsync -av '%s/' '%s@%s:%s'"%(self.path,env.user,env.host,self.app_path))
        
        self.venv_path = os.path.join(self.app_path, self.virtual)
        run('virtualenv %s'%(self.venv_path))
        if requirements:
            run('PIP_DOWNLOAD_CACHE="%s" %s install -r %s'%(
                self.arch.pip_download_cache,
	            os.path.join(self.venv_path, 'bin/pip'),
	            os.path.join(self.app_path, requirements))
            )
            
    def compile_python(self):
        # compile all python (with virtual python)
        run('%s -c "import compileall;compileall.compile_dir(\'%s\', force=1)"'%(os.path.join(self.venv_path, 'bin/python'),self.app_path))

    def clear_py_files():
        # clear all .py files
        run('find "%s" -name "*.py" -exec rm {} \;'%(self.app_path))

    def build_deb(self):
        """takes the whole app including the virtualenv, packages it using fpm and downloads it to my local host.
	    The version of the package is the build number - which is just the latest package version in our Ubuntu repositories plus one.
	    """
        with cd(self.base_path):
            self.run_deps.append('python-virtualenv')                   
            deps_str = '-d ' + ' -d '.join(self.run_deps)
            dirs_str = self.app_path
            #hooks_str = ' '.join(
            #    '{0} {1}'.format(opt, os.path.join('debian', fname))
            #    for opt, fname in [
            #        ('--before-remove', 'prerm'),
            #        ('--after-remove', 'postrm'),
            #        ('--before-install', 'preinst'),
            #        ('--after-install', 'postinst'),
            #    ]
            #    if os.path.exists(os.path.join('debian', fname))
            #)
            hooks_str = ''
            rv = run(
                'fpm -s dir -t deb -n {0.pkg_name} -v {0.version} '
                '-a all -x "*.git" -x "*.bak" -x "*.orig" {1} '
                '--description "Automated build. '
                'No Version Control." '
                '{2} {3}'
                .format(self, hooks_str, deps_str, dirs_str)
            )

            filename = rv.split('"')[-2]
            get(filename, './')
            run("rm '%s'"%filename)
