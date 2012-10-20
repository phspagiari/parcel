import sys, os
from random import randint                         
import socket
import threading
import SimpleHTTPServer
import SocketServer

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class WebServerMixin(object):
    """Webserver test cases."""
    def startWebServer(self,port=8000):
        self.host = 'localhost'

        try:
            self.server = ThreadedTCPServer((self.host, port), SimpleHTTPServer.SimpleHTTPRequestHandler)
        except Exception, e:
            print e
            raise
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
     
