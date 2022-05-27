const _ = require('lodash');
const winston = require('winston');

const transports = [
  new winston.transports.File({
    dirname: 'logs',
    maxsize: 1000000,
    maxFiles: 100,
  }),
];

if (process.env.NODE_ENV === 'development') {
  transports.push(new winston.transports.Console());
}

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.simple(),
  ),
  transports,
});

logger.errorNice = (context, error) => {
  const meta = { context };
  if (_.get(error, 'response.data.code')) meta.code = error.response.data.code;
  logger.error(error, meta);
};

logger.info('===== logger started =====');

module.exports = logger;
