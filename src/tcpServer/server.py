import SocketServer
import time
import select

connectionTimeout = 10.00
numConn = 0
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global numConn
        numConn += 1
        print "num connections:", numConn
        lastSleep = 0.1
        startTime = time.time()
        username = self.request.recv(1024).strip()
        # self.request is the TCP socket connected to the client
        while time.time() - startTime < connectionTimeout:
            self.data = self.request.recv(1024).strip()
            print "{} wrote:".format(self.client_address[0])
            print self.data
            self.request.sendall(self.data.upper())

        numConn -= 1

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()