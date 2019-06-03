import psycopg2
import psycopg2.extras

import os

_conn=psycopg2.connect('host={DAN_DB_HOST} port={DAN_DB_PORT} dbname={DAN_DB_NAME} user={DAN_DB_USER} password={DAN_DB_PASSWORD}'.format(**os.environ))
_cur=_conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

def q(query):
	_cur.execute(query)
	result=_cur.fetchall()
	if len(result)==1: result=result[0]
	return result
