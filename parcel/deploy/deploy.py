# -*- coding: utf-8 -*-
import os.path

from fabric.api import settings, run, cd, lcd, put, get, local, env, with_settings
from fabric.colors import green

from .. import versions
from .. import distro
from .. import tools
from .. import defaults

class Deployment(object):
    """The core :class:`Deployment <Deployment>` object. All Fabric tasks built with
    Parcel will probably use this an instance of this class.
    """

    virtual = "vp"
    build_dir = '.parcel'
    
    # these are the full text versions of the scripts
    prerm = None
    postrm = None
    preinst = None
    postinst = None
    
    # these are a list representation of commands to go into the scripts
    # if the control script templating is used
    prerm_lines = []
    postrm_lines = []
    preinst_lines = []
    postinst_lines = []
    
    def __init__(self, app_name, build_deps=[], run_deps=[], path=".", base=None,arch=distro.Debian(), version=None):

        #: The architecture of the build host. This should be a :class:`Distro <Distro>` object. 
        self.arch = arch
        remotehome = run('echo $HOME').strip()

        # if path isn't set, make it the home directory of the build user
        if base is None:
            base = remotehome
        elif not base.startswith('/'):
            base = os.path.join(remotehome, base)
        
        # update and install missing build dependency packages
        arch.update_packages()
        if build_deps:
            arch.build_deps(build_deps)
            
        # the version in the archives of this package if we have been built and uploaded before.
        self.version = arch.version(app_name).next() if version is None else versions.Version(version)
        
        #: The name of the resulting package.
        self.app_name = app_name

        #: A list of packages that must be installed to run the resulting package.
        self.run_deps = run_deps

        #: A list of packages that need to be installed to build the software.
        self.build_deps = build_deps
        self.pkg_name = app_name.lower()

        #: The directory that will be used as the base level directory.
        self.path = os.path.realpath(path)

	    #: Location of files during build on build host. Default is user's home directory.
        #: If path is relative, it's relative to the remote user's home directory. If the path is absolute,
        #: it's used as is.
        self.base_path = os.path.join(remotehome,self.build_dir)

        self.pkg_name = app_name.lower()
        self.root_path = os.path.join(self.base_path,"root")                    # where the final root fs is located
        
        # the path the app will be installed into
        self.app_path = os.path.join(base,'%s-%s'%(self.pkg_name,self.version))
        
        # the build path
        self.build_path = os.path.join(self.root_path, self.app_path[1:])                # cut the first / off app_path

        print "ROOT_PATH", self.root_path
        print "BASE_PATH",self.base_path
        print "APP PATH",self.app_path
        print "BUILD PATH",self.build_path

        self._clean()
        
    def prepare_app(self, branch=None, requirements="requirements.txt"):
        """Creates the necessary directories on the build server, checks out the desired branch (None means current),
        creates a virtualenv and populates it with dependencies from requirements.txt. 
        As a bonus it also fixes the shebangs (#!) of all scripts in the virtualenv to point the correct Python path
        on the target system."""
        self._sync_app()
        self._add_venv(requirements)
            
    def add_to_root_fs(self,localfile,remotepath):
        """Add a local file to the root package path.
        If remote path ends in /, the filename is copied into
        that directory. If the remote path doesn't end in /, it represents
        the final filename.
        """
        while remotepath[0]=='/':
            remotepath=remotepath[1:]
        put(localfile,os.path.join(self.root_path,remotepath))

    def add_data_to_root_fs(self, data, remotepath):
        """Copies data in file on remotepath (relative to final root)"""
        while remotepath[0]=='/':
            remotepath=remotepath[1:]
        tools.write_contents_to_remote(data,os.path.join(self.root_path, remotepath))
            
    def compile_python(self):
        # compile all python (with virtual python)
        vpython_path = os.path.join(self.venv_path,'bin/python')
        command = '%s -c "import compileall;compileall.compile_dir(\'%s\', force=1)"'%(vpython_path, self.build_path)
        run(command)

    def clear_py_files(self):
        # clear all .py files
        run('find "%s" -name "*.py" -exec rm {} \;'%(self.build_path))

    def add_prerm(self, lines):
        """Add lines to the prerm file"""
        self.prerm_lines.extend(lines)
        
    def add_postrm(self, lines):
        """Add lines to the postrm file"""        
        self.postrm_lines.extend(lines)
        
    def add_preinst(self, lines):
        """Add lines to the preinst file"""        
        self.preinst_lines.extend(lines)
        
    def add_postinst(self, lines):
        """Add lines to the postinst file"""
        self.postinst_lines.extend(lines)
        
    def build_deb(self, templates=True):
        """Takes the whole app including the virtualenv, packages it using fpm and downloads it to the local host.
	    The version of the package is the build number - which is just the latest package version in our Ubuntu repositories plus one.
	    """

        # add install and remove templates, use defaults if not supplied
        if templates:
            if not self.prerm:
                self.write_prerm_template(defaults.prerm_template)
            if not self.postrm:
                self.write_postrm_template(defaults.postrm_template)
            if not self.preinst:
                self.write_preinst_template(defaults.preinst_template)
            if not self.postinst:
                self.write_postinst_template(defaults.postinst_template)
        
        with cd(self.base_path):
            deps_str = '-d ' + ' -d '.join(self.run_deps)
            dirs_str = '.'
            
            if self.prerm or self.postrm or self.preinst or self.postinst:
                run("rm -rf debian && mkdir -p debian")
            
            # render pre/posts
            hooks = []
            if self.prerm:
                prerm = self.prerm.format(self)
                tools.write_contents_to_remote(prerm,'debian/prerm')
                hooks.extend(['--before-remove', '../debian/prerm'])
                
            if self.postrm:
                postrm = self.postrm.format(self)
                tools.write_contents_to_remote(postrm,'debian/postrm')
                hooks.extend(['--after-remove', '../debian/postrm'])
            
            if self.preinst:
                tools.write_contents_to_remote(self.preinst,'debian/preinst')
                hooks.extend(['--before-install', '../debian/preinst'])
            
            if self.postinst:
                tools.write_contents_to_remote(self.postinst,'debian/postinst')
                hooks.extend(['--after-install', '../debian/postinst'])
            
            hooks_str = ' '.join(hooks)
            
        with cd(self.root_path):
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
            print green(os.path.basename(filename))

    def write_prerm_template(self, template):
        """Take a template prerm script and format it with appname and prerm_lines
        If you call this function you must supply a template string that includes {app_name} and {lines}."""
        self.prerm = template.format(app_name=self.app_name, lines="\n        ".join(self.prerm_lines))

    def write_postrm_template(self, template):
        """Take a template postrm script and format it with appname and postrm_lines
        If you call this function you must supply a template string that includes {app_name} and {lines}."""
        self.postrm = template.format(app_name=self.app_name, lines="\n        ".join(self.postrm_lines))

    def write_preinst_template(self, template):
        """Take a template preinst script and format it with appname and preinst_lines
        If you call this function you must supply a template string that includes {app_name} and {lines}."""
        self.preinst = template.format(app_name=self.app_name, lines="\n        ".join(self.preinst_lines))

    def write_postinst_template(self, template):
        """Take a template postinst script and format it with appname and postinst_lines
        If you call this function you must supply a template string that includes {app_name} and {lines}."""
        self.postinst = template.format(app_name=self.app_name, lines="\n        ".join(self.postinst_lines))

    def _clean(self):
        """Make sure the root filesystem directory is empty."""
        run('rm -rf "%s"'%self.root_path)
        
    def _sync_app(self):
        """There is no revision control at the moment so... just copy directory over."""
        print self.build_path
        tools.rsync([self.path+'/'],self.build_path,rsync_ignore='.rsync-ignore')

    def _add_venv(self,requirements="requirements.txt"):
        """Builds virtualenv on remote host and installs from requirements.txt.
        
        :param requirements: The name of the requirements.txt file.
        """
        self.venv_path = os.path.join(self.build_path, self.virtual)
        run('virtualenv %s'%(self.venv_path))
        if requirements and os.path.exists(requirements):
            run('PIP_DOWNLOAD_CACHE="%s" %s install -r %s'%(
                self.arch.pip_download_cache,
	            os.path.join(self.venv_path, 'bin/pip'),
	            os.path.join(self.build_path, requirements))
            )
            
        # venv_root is final path
        self.venv_root = os.path.join(self.app_path, self.virtual)
        
        # lets make sure this venv is relinked on installation
        self.add_postinst(['virtualenv "%s"'%self.venv_root])
        
        # and we have the virtualenv executable
        self.run_deps.append('python-virtualenv')
