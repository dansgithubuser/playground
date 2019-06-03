import argparse
import os
import sys

import flask
import google_auth_oauthlib.flow
from OpenSSL import SSL
import requests

# run with FLASK_APP=googlephotos.py flask run
# go to http://localhost:5000 in browser
if sys.argv[0].endswith('flask'):
    '''
    example client_secrets.json:
    {
      "installed": {
        "client_id": "YOUR_CLIENT_ID_HERE",
        "client_secret": "YOUR_CLIENT_SECRET_HERE",
        "redirect_uris": ["http://localhost:5000/redirect"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token"
      }
    }
    '''
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/photoslibrary'],
    )
    flow.redirect_uri = 'http://localhost:5000/redirect'
    authorization_url, state = flow.authorization_url(access_type='offline')

    app = flask.Flask('oauth_app')

    @app.route('/')
    def root():
        return flask.redirect(authorization_url)

    @app.route('/redirect')
    def redirect():
        flow.fetch_token(authorization_response=flask.request.url)
        result = {
            'access_token': flow.credentials.token,
            'refresh_token': flow.credentials.refresh_token,
        }
        return result

else:
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', action='store_true')
    args = parser.parse_args()

    if args.upload:
        REFRESH_TOKEN = os.environ['GOOGLE_PHOTOS_REFRESH_TOKEN']

        with open('../gull.jpg', 'rb') as f: gull = f.read()

        response = requests.post('https://photoslibrary.googleapis.com/v1/uploads',
            headers={
                'Authorization': 'Bearer {}'.format(OAUTH2_TOKEN),
                'Content-type': 'Application/octet-stream',
                'X-Goog-Upload-File-Name': 'gull.jpg',
                'X-Goog-Upload-Protocol': 'raw',
            },
            data=gull,
        )
