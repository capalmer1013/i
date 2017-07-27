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
    This will need to use the threading mixin in order to handle
    multiple continuous client connections
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
            try:
                time.sleep(lastSleep)
                lastSleep *= 2
                inputReady, _ , _ = select.select([self.request], [], [])

                if inputReady:
                    self.data = self.request.recv(1024).strip()
                    print "{} wrote:".format(self.client_address[0])
                    print self.data
                    sendOthers(username, self.data)
                    self.request.sendall(">" + self.data)
            
            except:
                del connectedUsers[username]
                return
        
        del connectedUsers[username]
        self.request.sendall("Connection Timeout.")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5000

    # old way no threads just 1 connection
    # server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    server.shutdown()
    server.server_close()
