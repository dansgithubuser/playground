#!/usr/bin/env python3

from flask import Flask, request
app = Flask(__name__)

@app.post('/')
def root_post():
    return f'{request.form}'

@app.get('/')
def root_get():
    return 'get'

if __name__ == '__main__':
    app.run()
