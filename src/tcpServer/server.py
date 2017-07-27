import SocketServer
import time
import select

connectionTimeout = 60.00
connectedUsers = {}

def sendOthers(username, message):
    for user in connectedUsers:
        if user != username:
            connectedUsers[user].sendall(username+'>'+message)

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global connectedUsers

        lastSleep = 0.1
        startTime = time.time()
        self.request.setblocking(0)
        username = self.request.recv(1024).strip()

        if username not in connectedUsers:
            self.request.sendall(str(len(connectedUsers)) + "connected users.")
            connectedUsers[username] = self.request

        else:
            self.request.sendall("Connection failed. Username taken.")
            return

        # self.request is the TCP socket connected to the client
        while time.time() - startTime < connectionTimeout:
            time.sleep(lastSleep)
            lastSleep *= 2
            inputReady, _ , _ = select.select([self.request], [], [])

            if inputReady:
                self.data = self.request.recv(1024).strip()
                print "{} wrote:".format(self.client_address[0])
                print self.data
                self.request.sendall(">" + self.data)

        self.request.sendall("Connection Timeout.")
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
