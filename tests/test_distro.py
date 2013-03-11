import sys
import unittest2 as unittest

from mock import patch, MagicMock

from parcel.distro import debian, ubuntu, centos, Distro
from parcel.deploy import Deployment

from parcel_mocks import (run, _AttributeString, version_run, with_settings,
                          put, append)

# some mocks only used in distro tests
distro_run = MagicMock(name="distro_run")
distro_cd = MagicMock(name="distro_cd")
distro_cache = MagicMock(name="distro_cache")
distro_mkdir = MagicMock(name="distro_mkdir")
distro_rsync = MagicMock(name='distro_rsync')

# add mocks to this list if they should have reset called on them after tests
mocks_to_reset = [run, version_run, with_settings, put, append]


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
        commands = run.call_args_list
        
        # clean command should top list
        self.assertTrue("rm -rf" in commands[0][0][0])
        
        # the rest should be mkdirs.
        for command in commands[1:]:
            self.assertTrue(command[0][0].startswith('mkdir '))
            
            # the classes build space should be in the path
            self.assertTrue(debian.space in command[0][0])

    @patch('parcel.distro.run', run)
    def test_check_fpm_not_present(self):
        def called(command):
            class retobj: pass
            retval = retobj()
            
            if 'fpm' in command:
                retval.return_code = 1
            elif 'checkinstall' in command:
                retval.return_code = 0
        
            return retval 
            
        run.side_effect = called  # return these two objects from two calls to run
        self.assertRaises(Exception,debian.check,())  # should be fpm exception

    @patch('parcel.distro.run', run)        
    def test_check_fpm_present_checkinstall_not(self):
        def called(command):
            class retobj: pass
            retval = retobj()
            
            if 'fpm' in command:
                retval.return_code = 0
            elif 'checkinstall' in command:
                retval.return_code = 1
        
            return retval 
            
        run.side_effect = called  # return these two objects from two calls to run
        self.assertRaises(Exception,debian.check,())  # should be checkinstall exception

    @patch('parcel.distro.run', run)        
    def test_check_everything_present(self):
        class retobj: pass
        retval = retobj()
        retval.return_code = 0
        run.return_value = retval  # return these two objects from two calls to run
        debian.check()
    
    @patch('parcel.distro.put', put)
    def test_push_files(self):
        debian.push_files(['file1','file2','file3'], '/path/to/dest/')
        self.assertTrue( 'file1' in put.call_args_list[0][0][0])
        self.assertTrue('/path/to/dest/file1' in put.call_args_list[0][0][1])
        self.assertTrue( 'file2' in put.call_args_list[1][0][0])
        self.assertTrue('/path/to/dest/file2' in put.call_args_list[1][0][1])
        self.assertTrue( 'file3' in put.call_args_list[2][0][0])
        self.assertTrue('/path/to/dest/file3' in put.call_args_list[2][0][1])

    @patch('parcel.distro.run', run)
    def test_check(self):
        out = _AttributeString("/usr/local/bin/fpm")
        out.return_code = 0
        run.return_value = out
        debian.check()

        # check for fpm
        self.assertTrue( 'which fpm' in run.call_args_list[0][0][0])
        self.assertTrue( 'which checkinstall' in run.call_args_list[1][0][0])

    @patch('parcel.distro.run', distro_run)
    def test_check_no_fpm(self):
        fpm_out = _AttributeString("/usr/local/bin/fpm")
        fpm_out.return_code = 1
        checkinstall_out = _AttributeString("/usr/bin/checkinstall")
        checkinstall_out.return_code = 0
        distro_run.side_effect = [fpm_out, checkinstall_out]

        with self.assertRaises(Exception):
            debian.check()

    @patch('parcel.distro.run', distro_run)
    def test_check_no_checkinstall(self):
        fpm_out = _AttributeString("/usr/local/bin/fpm")
        fpm_out.return_code = 0
        checkinstall_out = _AttributeString("/usr/bin/checkinstall")
        checkinstall_out.return_code = 1
        distro_run.side_effect = [fpm_out, checkinstall_out]

        with self.assertRaises(Exception):
            debian.check()

    def test_unimplemented_methods_on_distro(self):
        d = Distro()
        with self.assertRaises(NotImplementedError):
            d.setup()
        with self.assertRaises(NotImplementedError):
            d.update_packages()
        with self.assertRaises(NotImplementedError):
            d.build_deps(['testdep'])
        with self.assertRaises(NotImplementedError):
            d.version('test_pkg')
        with self.assertRaises(NotImplementedError):
            d.check()

    def test_install_package_on_distro(self):
        d = Distro()
        with self.assertRaises(NotImplementedError):
            d.install_package('test_pkg')

    @patch.multiple('parcel.distro', with_settings=with_settings, run=run, put=put, cd=distro_cd)
    @patch('parcel.distro.cache.get', distro_cache)
    @patch('parcel.distro.Debian.mkdir', distro_mkdir)    
    def test_setup(self):
        distro_cache.return_value = '/a/test/path/file.gz'
        distro_mkdir.side_effect = ['.parcel-build-temp', '.parcel-build-temp/src', '.parcel-build-temp/build']
        debian.setup()

        self.assertTrue(run.call_args_list[0][0][0] == 'apt-get install -qq libyaml-ruby libzlib-ruby ruby ruby-dev checkinstall')
        self.assertTrue(run.call_args_list[1][0][0] == "rm -rf '.parcel-build-temp'")
        self.assertTrue(run.call_args_list[2][0][0] == 'tar xvfz ../src/file.gz')
        self.assertTrue(run.call_args_list[3][0][0] == 'ruby setup.rb')
        self.assertTrue(run.call_args_list[4][0][0] == 'gem1.8 install fpm')

        self.assertTrue(distro_mkdir.call_args_list[0][0][0] == '.parcel-build-temp')
        self.assertTrue(distro_mkdir.call_args_list[1][0][0] == '.parcel-build-temp/src')
        self.assertTrue(distro_mkdir.call_args_list[2][0][0] == '.parcel-build-temp/build')

        self.assertTrue(distro_cache.call_args_list[0][0][0] == 'http://production.cf.rubygems.org/rubygems/rubygems-1.8.24.tgz')

    @patch.multiple('parcel.distro', with_settings=with_settings, run=run, put=put, cd=distro_cd, append=append, rsync=distro_rsync)
    @patch('parcel.distro.Debian.mkdir', distro_mkdir)
    def test_install_package(self):
        distro_mkdir.side_effect = ['.parcel-build-temp', '.parcel-build-temp/src', '.parcel-build-temp/build', '.parcel-build-temp/pkg_dir']
        #run.side_effect = ["test", "testapp", "0.1.2", "test", "test"]
        debian.install_package('testapp_0.1.2_all.deb')

        self.assertTrue(append.call_args_list[0][0][0] == '/etc/apt/sources.list', 'deb file://.parcel-build-temp/pkg_dir /')
        self.assertTrue(run.call_args_list[0][0][0] == 'dpkg-scanpackages . /dev/null | gzip -c -9 > Packages.gz')
        self.assertTrue(run.call_args_list[1][0][0] == "dpkg -f testapp_0.1.2_all.deb | grep '^Package: ' | sed -e 's/Package: //'")
        self.assertTrue(run.call_args_list[2][0][0] == "dpkg -f testapp_0.1.2_all.deb | grep '^Version: ' | sed -e 's/Version: //'")
        self.assertTrue(run.call_args_list[3][0][0] == 'apt-get update -qq')
        self.assertTrue('apt-get install' in run.call_args_list[4][0][0])

    @patch.multiple('parcel.distro', with_settings=with_settings, run=run, put=put, cd=distro_cd)
    @patch('parcel.distro.cache.get', distro_cache)
    @patch('parcel.distro.Debian.mkdir', distro_mkdir)    
    def test_setup_ubuntu(self):
        distro_cache.return_value = '/a/test/path/file.gz'
        distro_mkdir.side_effect = ['.parcel-build-temp', '.parcel-build-temp/src', '.parcel-build-temp/build']
        ubuntu.setup()

        self.assertTrue(run.call_args_list[0][0][0] == 'apt-get install rubygems -y')
        self.assertTrue(run.call_args_list[1][0][0] == 'gem install fpm')


class DistroCentosTestSuite(unittest.TestCase):
    """Versions test cases."""

    def setUp(self):
        pass
    
    def tearDown(self):
        for m in mocks_to_reset:
            m.reset_mock()

    @patch('parcel.distro.run', run)
    def test_centos_update_packages(self):
        centos.update_packages()
        run.assert_called_once_with("yum update -y")

    @patch('parcel.distro.run', run)
    def test_centos_build_deps(self):
        deps = ['test_dep0', 'test_dep1']
        centos.build_deps(deps)
        run.assert_called_once_with("yum install -y %s"%(' '.join(deps)))

    @patch('parcel.distro.run', version_run)
    def test_centos_version(self):
        out = _AttributeString("0.5.1")
        out.return_code = 0
        version_run.return_value = out
        ret = centos.version('test_pkg')
        version_run.assert_called_once_with('rpm -qi %s 2>/dev/null | sed -nr "s/^Version.+: ([0-9]+)(-.+)?/\\1/p"'%('test_pkg'))
        self.assertEqual(str(ret), "0.5.1")

    @patch('parcel.distro.run', version_run)
    def test_centos_version_not_found(self):
        out = _AttributeString("")
        out.return_code = 1
        version_run.return_value = out
        ret = centos.version('test_pkg')
        version_run.assert_called_once_with('rpm -qi %s 2>/dev/null | sed -nr "s/^Version.+: ([0-9]+)(-.+)?/\\1/p"'%('test_pkg'))
        self.assertEqual(ret, None)


    @patch.multiple('parcel.distro', with_settings=with_settings, run=run, put=put, cd=distro_cd)
    @patch('parcel.distro.cache.get', distro_cache)
    @patch('parcel.distro.Centos.mkdir', distro_mkdir)    
    def test_centos_setup(self):
        distro_cache.return_value = '/a/test/path/file.gz'
        distro_mkdir.side_effect = ['.parcel-build-temp', '.parcel-build-temp/src', '.parcel-build-temp/build']
        centos.setup()

        self.assertTrue(run.call_args_list[0][0][0] == 'yum install rubygems -y')
        self.assertTrue(run.call_args_list[1][0][0] == 'gem install fpm')
        self.assertTrue(run.call_args_list[2][0][0] == 'yum install rpm-build -y')
        self.assertTrue(run.call_args_list[3][0][0] == 'yum install rsync -y')

    @patch('parcel.distro.run', run)
    def test_centos_check(self):
        out = _AttributeString("/usr/local/bin/fpm")
        out.return_code = 0
        run.return_value = out
        centos.check()

        # check for fpm
        self.assertTrue( 'which fpm' in run.call_args_list[0][0][0])

    @patch('parcel.distro.run', distro_run)
    def test_check_no_fpm(self):
        fpm_out = _AttributeString()
        fpm_out.return_code = 1
        distro_run.side_effect = [fpm_out]

        with self.assertRaises(Exception):
            centos.check()
