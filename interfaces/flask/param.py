#!/usr/bin/env python3

from flask import Flask, request
app = Flask(__name__)

@app.route('/url-param/<string>/<int:integer>')
def url_param(string, integer):
    return f'{string} {integer}'

@app.route('/query-param')
def query_param():
    return f'{request.args}'

if __name__ == '__main__':
    app.run()
