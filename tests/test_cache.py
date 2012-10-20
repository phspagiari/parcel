import unittest2 as unittest
import sys, os

from parcel.cache import FileCache

from random import randint                         

##
## Some functions to help building and clearing a directory
##
import tempfile, shutil

def mkdir():
    return tempfile.mkdtemp()
    
def rmdir(path):
    shutil.rmtree(path)



##
## We need to test web download functionality, but web is too slow
## Built in simple threaded server
##
import socket
import threading
import SimpleHTTPServer
import SocketServer

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


##
## Test Suite
##
class CacheTestSuite(unittest.TestCase):
    """Versions test cases."""
    def setUp(self):
        self.path = None                # use this in tests for a directory that will always be deleted
    
    def tearDown(self):
        if self.path:
            rmdir(self.path)
        self.path = None
    
    def startWebServer(self,port):
        self.host = 'localhost'

        self.server = ThreadedTCPServer((self.host, port), SimpleHTTPServer.SimpleHTTPRequestHandler)
        self.ip, self.port = self.server.server_address
        
        # Start a thread with the server
        def sthread():
            os.chdir(os.path.join(os.path.dirname(__file__),"data"))                 # serve out the data directory
            self.server.serve_forever()
            
        self.server_thread = threading.Thread(target=sthread)
        
        # Exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()

    def stopWebServer(self):
        self.server.shutdown()
        
    def test_new_cache_makes_directory(self):
        # make a path
        self.path = mkdir()
        
        # delete it. so the cache has to create it
        rmdir(self.path)
  
        # make a cache with it
        cache = FileCache(self.path)
        
        # director should exist
        self.assertTrue(os.path.isdir(self.path))
        
        # directory should be empty
        self.assertFalse(os.listdir(self.path))
        
    def test_new_cache_uses_existing_directory(self):
        # make path
        self.path = mkdir()
        
        # make a cache with it
        cache = FileCache(self.path)
        
        # director should exist
        self.assertTrue(os.path.isdir(self.path))
        
        # directory should be empty
        self.assertFalse(os.listdir(self.path))
        
    def test_get_tarball_url(self):
        port = randint(1024,64000)                           # we randomise our server port as a shitty way of not needing to set SO_REUSEADDR
        self.startWebServer(port)
        
        # make cache
        self.path = mkdir()
        cache = FileCache(self.path)
        
        # get test tarball
        path = cache.get("http://localhost:%d/tip.tar.gz"%port)
        
        self.assertTrue('tip.tar.gz' in os.listdir(self.path))          # make sure file is in cache
        self.assertEquals(path, os.path.join(self.path,'tip.tar.gz'))   # make sure thats what was returned
        
        self.stopWebServer()
        
    def test_is_cached(self):
        pass
        
