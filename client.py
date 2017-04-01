import socket
import json
import getpass

DEBUG = True

SENDPORT = 5008
RECEIVEPORT = 5009
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def login():
    # send login request
    # with username and password
    # wait for success or failure response
    jsonDict = {'message': 'login'}  # login should be added to messaging module
    jsonDict['username'] = raw_input("username: ")
    jsonDict['password'] = getpass.getpass("password: ")
    serverIP = 'localhost' if DEBUG else 'something else'
    sock.sendto(json.dumps(jsonDict), (serverIP, SENDPORT))
    received = sock.recv(1024)
    print received


def main():
    login()
    pass

if __name__ == "__main__":
    main()
