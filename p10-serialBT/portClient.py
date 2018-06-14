# Echo client program
import socket

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect("/tmp/channel1")
s.send(b'10;1000')
data = s.recv(1024)
s.close()
print('Received ' + repr(data))
