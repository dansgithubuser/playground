import flask

app = flask.Flask(__name__)

@app.put("/upload")
def upload():
    content = flask.request.data
    offset = flask.request.headers.get('Content-Range')
    print(f'got content, size is {len(content)}, offset is {offset}')
    return ('OK', 200)

app.run()
