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
def build_for_uwsgi():
    """Instantiate a Deployment object and build a Debian based package for
    uwsgi deployment."""
    assert hasattr(env, 'service_name'), "You need to set env.service_name"
    assert hasattr(env, 'service_port'), "You need to set env.service_port"
    d = deploy.uWSGI(app_name=env.app_name,
                     build_deps=env.build_deps,
                     run_deps=env.run_deps,
                     path=env.path,
                     base=env.base,
                     arch=env.arch
                     )
    d.prepare_app()
    d.add_supervisord_uwsgi_service(env.service_name, env.service_port)
    d.build_deb()
