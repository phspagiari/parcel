from fabric.api import env, task
from fabric.tasks import Task
from parcel import distro
from parcel import deploy
from parcel.helpers import setup_centos

# NB: Centos will need to have EPEL activated and be using a more modern python than 2.4

env.app_name = 'default_app_name'
env.run_deps = []
env.build_deps = []
env.base = "/usr/local/webapps/"
env.path = '.'
env.arch = distro.centos

@task
def build():
    """Instantiate a Deployment object and
    build an RPM based package."""
    d = deploy.Deployment(app_name=env.app_name,
                          build_deps=env.build_deps,
                          run_deps=env.run_deps,
                          path=env.path,
                          base=env.base,
                          arch=env.arch
                          )

    d.prepare_app()
    d.build_package()

