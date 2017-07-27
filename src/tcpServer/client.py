import socket
import sys

HOST, PORT = "10.0.0.21", 5000
username = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    data = username

    while data.lower() != 'q':
        sock.sendall(data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
        # print "Sent:     {}".format(data)
        print received
        data = str(raw_input(">"))
finally:
    sock.close()

print "Sent:     {}".format(data)
print "Received: {}".format(received)