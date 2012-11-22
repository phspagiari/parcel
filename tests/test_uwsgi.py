import sys
import os
import unittest2 as unittest
from functools import partial
import mock
from mock import patch

from parcel.deploy import uWSGI
from parcel.distro import Debian
from parcel.versions import Version
from parcel_mocks import (run, local, rsync, version_mock, update_packages,
                          build_deps, mock_put, mock_get, lcd, build_deb_local)

# add mocks to this list if they should have reset called on them after tests
mocks_to_reset = [version_mock, update_packages, build_deps, run]

class DeployTestSuite_AppBuild(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        for m in mocks_to_reset:
            m.reset_mock()

    @patch('parcel.deploy.uwsgi.run', local)
    @patch('parcel.deploy.deploy.run', local)
    @patch.multiple('parcel.tools', run=local, rsync=rsync, put=mock_put)
    @patch('parcel.distro.run', local)
    @patch.multiple('parcel.distro.Debian', version=version_mock, update_packages=update_packages, build_deps=build_deps)
    def test_init(self):
        basepath = os.path.join(os.path.expanduser('~/'))
        d = uWSGI('testapp', base=basepath)
        d.venv_root = 'test_path'
        d.add_supervisord_uwsgi_service('testapp')
        # test dirs present and have content
        self.assertTrue(os.path.exists(os.path.join(os.path.expanduser('~/'), d.root_path, 'etc/supervisor/conf.d/uwsgi.conf')))
        self.assertTrue(os.path.exists(os.path.join(os.path.expanduser('~/'), d.root_path, 'etc/uwsgi/testapp.uswgi')))

