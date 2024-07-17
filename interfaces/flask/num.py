#!/usr/bin/env python3

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def num():
    return {
        'int': 1,
        'float': 1.0,
    }

if __name__ == '__main__':
    app.run()
