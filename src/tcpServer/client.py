import socket
import sys
import threading
import time

HOST, PORT = "10.0.0.21", 5000
username = " ".join(sys.argv[1:])
loopRecv = True
pingTime = 10.0
# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def printRecv():
    global loopRecv
    while loopRecv:
        time.sleep(.5)
        response = sock.recv(1024)
        print response
        if response == "Connection Timeout.":
            loopRecv = False

def keepAlive():
    while loopRecv:
        time.sleep(pingTime)
        sock.sendall("<PING>")
try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    data = username

    server_thread = threading.Thread(target=printRecv)
    server_thread.daemon = True
    server_thread.start()

    while data.lower() != 'q' and loopRecv:
        sock.sendall(data)
        data = str(raw_input())

finally:
    loopRecv = False
    sock.close()

#print "Sent:     {}".format(data)
#print "Received: {}".format(received)