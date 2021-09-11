import os
import sqlite3

if os.path.exists('db.sqlite3'): os.remove('db.sqlite3')

conn = sqlite3.connect('db.sqlite3')

conn.execute('CREATE TABLE rows (col1 INTEGER PRIMARY KEY AUTOINCREMENT, col2 TEXT, col3 JSONB)')
conn.execute("INSERT INTO rows (col2) VALUES ('hello')")
conn.execute("INSERT INTO rows (col2) VALUES ('goodbye')")
conn.execute('''INSERT INTO rows (col3) VALUES ('{"a": 1}')''')
conn.commit()

print(conn.execute('SELECT * FROM rows').fetchall())
print(conn.execute('SELECT col2 FROM rows WHERE col1 = 1').fetchone())
print(conn.execute('SELECT col3 FROM rows WHERE col1 = 3').fetchone())
