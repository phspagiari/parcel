import unittest2 as unittest
from fabric.api import run
import tempfile

from mock import patch

from mixins import WebServerMixin
from parcel.tools import dl, read_contents_from_remote, quiet_run, rsync
from parcel_mocks import mock_get, local

# add mocks to this list if they should have reset called on them after tests
mocks_to_reset = []


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


    @patch('parcel.tools.run', local)

    # patch local so rsync command not run, check correct command is called
    def _test_rsync(self):
        test_file = os.path.join(os.path.dirname(__file__),"data", "tip.tar.gz")
        #make a dir - rsync into it
        # test
        # remove
        rsync(test_file, 'test.tar.gz')
