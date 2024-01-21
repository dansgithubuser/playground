#!/usr/bin/env python3

import xmpp

import argparse
import getpass

parser = argparse.ArgumentParser()
parser.add_argument('id', help='example: name@example.com')
parser.add_argument('--ssl', action='store_true', help='NOTE! SSL: WRONG_VERSION_NUMBER might be a red herring!')
args = parser.parse_args()

jid = xmpp.protocol.JID(args.id)
client = xmpp.Client(server=jid.getDomain(), debug=True)
print('connecting')
client.connect(secure=1 if args.ssl else None)
print('connected')
print('authing')
password = getpass.getpass()
client.auth(user=jid.getNode(), password=password, resource=jid.getResource())
print('authed')
