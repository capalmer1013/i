import SocketServer
import time
import select

connectionTimeout = 60.00
connectedUsers = {}
initialTimeout = 0.1
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

        lastSleep = initialTimeout
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
                lastSleep += 0.1
                inputReady, _ , _ = select.select([self.request], [], [], 0.5)
                if inputReady:
                    startTime = time.time()
                    lastSleep = initialTimeout
                    self.data = self.request.recv(1024).strip()
                    #print "{} wrote:".format(self.client_address[0])
                    #print self.data
                    if self.data and self.data != "<PING>":
                        sendOthers(username, self.data)
            
            except Exception as e:
                print e
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
