require('../src/env');

const dbConfig = {
  username: process.env.DB_USER,
  password: process.env.DB_PW,
  database: process.env.DB,
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  dialect: 'postgres',
};

module.exports = {
  development: dbConfig,
  test: dbConfig,
  staging: dbConfig,
  production: dbConfig,
};
