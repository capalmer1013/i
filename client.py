import socket
import json
import getpass
import random
import time

DEBUG = True

SENDPORT = 5008
RECEIVEPORT = 5009
MESSAGERECEIVE = 5010
serverIP = 'localhost' if DEBUG else 'something else'  # I'll figure this out at some point

messageSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
messageSock.settimeout(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(3)


def sendGlobalChat(message):
    jsonDict = {
        'message': 'sendGlobalChat',
        'chat': str(message)
    }
    sock.sendto(json.dumps(jsonDict), (serverIP, SENDPORT))  # all messaging stuff should be on a different socket

    #received = json.loads(sock.recv(1024))


def sendGroupChat(message, groupId):
    pass


def sendDirectMessageChat(message, playerName):
    pass


def receiveAllMessages():
    result = sock.recv(1024)
    pass


def createAccount(username, password):
    jsonDict = {
        'message': 'createPlayer',
        'username': username,
        'password': password
        }
    sock.sendto(json.dumps(jsonDict), (serverIP, SENDPORT))
    try:
        received = json.loads(sock.recv(1024))
        if received['response'] == 'success':
            print "account created"
            return True

        else:
            print "create account failed"
            return False

    except socket.timeout:
        print "connection timed out"
        return False

    return True


def pingServer():
    pingId = random.randint(0, 100000000)  # becuase using a sequence would be too easy
    jsonDict = {'message': 'ping'}
    jsonDict['id'] = pingId

    startTime = time.time()
    sock.sendto(json.dumps(jsonDict), (serverIP, SENDPORT))
    try:
        received = sock.recv(1024)

    except socket.timeout:
        print "connection timed out"
        return -2

    if int(received) == pingId:
        roundTrip = time.time() - startTime
        print "Ping", roundTrip
        return roundTrip

    return -1  # response out of order


def login():
    jsonDict = {'message': 'login'}  # login should be added to messaging module
    jsonDict['username'] = raw_input("username: ")
    jsonDict['password'] = getpass.getpass("password: ")
    sock.sendto(json.dumps(jsonDict), (serverIP, SENDPORT))
    received = sock.recv(1024)
    print received


def main():
    username = raw_input("username: ")
    password = getpass.getpass("password")
    createAccount(username, password)


if __name__ == "__main__":
    main()
