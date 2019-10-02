import requests

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('api_key')
parser.add_argument('email_sender')
parser.add_argument('email_recipient')
args = parser.parse_args()

requests.post(
    'https://api.mailgun.net/v3/mail.singlekey.com/messages',
    auth=('api', args.api_key),
    data={
        'from': f'tester <{args.email_sender}>',
        'to': f'testee <{args.email_recipient}>',
        'subject': 'test subject',
        'template': 'test',
        'h:X-Mailgun-Variables': '{"test_name": "test_value"}'
    }
)
