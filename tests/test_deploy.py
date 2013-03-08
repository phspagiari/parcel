import sys
import os
import unittest2 as unittest
from functools import partial
import shutil
import mock
from mock import patch

from parcel.deploy import Deployment
from parcel.distro import Debian, Centos, centos
from parcel.versions import Version
from parcel_mocks import (run, rsync, version_mock, update_packages,
                          build_deps, mock_put, mock_get, lcd, mock_local)

# add mocks to this list if they should have reset called on them after tests
mocks_to_reset = [version_mock, update_packages, build_deps, run]

# set build dir to a test value so we can remove it cleanly
Deployment.build_dir = ".parcel_test"


class TestDeploy(Deployment):
    """Simple test class for deploytment which  overrides __init__ so we are not calling remote host"""
    def __init__(self, app_name=None):
        self.app_name = app_name


class DeployTestSuite(unittest.TestCase):

    def setUp(self):
        self.app_name = "testapp"
        self.deploy = TestDeploy(self.app_name)
        
    def tearDown(self):
        test_build_dir = os.path.join(os.path.expanduser('~/'), '.parcel_test') 
        shutil.rmtree(test_build_dir, True)
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


class DeployTestSuite_AppBuild(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        test_build_dir = os.path.join(os.path.expanduser('~/'), '.parcel_test') 
        shutil.rmtree(test_build_dir, True)
        for m in mocks_to_reset:
            m.reset_mock()
            
        # remove the deb we may have built
        deb = os.path.join(os.path.dirname(__file__),"data", "testapp_0.1.2_all.deb")
        if os.path.exists(deb):
            os.unlink(deb)

    @patch('parcel.deploy.deploy.run', mock_local())
    @patch.multiple('parcel.tools', run=mock_local(), rsync=rsync)
    @patch('parcel.distro.run', mock_local())
    @patch.multiple('parcel.distro.Debian', version=version_mock, update_packages=update_packages, build_deps=build_deps)
    def test_init(self):
        basepath = os.path.join(os.path.expanduser('~/'))
        d = Deployment('testapp', base=basepath)
        d.prepare_app()
        
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

        # now check with no basepath
        d = Deployment('testapp')
        self.assertTrue(basepath in d.build_path)
        
        # now check with basepath without initial slash
        basepath = os.path.join(os.path.dirname(__file__))
        d = Deployment('testapp', base=basepath[1:])
        self.assertTrue(basepath in d.build_path)
        
    @patch('parcel.deploy.deploy.run', mock_local())
    @patch.multiple('parcel.tools', run=mock_local(), rsync=rsync)
    @patch('parcel.distro.run', mock_local())
    @patch.multiple('parcel.distro.Debian', version=version_mock, update_packages=update_packages, build_deps=build_deps)
    def test_init_with_deps(self):
        basepath = os.path.join(os.path.expanduser('~/'))
        d = Deployment('testapp', base=basepath, build_deps=['requests'])
        d.prepare_app()

        # if we supply build_deps then this should be called
        build_deps.assert_called_once()


    @patch('parcel.deploy.deploy.run', mock_local())
    @patch.multiple('parcel.tools', run=mock_local(), rsync=rsync)
    @patch('parcel.distro.run', mock_local())
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


    @patch.multiple('parcel.deploy.deploy', run=mock_local(), put=mock_put, cd=lcd, get=mock_get)
    @patch.multiple('parcel.tools', run=mock_local(), rsync=rsync, put=mock_put)
    @patch('parcel.distro.run', mock_local())
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

        # now check with a leading slash
        d.add_to_root_fs(test_file, '/tip.tar.gz')
        dest_file = os.path.join(d.root_path, "tip.tar.gz")
        self.assertTrue(os.path.exists(dest_file))

        # check we can add data
        data = "this is some test data"
        d.add_data_to_root_fs(data, "test_data.txt")
        dest_file = os.path.join(d.root_path, "test_data.txt")
        self.assertTrue(os.path.exists(dest_file))
        with open(dest_file) as f:
            self.assertEquals(data, f.read())

        # try the same with a leading slash
        data = "this is some test data"
        d.add_data_to_root_fs(data, "/test_data.txt")
        dest_file = os.path.join(d.root_path, "test_data.txt")
        self.assertTrue(os.path.exists(dest_file))
        with open(dest_file) as f:
            self.assertEquals(data, f.read())

        # check we can compile python files
        d.compile_python()
        dest_file = os.path.join(d.build_path, 'data', 'hello.pyc')
        self.assertTrue(os.path.exists(dest_file))

        # check we can clear .py and just leave .pyc files
        d.clear_py_files()
        dest_file = os.path.join(d.build_path, 'data', 'hello.py')
        self.assertFalse(os.path.exists(dest_file))


    @patch.multiple('parcel.deploy.deploy', run=mock_local(), put=mock_put, cd=lcd, get=mock_get)
    @patch.multiple('parcel.tools', run=mock_local(), rsync=rsync, put=mock_put)
    @patch.multiple('parcel.distro', run=mock_local(), get=mock_get)
    @patch.multiple('parcel.distro.Debian', version=version_mock, update_packages=update_packages, build_deps=build_deps)
    def test_build_deb(self):
        basepath = os.path.join(os.path.expanduser('~/'))
        d = Deployment('testapp', base=basepath)
        d.root_path = os.path.join(basepath, '.parcel')
        d.prepare_app()
        
        # test build, will not actually call fpm
        d.build_package()
        dest_file = os.path.join(os.path.dirname(__file__),"data", "testapp_0.1.2_all.deb")
        self.assertTrue(os.path.exists(dest_file))
        os.unlink(dest_file)

        # now do it without templates to exercise those paths
        d = Deployment('testapp', base=basepath)
        d.root_path = os.path.join(basepath, '.parcel_test')
        d.build_package(templates=False)
        dest_file = os.path.join(os.path.dirname(__file__),"data", "testapp_0.1.2_all.deb")
        self.assertTrue(os.path.exists(dest_file))
        os.unlink(dest_file)

        # now set some prerm etc directly and check
        d = Deployment('testapp', base=basepath)
        d.root_path = os.path.join(basepath, '.parcel_test')
        lines = ['test line one', 'test line two']
        d.prerm = " ".join(lines)
        d.postrm = " ".join(lines)
        d.preinst = " ".join(lines)
        d.postinst = " ".join(lines)
        d.build_package()
        dest_file = os.path.join(os.path.dirname(__file__),"data", "testapp_0.1.2_all.deb")
        self.assertTrue(os.path.exists(dest_file))
        os.unlink(dest_file)


    @patch('parcel.deploy.deploy.run', run)
    @patch('parcel.distro.run', mock_local())
    @patch.multiple('parcel.distro.Debian', version=version_mock, update_packages=update_packages)
    def test_add_venv_with_requirements(self):
        basepath = os.path.join(os.path.expanduser('~/'))
        d = Deployment('testapp', base=basepath)
        req_file = os.path.join(os.path.dirname(__file__),"data", "requirements_test")

        # call _add_venv directly so we can just mock that run out
        d._add_venv(requirements=req_file)
        self.assertTrue('PIP_DOWNLOAD_CACHE' in run.call_args[0][0])


class DeployTestSuite_CentosRPMAppBuild(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        test_build_dir = os.path.join(os.path.expanduser('~/'), '.parcel_test') 
        shutil.rmtree(test_build_dir, True)
        for m in mocks_to_reset:
            m.reset_mock()
            
        # remove the deb we may have built
        deb = os.path.join(os.path.dirname(__file__),"data", "testapp_0.1.1-1.noarch.rpm")
        if os.path.exists(deb):
            os.unlink(deb)


    # centos tests
    @patch.multiple('parcel.deploy.deploy', run=mock_local(), put=mock_put, cd=lcd, get=mock_get)
    @patch.multiple('parcel.tools', run=mock_local(), rsync=rsync, put=mock_put)
    @patch.multiple('parcel.distro', run=mock_local(), get=mock_get)
    @patch.multiple('parcel.distro.Centos', version=version_mock, update_packages=update_packages, build_deps=build_deps)
    def test_build_rpm(self):
        basepath = os.path.join(os.path.expanduser('~/'))
        d = Deployment('testapp', base=basepath, arch=centos)
        d.root_path = os.path.join(basepath, '.parcel')
        d.prepare_app()
        
        # test build, will not actually call fpm
        d.build_package()
        dest_file = os.path.join(os.path.dirname(__file__),"data", "testapp_0.1.1-1.noarch.rpm")
        print dest_file
        self.assertTrue(os.path.exists(dest_file))
        os.unlink(dest_file)

