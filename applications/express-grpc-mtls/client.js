//===== requires =====//
const _ = require('lodash');
const grpc = require('@grpc/grpc-js')
const protoLoader = require('@grpc/proto-loader');

const fs = require('fs');

//===== consts =====//
const bird = grpc.loadPackageDefinition(protoLoader.loadSync('bird.proto')).bird;

//===== functions =====//
function log_error(error) {
  if (error) console.log('client error:', error);
}

//===== main =====//
const name = _.sample(['Benji', 'Bonnie', 'Bert', 'Bob']);
console.log('I am', name, '(a client)');

const client = new bird.Bird(
  'localhost:8001',
  grpc.credentials.createSsl(
    fs.readFileSync('ca.pem'),
    fs.readFileSync('client.key'),
    fs.readFileSync('client.crt'),
  ),
);

client.sing({ name })
  .on('data', (song) => {
    console.log('client heard', song, '-- echoing');
    if (song.chirp) client.chirp(song.chirp, log_error);
    else if (song.tweet) client.tweet(song.tweet, log_error);
    else if (song.warble) client.warble(song.warble, log_error);
    else if (song.squawk) client.squawk(song.squawk, log_error);
  });
