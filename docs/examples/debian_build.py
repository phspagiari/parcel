from fabric.api import env, task
from fabric.tasks import Task
from parcel import distro
from parcel import deploy

env.app_name = 'default_app_name'
env.run_deps = []
env.build_deps = []
env.base = None
env.path = '.'
env.arch = distro.Debian()

@task
def build():
    """Instantiate a Deployment object and
    build a Debian based package."""
    d = deploy.Deployment(app_name=env.app_name,
                          build_deps=env.build_deps,
                          run_deps=env.run_deps,
                          path=env.path,
                          base=env.base,
                          arch=env.arch
                          )
    d.prepare_app()
    d.build_deb()
