import sys
import unittest2 as unittest

from mock import patch, MagicMock

from parcel.distro import debian
from parcel.deploy import Deployment

from parcel_mocks import run, _AttributeString, version_run, with_settings

# add mocks to this list if they should have reset called on them after tests
mocks_to_reset = [run, version_run, with_settings]


class TestDeploy(Deployment):
    """Simple test class for deploytment which  overrides __init__ so we are not calling remote host"""
    def __init__(self, app_name=None):
        self.app_name = app_name


class DistroTestSuite(unittest.TestCase):
    """Versions test cases."""

    def setUp(self):
        pass
    
    def tearDown(self):
        for m in mocks_to_reset:
            m.reset_mock()

    @patch('parcel.distro.run', run)
    def test_build_deps(self):
        deps = ['test_dep0', 'test_dep1']
        debian.build_deps(deps)
        run.assert_called_once_with("apt-get install -qq %s"%(' '.join(deps)))

    @patch('parcel.distro.run', version_run)
    def test_version(self):
        out = _AttributeString("0.5.1")
        out.return_code = 0
        version_run.return_value = out
        ret = debian.version('test_pkg')
        version_run.assert_called_once_with('apt-cache show %s 2>/dev/null | sed -nr "s/^Version: ([0-9]+)(-.+)?/\\1/p"'%('test_pkg'))
        self.assertEqual(str(ret), "0.5.1")

    @patch('parcel.distro.run', version_run)
    def test_version_not_found(self):
        out = _AttributeString("")
        out.return_code = 1
        version_run.return_value = out
        ret = debian.version('test_pkg')
        version_run.assert_called_once_with('apt-cache show %s 2>/dev/null | sed -nr "s/^Version: ([0-9]+)(-.+)?/\\1/p"'%('test_pkg'))
        self.assertEqual(ret, None)


    @patch('parcel.distro.run', run)
    def test_update_packages(self):
        debian.update_packages()
        run.assert_called_once_with("apt-get update -qq")

    @patch('parcel.distro.run', run)
    def test_cleanup(self):
        debian._cleanup()
        self.assertEqual(run.call_count,1)
        self.assertTrue("rm -rf" in run.call_args[0][0])

    @patch('parcel.distro.run', run)
    def test_internal_setup(self):
        debian._setup()
        commands = run.call_args_list                   # get the commands run remotely in order
        
        # clean command should top list
        self.assertTrue("rm -rf" in commands[0][0][0])
        
        # the rest should be mkdirs.
        for command in commands[1:]:
            self.assertTrue(command[0][0].startswith('mkdir '))
            
            # the classes build space should be in the path
            self.assertTrue(debian.space in command[0][0])

    def test_check_fpm_not_present(self):
        def called(command):
            class retobj: pass
            retval = retobj()
            
            if 'fpm' in command:
                retval.return_code = 1
            elif 'checkinstall' in command:
                retval.return_code = 0
        
            return retval 
            
        run.side_effect = called              # return these two objects from two calls to run
        self.assertRaises(Exception,debian.check,())                  # should be fpm exception
        
    def test_check_fpm_present_checkinstall_not(self):
        def called(command):
            class retobj: pass
            retval = retobj()
            
            if 'fpm' in command:
                retval.return_code = 0
            elif 'checkinstall' in command:
                retval.return_code = 1
        
            return retval 
            
        run.side_effect = called              # return these two objects from two calls to run
        
        self.assertRaises(Exception,debian.check,())                  # should be checkinstall exception

    @patch('parcel.distro.run', run)        
    def test_check_everything_present(self):
        class retobj: pass
        retval = retobj()
        retval.return_code = 0
        run.return_value = retval              # return these two objects from two calls to run
        debian.check()
