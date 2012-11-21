import unittest2 as unittest
from fabric.api import run
import tempfile

from mock import patch, MagicMock

from mixins import WebServerMixin
from parcel.tools import dl, read_contents_from_remote, quiet_run, rsync
from parcel_mocks import mock_get, local

# add mocks to this list if they should have reset called on them after tests
mocks_to_reset = []

rsync_run = MagicMock(name="rsync_run")
rsync_local = MagicMock(name="rsync_local")

def tempname():
    return tempfile.mkstemp()[1]
    
import zlib, os

def crc32(filename):
    CHUNKSIZE = 8192
    checksum = 0
    with open(filename, 'rb') as fh:
        data = fh.read(CHUNKSIZE)
        while data:
            checksum = zlib.crc32(data, checksum)
            data = fh.read(CHUNKSIZE)
    return checksum


class ToolsTestSuite(unittest.TestCase, WebServerMixin):
    """Tools test cases."""

    def tearDown(self):
        for m in mocks_to_reset:
            m.reset_mock()
    
    def test_dl(self):
        self.startWebServer()
        
        filename = tempname()
        
        dl("http://localhost:%s/tip.tar.gz"%self.port,filename)
        
        try:
            # there should be no differences between the files
            self.assertEquals(crc32(filename),crc32(os.path.join(self.webroot,'tip.tar.gz')))
        finally:
            # shutdown webserver
            self.stopWebServer()
            
            # clean up file
            os.unlink(filename)
        
    @patch('parcel.tools.get', mock_get)
    def test_read_contents_from_remote(self):
        test_file = os.path.join(os.path.dirname(__file__),"data", "tip.tar.gz")
        data = read_contents_from_remote(test_file)

        fd,name = tempfile.mkstemp()
        os.unlink(name)

        with open(name,'w') as fh:
            data = fh.write(data)

        try:
            # there should be no differences between the files
            self.assertEquals(crc32(test_file),crc32(name))
        finally:
            # clean up file
            os.unlink(name)


    @patch.multiple('parcel.tools', get=mock_get, run=local)
    def test_quiet_run(self):

        data = quiet_run('ls .')
        self.assertTrue('hello.py' in data)
        self.assertTrue('tip.tar.gz' in data)


    # patch local so rsync command not run, check correct command is called
    @patch.multiple('parcel.tools', run=rsync_run, local=rsync_local)
    def test_rsync(self):
        test_file = os.path.join(os.path.dirname(__file__),"data", "tip.tar.gz")
        rsync_local.return_value = "This is output\n from test_rsync local mock.\n\n This is the fourth line.\n"
        rsync(test_file, 'test.tar.gz')

        # check rsync was called
        self.assertTrue('rsync -av' in rsync_local.call_args[0][0])

        # with colors off
        rsync(test_file, 'test.tar.gz', color_files=False)
        
        # with rsync_ignore, not real rsync file, just has to exist in this case
        # as we are not really calling rsync
        ignore_file = os.path.join(os.path.dirname(__file__),"data", "hello.py")
        rsync(test_file, 'test.tar.gz', rsync_ignore=ignore_file)
        self.assertTrue('--exclude-from={}'.format(ignore_file) in rsync_local.call_args[0][0])

        # with rsync_ignore but a non-existent file
        rsync(test_file, 'test.tar.gz', rsync_ignore='rsync_ignore')
        self.assertTrue('--exclude-from' not in rsync_local.call_args[0][0])

        # call with a list
        rsync([test_file, 'another_test_file'], 'test_files/')
        command = "rsync -av '{0}' '{1}'".format(test_file, 'another_test_file')
        self.assertTrue(command in rsync_local.call_args[0][0])
