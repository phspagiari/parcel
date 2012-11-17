import sys
import os
import unittest2 as unittest

import mock
from mock import patch

from parcel.deploy import Deployment
from parcel.distro import Debian
from parcel.versions import Version
from parcel_mocks import run, local, rsync, version_mock, update_packages, build_deps

# add mocks to this list if they should have reset called on them after tests
mocks_to_reset = [version_mock, update_packages, build_deps]



class TestDeploy(Deployment):
    """Simple test class for deploytment which  overrides __init__ so we are not calling remote host"""
    def __init__(self, app_name=None):
        self.app_name = app_name


class DeployTestSuite(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        for m in mocks_to_reset:
            m.reset_mock()
        

    def test_write_prerm_template(self):
        prerm_template = "Test rm template {app_name} and {lines}"

        # test with no prerm lines
        app_name = "testapp"
        lines = []
        d = TestDeploy(app_name)
        d.write_prerm_template(prerm_template)
        self.assertEquals(d.prerm, prerm_template.format(app_name=app_name, lines="\n        ".join(lines)))

        # test with prerm lines
        app_name = "testapp"
        lines = ["test line 1", "test line 2"]
        d = TestDeploy(app_name)
        d.add_prerm(lines)
        d.write_prerm_template(prerm_template)
        self.assertEquals(d.prerm, prerm_template.format(app_name=app_name, lines="\n        ".join(lines)))

    def test_write_postinst_template(self):

        postinst_template = "Test postint template {app_name} and {lines}"

        # test with no postinst lines
        app_name = "testapp"
        lines = []
        d = TestDeploy(app_name)
        d.write_postinst_template(postinst_template)
        self.assertEquals(d.postinst, postinst_template.format(app_name=app_name, lines="\n        ".join(lines)))

        # test with postinst lines
        app_name = "testapp"
        lines = ["test line 1", "test line 2"]
        d = TestDeploy(app_name=app_name)
        d.add_postinst(lines)
        d.write_postinst_template(postinst_template)
        self.assertEquals(d.postinst, postinst_template.format(app_name=app_name, lines="\n        ".join(lines)))


    def test_add_to_root_fs(self):
        pass

    def test_add_data_to_root_fs(self):
        pass

    def test_compile_python(self):
        pass

    def test_clear_py_files(self):
        pass

    def test_add_prerm(self):
        pass

    def test_add_postrm(self):
        pass

    def test_add_preinst(self):
        pass

    def test_add_postinst(self):
        pass

    def test_build_deb(self):
        pass



class DeployTestSuite2(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        for m in mocks_to_reset:
            m.reset_mock()


    @patch('parcel.deploy.deploy.run', local)
    @patch.multiple('parcel.tools', run=local, rsync=rsync)
    @patch('parcel.distro.run', local)
    @patch.multiple('parcel.distro.Debian', version=version_mock, update_packages=update_packages, build_deps=build_deps)
    def test_init(self):
        basepath = os.path.join(os.path.expanduser('~/'))
        d = Deployment('testapp', base=basepath)

        # version
        self.assertEquals(d.version.version, Version('0.1.2').version)

        # app_name
        self.assertEquals(d.app_name, 'testapp')

        # check that that a build_dir has been set up
        build_dir = os.path.join(basepath, d.build_dir)
        self.assertTrue(os.path.exists(build_dir))

        # no deps to install
        self.assertFalse(build_deps.called)

        # update_packages
        update_packages.assert_called_once()


    @patch('parcel.deploy.deploy.run', local)
    @patch.multiple('parcel.tools', run=local, rsync=rsync)
    @patch('parcel.distro.run', local)
    @patch.multiple('parcel.distro.Debian', version=version_mock, update_packages=update_packages, build_deps=build_deps)
    def test_init_with_deps(self):

        basepath = os.path.join(os.path.expanduser('~/'))
        d = Deployment('testapp', base=basepath, build_deps=['requests'])
        d.prepare_app()

        # if we supply build_deps then this should be called
        build_deps.assert_called_once()


    @patch('parcel.deploy.deploy.run', local)
    @patch.multiple('parcel.tools', run=local, rsync=rsync)
    @patch('parcel.distro.run', local)
    @patch.multiple('parcel.distro.Debian', version=version_mock, update_packages=update_packages, build_deps=build_deps)
    def test_prepare_app(self):

        basepath = os.path.join(os.path.expanduser('~/'))
        d = Deployment('testapp', base=basepath)
        d.prepare_app()

        # check that sync_app worked
        self.assertTrue(os.path.exists(d.build_path))

        # check that virtualenv was built
        ve_path = os.path.join(d.build_path, d.virtual)
        self.assertTrue(os.path.exists(ve_path))





