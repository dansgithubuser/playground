class Receiver:
    def __init__(self, sock):
        self.leftover = b''
        self.sock = sock

    def recv(self):
        chunks = []
        while True:
            if self.leftover:
                chunk = self.leftover
                self.leftover = b''
            else:
                chunk = self.sock.recv(4)
            if not chunk:
                return
            if 0 in chunk:
                chunk, self.leftover = chunk.split(b'\0', 1)
                chunks.append(chunk)
                return b''.join(chunks)
            chunks.append(chunk)
