import sys
import os
import unittest2 as unittest

import mock
from mock import patch

from parcel.deploy import Deployment
from parcel.distro import Debian
from parcel.versions import Version
from parcel_mocks import run, local, rsync, version_mock, update_packages, build_deps, mock_put

# add mocks to this list if they should have reset called on them after tests
mocks_to_reset = [version_mock, update_packages, build_deps]



class TestDeploy(Deployment):
    """Simple test class for deploytment which  overrides __init__ so we are not calling remote host"""
    def __init__(self, app_name=None):
        self.app_name = app_name


class DeployTestSuite(unittest.TestCase):

    def setUp(self):
        self.app_name = "testapp"
        self.deploy = TestDeploy(self.app_name)

    def tearDown(self):
        for m in mocks_to_reset:
            m.reset_mock()
        
    def test_write_prerm_template(self):
        prerm_template = "Test rm template {app_name} and {lines}"

        # test with no prerm lines
        lines = []
        self.deploy.write_prerm_template(prerm_template)
        self.assertEquals(self.deploy.prerm, prerm_template.format(app_name=self.app_name, lines="\n        ".join(lines)))

        # test with prerm lines
        lines = ["test line 1", "test line 2"]
        self.deploy.add_prerm(lines)
        self.deploy.write_prerm_template(prerm_template)
        self.assertEquals(self.deploy.prerm, prerm_template.format(app_name=self.app_name, lines="\n        ".join(lines)))

    def test_write_postrm_template(self):
        postrm_template = "Test rm template {app_name} and {lines}"

        # test with no postrm lines
        lines = []
        self.deploy.write_postrm_template(postrm_template)
        self.assertEquals(self.deploy.postrm, postrm_template.format(app_name=self.app_name, lines="\n        ".join(lines)))

        # test with postrm lines
        lines = ["test line 1", "test line 2"]
        self.deploy.add_postrm(lines)
        self.deploy.write_postrm_template(postrm_template)
        self.assertEquals(self.deploy.postrm, postrm_template.format(app_name=self.app_name, lines="\n        ".join(lines)))

    def test_write_preinst_template(self):
        preinst_template = "Test postint template {app_name} and {lines}"

        # test with no preinst lines
        lines = []
        self.deploy.write_preinst_template(preinst_template)
        self.assertEquals(self.deploy.preinst, preinst_template.format(app_name=self.app_name, lines="\n        ".join(lines)))

        # test with preinst lines
        lines = ["test line 1", "test line 2"]
        self.deploy.add_preinst(lines)
        self.deploy.write_preinst_template(preinst_template)
        self.assertEquals(self.deploy.preinst, preinst_template.format(app_name=self.app_name, lines="\n        ".join(lines)))

    def test_write_postinst_template(self):
        postinst_template = "Test postint template {app_name} and {lines}"

        # test with no postinst lines
        lines = []
        self.deploy.write_postinst_template(postinst_template)
        self.assertEquals(self.deploy.postinst, postinst_template.format(app_name=self.app_name, lines="\n        ".join(lines)))

        # test with postinst lines
        lines = ["test line 1", "test line 2"]
        self.deploy.add_postinst(lines)
        self.deploy.write_postinst_template(postinst_template)
        self.assertEquals(self.deploy.postinst, postinst_template.format(app_name=self.app_name, lines="\n        ".join(lines)))

    def test_compile_python(self):
        pass

    def test_clear_py_files(self):
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


    @patch.multiple('parcel.deploy.deploy', run=local, put=mock_put)
    @patch.multiple('parcel.tools', run=local, rsync=rsync, put=mock_put)
    @patch('parcel.distro.run', local)
    @patch.multiple('parcel.distro.Debian', version=version_mock, update_packages=update_packages, build_deps=build_deps)
    def test_deployment(self):

        basepath = os.path.join(os.path.expanduser('~/'))
        d = Deployment('testapp', base=basepath)
        d.prepare_app()

        # check that sync_app worked
        self.assertTrue(os.path.exists(d.build_path))

        # check that virtualenv was built
        ve_path = os.path.join(d.build_path, d.virtual)
        self.assertTrue(os.path.exists(ve_path))

        # check we can add a file
        test_file = os.path.join(os.path.dirname(__file__),"data", "tip.tar.gz")
        d.add_to_root_fs(test_file, 'tip.tar.gz')
        dest_file = os.path.join(d.root_path, "tip.tar.gz")
        self.assertTrue(os.path.exists(dest_file))

        # check we can add data
        data = "this is some test data"
        d.add_data_to_root_fs(data, "test_data.txt")
        dest_file = os.path.join(d.root_path, "test_data.txt")
        self.assertTrue(os.path.exists(dest_file))
        with open(dest_file) as f:
            self.assertEquals(data, f.read())
            
