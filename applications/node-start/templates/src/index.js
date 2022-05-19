require('./env');

const express = require('./express');
const logger = require('./logger');

process.on('unhandledException', (err) => logger.error('unhandled exception:', err));
process.on('unhandledRejection', (err) => logger.error('unhandled rejection:', err));

express.init();
