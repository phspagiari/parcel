import sys, os                      
import threading
import SimpleHTTPServer
import SocketServer
import socket, errno

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class WebServerMixin(object):
    """Webserver test cases."""
    def startWebServer(self,port=8000):
        self.host = 'localhost'

        self.server = None
        while self.server is None:
            try:
                self.server = ThreadedTCPServer((self.host, port), SimpleHTTPServer.SimpleHTTPRequestHandler)
            except socket.error, e:
                if e.errno==errno.EADDRINUSE:
                    port += 1               # address in use. Increase the port
                else:
                    raise e
        self.ip, self.port = self.server.server_address
        
        self.webroot = os.path.join(os.path.dirname(__file__),"data")           # serve out the data directory
        
        # Start a thread with the server
        def sthread():
            os.chdir(self.webroot)                 
            self.server.serve_forever()
            
        self.server_thread = threading.Thread(target=sthread)
        
        # Exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()

    def stopWebServer(self):
        self.server.shutdown()
     
