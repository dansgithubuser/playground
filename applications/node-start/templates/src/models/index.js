const globals = require('../globals');
const logger = require('../logger');

const Sequelize = require('sequelize');

const fs = require('fs');
const path = require('path');

const basename = path.basename(__filename);
const env = process.env.NODE_ENV || 'development';
const config = require(path.join(__dirname, '/../../config/config'))[env]; // eslint-disable-line import/no-dynamic-require
const db = {};

let sequelize;
config.logging = (msg, ms) => {
  if (ms > 1000) {
    if (msg.length > 1000) {
      msg = `${msg.slice(0, 800)}\n...\n${msg.slice(-200)}`;
    }
    logger.warn(`Query took ${ms} ms. ${msg}`);
  } else if (globals.controls.log_sql_matching) {
    if (msg.match(globals.controls.log_sql_matching)) {
      logger.info(`Query matched logging pattern. ${ms} ms. ${msg}`);
    }
  } else {
    logger.debug(msg);
  }
};
config.benchmark = true;
if (config.use_env_variable) {
  sequelize = new Sequelize(process.env[config.use_env_variable], config);
} else {
  sequelize = new Sequelize(config.database, config.username, config.password, config);
}

fs
  .readdirSync(__dirname)
  .filter((file) => (file.indexOf('.') !== 0) && (file !== basename) && (file.slice(-3) === '.js'))
  .forEach((file) => {
    const model = require(path.join(__dirname, file))(sequelize, Sequelize.DataTypes); // eslint-disable-line import/no-dynamic-require,max-len,global-require
    db[model.name] = model;
  });

Object.keys(db).forEach((modelName) => {
  if (db[modelName].associate) {
    db[modelName].associate(db);
  }
});

db.sequelize = sequelize;
db.Sequelize = Sequelize;

module.exports = db;
