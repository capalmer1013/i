import SocketServer
import time
import sqlite3
import json
from objects import playerDb

DEBUG = True
ANY = '0.0.0.0'
SENDERPORT = 5009
RECEIVERPORT = 5008


def login(jsonDict):
    return playerDb.lookupUsernamePassword(str(jsonDict['username']), str(jsonDict['password']))


processMessage = {
    'login': login
}


class MyUDPHandler (SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        dataDict = json.loads(data)
        result = processMessage[dataDict['message']](dataDict)
        print data
        sock.sendto(str(result), self.client_address)


def main():
    if DEBUG:
        HOST = 'localhost'
    else:
        pass

    server = SocketServer.UDPServer((ANY, RECEIVERPORT), MyUDPHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
