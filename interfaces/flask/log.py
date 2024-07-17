#!/usr/bin/env python3

import logging

from flask import Flask

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S%z')
for handler in logger.handlers:
    handler.setFormatter(formatter)
logger.propagate = False

app = Flask(__name__)

@app.route('/')
def root():
    logger.info('hello')
    return {}

if __name__ == '__main__':
    logger.info('starting')
    app.run()
