# Two-way authentication provisioning

Two-way authenticated communication under a single authority can be established with the following provisions.

Note:
- We expect keys are secret.
- We expect pems are public but untampered.

```
# create ca.key
openssl genrsa -out ca.key 2048
# create ca.pem from ca.key
openssl req -x509 -new -nodes -key ca.key -sha256 -out ca.pem -subj /C=CA/ST=Ontario/L=Toronto/CN=www.test.com

# create server.key
openssl genrsa -out server.key 2048
# create server.pem from server.key, sign with ca.key
openssl req -new -key server.key -out server.csr -subj /C=CA/ST=Ontario/L=Toronto/CN=www.test.com
echo 'authorityKeyIdentifier = keyid,issuer
	basicConstraints = CA:FALSE
	keyUsage = digitalSignature, keyEncipherment
	extendedKeyUsage = serverAuth
	subjectAltName = DNS:localhost' > server.ext
openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out server.crt -sha256 -extfile server.ext
openssl x509 -in server.crt -out server.pem -outform PEM

# create client.key
openssl genrsa -out client.key 2048
# create client.pem from client.key, sign with ca.key
openssl req -new -key client.key -out client.csr -subj /C=CA/ST=Ontario/L=Toronto/CN=www.test.com
echo 'authorityKeyIdentifier=keyid,issuer
	basicConstraints=CA:FALSE
	extendedKeyUsage = clientAuth' > client.ext
openssl x509 -req -in client.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out client.crt -sha256 -extfile client.ext
openssl x509 -in client.crt -out client.pem -outform PEM
```

Now:
- when client makes a request to server, server sends back `server.pem`;
- client verifies `server.pem` with `ca.pem` and sends `client.pem` and a session key, encrypted with `server.pem`;
- server decrypts with `server.key` (thereby proving its identity to client) and verifies `client.pem` with `ca.pem`;
- client signs the exchange so far with `client.key` and sends to server to prove its identity.

Example using rustls:
- server: `cargo run --example tlsserver -- --certs server.pem --key server.key --auth ca.pem -p 8443 echo`
- client: `cargo run --example tlsclient -- --http localhost -p 8443 --cafile ca.pem --auth-key client.key --auth-certs client.pem`

Reference:
- https://tools.ietf.org/rfcmarkup/5246
- especially https://tools.ietf.org/rfcmarkup/5246#section-7.4.8, which doesn't seem covered in summaries

# Getting certificate for URL
`openssl s_client -connect foresightanalytics.ca:443 | openssl x509`
