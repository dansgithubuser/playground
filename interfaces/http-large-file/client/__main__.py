import requests

import struct

class PretendFile:
    def __init__(self, size=1000, chunk_size=64):
        self.i = 0
        self.size = size
        self.chunk_size = chunk_size
        self.offset = 0

    def next_chunk(self):
        chunk = bytearray()
        for i in range(self.chunk_size // 4):
            if self.offset >= self.size: break
            chunk.extend(self.i.to_bytes(4, 'big'))
            self.offset += 4
            self.i += 1
        return chunk

file = PretendFile()

while True:
    offset = file.offset
    chunk = file.next_chunk()
    if not chunk: break
    requests.put(
        'http://localhost:5000/upload',
        data=chunk,
        headers={'Content-Range': str(offset)},
    )
