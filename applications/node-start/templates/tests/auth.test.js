const { app } = require('../src/express');
const models = require('../src/models');

const supertest = require('supertest');
const supertestSession = require('supertest-session');

let fSession;

beforeAll(async (done) => {
  const email = `test-${new Date() / 1000}@email.com`;
  const password = 'testpw123412';
  await supertest(app).post('/auth/signup').send({ email, password });
  fSession = supertestSession(app);
  await fSession.post('/auth/login').send({ email, password });
  done();
});

afterAll(async (done) => {
  await models.sequelize.close();
  done();
});

test('Hello, world!', async (done) => {
  const res = await fSession.get('/hello/world').send();
  expect(res.status).toBe(200);
  done();
});
