import ecdsa

import hashlib

with open('pkcs8', 'rb') as f:
    signing_key = ecdsa.SigningKey.from_der(f.read())

def sig_encode_ring(r, s, order):
    return r.to_bytes(32, 'big') + s.to_bytes(32, 'big')

sig = signing_key.sign(
    b'asdf',
    hashfunc=hashlib.sha256,
    sigencode=sig_encode_ring,
)

with open('sig', 'wb') as f:
    f.write(sig)
