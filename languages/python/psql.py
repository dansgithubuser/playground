#!/usr/bin/env python3

import argparse
import json
import os
import pprint
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--dbname', '-d')
parser.add_argument('--username', '-U')
parser.add_argument('--password')
parser.add_argument('statement')
args = parser.parse_args()

class Querier:
    def __init__(self, host, dbname, username, password=None):
        self.host = host
        self.dbname = dbname
        self.username = username
        self.password = password

    def __call__(self, statement):
        json_statement = f'''
            WITH x AS ({statement})
            SELECT json_agg(row_to_json(x))
            FROM x
        '''
        env = {**os.environ}
        if self.password: env['PGPASSWORD'] = self.password
        p = subprocess.run(
            [
                'psql',
                '-h', self.host,
                '-d', self.dbname,
                '-U', self.username,
                '-t',
                '--quiet',
                '-c', json_statement,
            ],
            env=env,
            check=True,
            capture_output=True,
        )
        return [
            json.loads(i.strip())
            for i in p.stdout.decode().splitlines()
            if i.strip() != ''
        ]

querier = Querier(args.host, args.dbname, args.username, args.password)
pprint.pprint(querier(args.statement))
