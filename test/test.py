import socket
import sys

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = '10.2.4.159'
port = 8081

while(1) :
    msg = raw_input('Enter message to send : ')

    try :
        # Set the whole string
        s.sendto(msg, (host, port))

    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
