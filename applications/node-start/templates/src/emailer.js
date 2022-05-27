const logger = require('./logger');

const nodemailer = require('nodemailer');

if (process.env.EMAILER_PASSWORD) {
  const transport = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.NODE_ENV === 'production'
        ? '{{{emailer_email_prod}}}'
        : '{{{emailer_email_stag}}}',
      pass: process.env.EMAILER_PASSWORD,
    },
  });

  module.exports = {
    async send(recipient, subject, body) {
      logger.info(`sending email to ${recipient} with subject ${subject}`);
      await transport.sendMail({
        to: recipient,
        subject,
        html: body,
      });
    },
  };
} else {
  module.exports = {
    send() {},
  };
}
