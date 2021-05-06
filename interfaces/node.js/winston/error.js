const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.simple(),
  ),
  transports: [new winston.transports.Console()],
});

logger.error('got an error:', new Error('hello'));
console.log('\n');
logger.error(new Error('hello again'));
console.log('\n');
logger.info('not an error');
console.log('\n');
logger.error('got another error:', new Error('message', { config: 'lol' }));
console.log('\n');
logger.error(new Error('message', { config: 'lol' }));
console.log('\n');
logger.error(new Error('message', { config: 'lol' }), { extra: 'doodly' });
console.log('\n');
logger.error('not what you might think', new Error('message', { config: 'lol' }), { extra: 'doodly' });
console.log('\n');
