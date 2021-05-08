import socket

from receiver import Receiver

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8000))
sock.listen(5)

while True:
    (sock_client, address) = sock.accept()
    receiver = Receiver(sock_client)
    while True:
        msg = receiver.recv()
        if msg == None: break
        print('server got msg:', msg)
        sock_client.sendall(b'yo!\0')
