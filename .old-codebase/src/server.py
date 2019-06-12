import SocketServer
import json
import socket
from objects import playerDb

DEBUG = True
ANY = '0.0.0.0'
SENDERPORT = 5009
RECEIVERPORT = 5008

messageSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectedClients = []


def login(jsonDict):
    return playerDb.lookupUsernamePassword(str(jsonDict['username']), str(jsonDict['password']))


def ping(jsonDict):
    return jsonDict['id']


def createPlayer(jsonDict):
    result = playerDb.createUsernamePassword(jsonDict['username'], jsonDict['password'])
    if result == 'success':
        return json.dumps({'message': 'createPlayer', 'response': 'success'})

    else:
        return json.dumps({'message': 'createPlayer', 'response': 'failure'})


def sendGlobalChat(jsondict):
    print jsondict['address']
    return json.dumps(jsondict)

    pass


def sendGroupChat(jsonDict):
    pass


def sendDirectMessageChat(jsonDict):
    pass

processMessage = {
    'login': login,
    'ping': ping,
    'createPlayer': createPlayer,
    'sendGlobalChat': sendGlobalChat,
}


class MyUDPHandler (SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        dataDict = json.loads(data)
        dataDict['address'] = self.client_address
        connectedClients.append(self.client_address)
        result = processMessage[dataDict['message']](dataDict)
        print self.client_address, dataDict['message']
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
