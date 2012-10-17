import os.path

from fabric.api import settings, run, cd, lcd, put, get, local, env, with_settings
from fabric.contrib.files import sed

from . import versions

class Deployment(object):
    def __init__(self, app_name, build_deps=[], run_deps=[]):
        with settings(user='root'):
            run('apt-get update -qq')
            if build_deps:
                run('apt-get install -qq %s'%(' '.join(build_deps)))
            v = run(
                'apt-cache 2>/dev/null show %s | sed -nr "s/^Version: ([0-9]+)(-.+)?/\\1/p"'%(app_name)
            )
            self.version = versions.Version(v)

        self.app_name = app_name
        self.run_deps = run_deps
        self.build_deps = build_deps
        self.pkg_name = ('ca-' + app_name).lower()

		# the path we build everything on on the remote host
        self.base_path = '/ca/buildbot/build/%s-%s'%(
            self.pkg_name,
            self.version
        )
        self.app_path = os.path.join(self.base_path, 'ca', app_name)
        #self.current_branch = local('git symbolic-ref HEAD', capture=True)[11:]

	@with_settings(user='buildbot')
	def prepare_app(self, branch=None):
	    """creates the necessary directories on the build server, checks out the desired branch (None means current),
		creates a virtualenv and populates it with dependencies from requirements.txt. 
		As a bonus it also fixes the shebangs ("#!") of all scripts in the virtualenv to point the correct Python path on the target system."""
	    run('rm -rf ~/build/ca-%s*'%(self.app_name))
	    self.src_path = os.path.join(self.app_path, self.app_name)
	    if not branch:
	        self.git_branch = local('git symbolic-ref HEAD', capture=True)[11:]
	    else:
	        self.git_branch = branch
	    local('git push origin ' + self.git_branch)
	    git_clone(self.app_name, self.git_branch, self.src_path)
	    with cd(self.src_path):
	        self.git_commit = run('git rev-parse --short HEAD')

	    self.venv_path = os.path.join(self.app_path, 'venv')
	    run('virtualenv %s'%(self.venv_path))
	    run('%s install -r %s'%(
	        os.path.join(self.venv_path, 'bin/pip'),
	        os.path.join(self.src_path, 'requirements.txt'))
	    )
	    # fix shebangs
	    target_venv_bin = os.path.join('/ca', self.app_name, 'venv/bin')
	    with cd(os.path.join(self.venv_path, 'bin')):
	        for script in run('ls').split():
	            sed(
	                script,
	                '#!' + os.path.join(self.venv_path, 'bin/(.+)'),
	                '#!' + os.path.join(target_venv_bin, r'\1')
	            )

    @with_settings(user='buildbot')
    def build_deb(self, dirs=['ca']):
        """takes the whole app including the virtualenv, packages it using fpm and downloads it to my local host.
		The version of the package is the build number - which is just the latest package version in our Ubuntu repositories plus one.
		"""
        with cd(self.base_path):
            run('mv {} .'.format(os.path.join(self.src_path, 'debian')))
            self.run_deps.append('python-virtualenv')
            deps_str = '-d ' + ' -d '.join(self.run_deps)
            dirs_str = ' '.join(dirs)
            hooks_str = ' '.join(
                '{} {}'.format(opt, os.path.join('debian', fname))
                for opt, fname in [
                    ('--before-remove', 'prerm'),
                    ('--after-remove', 'postrm'),
                    ('--before-install', 'preinst'),
                    ('--after-install', 'postinst'),
                ]
                if os.path.exists(os.path.join('debian', fname))
            )
            rv = run(
                'fpm -s dir -t deb -n {0.pkg_name} -v {0.version} '
                '-a all -x "*.git" -x "*.bak" -x "*.orig" {1} '
                '--description "Automated build. '
                'Branch: {0.git_branch} Commit: {0.git_commit}" '
                '{2} {3}'
                .format(self, hooks_str, deps_str, dirs_str)
            )

            get(rv.split('"')[-2], 'debian/%(basename)s')	
