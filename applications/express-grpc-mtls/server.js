//===== requires =====//
const _ = require('lodash');
const express = require('express');
const grpc = require('@grpc/grpc-js')
const protoLoader = require('@grpc/proto-loader');

const fs = require('fs');

//===== consts =====//
const bird = grpc.loadPackageDefinition(protoLoader.loadSync('bird.proto')).bird;

//===== state =====//
const birds = {};

//===== functions =====//
function sing(call) {
  birds[call.call.stream.session.socket.getPeerCertificate().modulus] = {
    name: call.request.name,
  };
  const value = _.sample([
    { chirp: { description: _.sample(['seed', 'bug']) } },
    { tweet: { description: _.sample(['nice', 'wind', 'rain']) } },
    { warble: { description: _.sample(['happy', 'annoyed', 'shy', 'bird']) } },
    { squawk: { description: _.sample(['squirrel', 'dog', 'big bird']) } },
  ]);
  console.log('server singing', value, 'to', call.request.name);
  call.write(value);
  setTimeout(() => sing(call), 3000);
}

function chirp(call, callback) {
  const name = birds[call.call.stream.session.socket.getPeerCertificate().modulus].name;
  console.log(`server heard chirp from ${name}:`, call.request);
  callback(null, {});
}

function tweet(call, callback) {
  const name = birds[call.call.stream.session.socket.getPeerCertificate().modulus].name;
  console.log(`server heard tweet from ${name}:`, call.request);
  callback(null, {});
}

function warble(call, callback) {
  const name = birds[call.call.stream.session.socket.getPeerCertificate().modulus].name;
  console.log(`server heard warble from ${name}:`, call.request);
  callback(null, {});
}

function squawk(call, callback) {
  const name = birds[call.call.stream.session.socket.getPeerCertificate().modulus].name;
  console.log(`server heard squawk from ${name}:`, call.request);
  callback(null, {});
}

//===== grpc =====//
const grpcServer = new grpc.Server();

grpcServer.addService(bird.Bird.service, {
  sing,
  chirp,
  tweet,
  warble,
  squawk,
});

grpcServer.bindAsync(
  '0.0.0.0:8001',
  grpc.ServerCredentials.createSsl(
    fs.readFileSync('ca.pem'),
    [
      {
        private_key: fs.readFileSync('server.key'),
        cert_chain: fs.readFileSync('server.crt'),
      }
    ],
    true,
  ),
  (err, port) => grpcServer.start(),
);

//===== express =====//
const app = express();

app.get('/', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(birds));
});

app.listen(8000, () => console.log(`Express listening on port 8000`));
