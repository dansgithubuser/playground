import os
import sqlite3

if os.path.exists('db.sqlite3'): os.remove('db.sqlite3')

conn = sqlite3.connect('db.sqlite3')

conn.execute('CREATE TABLE rows (col1 INTEGER PRIMARY KEY AUTOINCREMENT, col2 TEXT)')
conn.execute("INSERT INTO rows (col2) VALUES ('hello')")
conn.execute("INSERT INTO rows (col2) VALUES ('goodbye')")
conn.commit()

print(conn.execute('SELECT * FROM rows').fetchall())
print(conn.execute('SELECT col2 FROM rows WHERE col1 = 1').fetchone())
