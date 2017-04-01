import socket
import SocketServer
import time
import sqlite3

DEBUG = True
ANY = '0.0.0.0'
SENDERPORT = 5009
RECEIVERPORT = 5008


class MyUDPHandler (SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        sock = self.request[1]
        print "{} wrote:".format(self.client_address[0])
        print data
        sock.sendto(data.upper(), self.client_address)


def main():
    if DEBUG:
        HOST = 'localhost'
    else:
        pass

    server = SocketServer.UDPServer((ANY, RECEIVERPORT), MyUDPHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
