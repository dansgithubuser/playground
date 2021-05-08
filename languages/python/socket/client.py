import socket

from receiver import Receiver

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8000))
sock.sendall(b'hello!\0')
print('client got msg:', Receiver(sock).recv())
