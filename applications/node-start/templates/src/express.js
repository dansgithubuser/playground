//===== requires =====//
// in-repo
const consts = require('./consts');
const emailer = require('./emailer'); // eslint-disable-line no-unused-vars
const globals = require('./globals');
const logger = require('./logger');
const models = require('./models');

// packages
const AdminBroExpress = require('@admin-bro/express');
const AdminBroSequelize = require('@admin-bro/sequelize');
const AdminBro = require('admin-bro');
const bodyParser = require('body-parser');
const connectSessionSequelize = require('connect-session-sequelize');
const cors = require('cors');
const express = require('express');
const session = require('express-session');
const _ = require('lodash');
const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const sequelize = require('sequelize');

// node
const fs = require('fs');
const https = process.env.NODE_ENV === 'development' ? require('http') : require('https');

//===== consts =====//
const { Op } = sequelize; // eslint-disable-line no-unused-vars

const app = express();
app.disable('x-powered-by');

//===== helpers =====//
function asyncHandler(callback) {
  return (req, res, next) => {
    callback(req, res, next).catch((e) => {
      logger.errorNice(`responding to ${req.url}`, e);
      next(e);
    });
  };
}

function sendRespectingPartialContent(req, res, bytes) { // eslint-disable-line no-unused-vars
  if (req.get('Range')) {
    let [start, end] = req.get('Range').replace('bytes=', '').split('-');
    if (end === '') end = bytes.length - 1;
    res.set('Content-Range', `bytes ${start}-${end}/${bytes.length}`);
    res.set('Accept-Ranges', 'bytes');
    res.set('Content-Length', end - start + 1);
    const partial = bytes.slice(parseInt(start, 10), parseInt(end, 10) + 1);
    return res.status(206).send(partial);
  }
  return res.send(bytes);
}

//===== passport =====//
passport.use(new LocalStrategy(
  {
    usernameField: 'email',
  },
  async (email, password, done) => {
    try {
      const user = await models.User.findOne({ where: { email } });
      if (!user) {
        return done(null, false, { message: 'Incorrect email.' });
      }
      if (!await user.checkPassword(password)) {
        return done(null, false, { message: 'Incorrect password.' });
      }
      return done(null, user);
    } catch (e) {
      return done(e);
    }
  },
));

passport.serializeUser((user, done) => {
  done(null, user.id);
});

passport.deserializeUser(async (id, done) => {
  try {
    const user = await models.User.findByPk(id);
    done(null, user);
  } catch (e) {
    done(e);
  }
});

//===== middlewares =====//
// log
app.use((req, res, next) => {
  const start = new Date();
  res.on('close', () => {
    const duration = new Date() - start;
    let logFn;
    if (res.statusCode >= 500) {
      logFn = logger.error;
    } else if (duration > 1000) {
      logFn = logger.warn;
    } else if (globals.controls.log_all_http) {
      logFn = logger.info;
    }
    if (logFn) logFn(`[${new Date()}] ${req.method} ${req.url} ${res.statusCode} user ${_.get(req, 'user.id')} ${duration} ms`);
  });
  next();
});

// static
app.use(express.static('static'));

// session
const SequelizeStore = connectSessionSequelize(session.Store);
const store = new SequelizeStore({ db: models.sequelize });
store.sync();
app.use(session({
  name: '{{{project_name}}}-session-id',
  secret: process.env.SESSION_SECRET,
  store,
  cookie: {
    sameSite: {
      production: 'strict',
      staging: 'none',
    }[process.env.NODE_ENV],
    httpOnly: false,
    secure: ['staging', 'production'].includes(process.env.NODE_ENV),
    maxAge: 7 * 24 * 60 * 60 * 1000,
  },
  resave: false,
  saveUninitialized: false,
}));

// JSON
app.use(bodyParser.json());

// passport
app.use(passport.initialize());
app.use(passport.session());

// CORS
app.use(cors({
  origin: process.env.NODE_ENV === 'production'
    ? [
      'https://{{{hostname_prod}}}',
    ]
    : (origin, callback) => callback(null, origin),
  credentials: true,
}));

// content security policy
app.use((req, res, next) => {
  res.set('Content-Security-Policy', "frame-ancestors 'none';");
  next();
});

// no caching by default
app.use((req, res, next) => {
  if (!res.get('Cache-Control')) res.set('Cache-Control', 'no-store');
  next();
});

// raw
app.use(express.raw({ limit: '200MB' }));

//===== auth routes =====//
const authRouter = express.Router();

authRouter.post('/signup', asyncHandler(async (req, res) => {
  if (!req.body) return res.status(400).send('Missing body.');
  if (!req.body.email) return res.status(400).send('Missing email.');
  if (!req.body.password) return res.status(400).send('Missing password.');
  if (models.User.isPasswordShort(req.body.password)) return res.status(400).send('Password too short.');
  if (await models.User.findOne({ where: { email: req.body.email } })) {
    return res.status(400).send('Already signed up.');
  }
  await models.User.createSecure({
    email: req.body.email,
    password: req.body.password,
  });
  return res.sendStatus(200);
}));

authRouter.post(
  '/login',
  (req, res, next) => {
    req.body.email = req.body.email.toLowerCase();
    next();
  },
  passport.authenticate('local'),
  (req, res) => { res.sendStatus(200); },
);

authRouter.post(
  '/logout',
  (req, res) => {
    req.logout();
    res.sendStatus(200);
  },
);

function authenticator({ admin }) {
  return (req, res, next) => {
    // if you wanna debug admin bro locally, just skip auth
    if (!req.isAuthenticated()) return res.sendStatus(401);
    if (admin && !req.user.admin) return res.sendStatus(404);
    return next();
  };
}

//===== regular routes =====//
const regularRouter = express.Router();
regularRouter.use(authenticator({}));

regularRouter.get('/hello/world', asyncHandler(async (req, res) => {
  return res.send('Hello, world!');
}));

//==== admin routes =====//
const adminRouter = express.Router();
adminRouter.use(authenticator({ admin: true }));

// bro
AdminBro.registerAdapter(AdminBroSequelize);
const adminBro = new AdminBro({
  databases: [models],
  rootPath: '/admin/bro',
});
adminRouter.use('/bro', AdminBroExpress.buildRouter(adminBro));

// control
adminRouter.post('/control/:id', asyncHandler(async (req, res) => {
  globals.controls[req.params.id] = req.body.value;
  return res.sendStatus(200);
}));

//===== routers =====//
app.use('/auth', authRouter);
app.use('/', regularRouter);
app.use('/admin', adminRouter);

//===== exports =====//
function init() {
  if (['production', 'staging'].includes(process.env.NODE_ENV)) {
    const key = fs.readFileSync('letsencrypt/privkey.pem');
    const cert = fs.readFileSync('letsencrypt/fullchain.pem');
    https.createServer({ key, cert }, app).listen(
      443,
      () => logger.info(`listening on port 443, NODE_ENV is ${process.env.NODE_ENV}`),
    );
    const httpRedirecter = express();
    httpRedirecter.get('*', (req, res) => res.redirect(`https://${req.headers.host}${req.url}`));
    httpRedirecter.listen(80, () => logger.info('redirecting on port 80'));
  } else {
    app.listen(
      consts.port,
      () => logger.info(`listening on port ${consts.port}, NODE_ENV is ${process.env.NODE_ENV}`),
    );
  }
}

module.exports = {
  app,
  init,
};
