import sys
import unittest2 as unittest
import mock
from mock import patch

from parcel.deploy import Deployment
from parcel.distro import Debian
from parcel.versions import Version
from mocks import run, rsync

version_mock = mock.Mock(spec=Version)


class TestDeploy(Deployment):
    """Simple test class for deploytment which  overrides __init__ so we are not calling remote host"""
    def __init__(self, app_name=None):
        self.app_name = app_name


class DeployTestSuite(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        run.reset_mock()
        

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



class DeployTestSuite2(unittest.TestCase):

    def setUp(self):
        self.saved_side_effect = run.side_effect
        run.reset_mock()

    def tearDown(self):
        run.reset_mock()
        
        #restore default side_effect
        run.side_effect = self.saved_side_effect

    @patch('parcel.deploy.deploy.run', mock.MagicMock(name="run"))
    @patch('parcel.tools.run' , mock.MagicMock(name="run"))
    @patch('parcel.tools.rsync', rsync)    
    @patch('parcel.distro.run', mock.MagicMock(name="run"))
    @patch('parcel.distro.Debian.version', mock.MagicMock(name="version"))
    def test_prepare_app(self):
        
        d = Deployment('testapp')
        ## d. arch = Debian()

        ## d.path ="."
        ## d.build_path = 'build'
        d.prepare_app()
        #run.assert_called_once_with("apt-get update -qq")



