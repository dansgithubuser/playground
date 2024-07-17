import os
import sqlite3

if os.path.exists('db.sqlite3'): os.remove('db.sqlite3')

con = sqlite3.connect('db.sqlite3')

con.execute('CREATE TABLE rows (col1 INTEGER PRIMARY KEY AUTOINCREMENT, col2 TEXT, col3 JSONB)')
con.execute("INSERT INTO rows (col2) VALUES ('hello')")
con.execute("INSERT INTO rows (col2) VALUES ('goodbye')")
con.execute('''INSERT INTO rows (col3) VALUES ('{"a": 1}')''')
con.commit()

print(con.execute('SELECT * FROM rows').fetchall())
print(con.execute('SELECT col2 FROM rows WHERE col1 = 1').fetchone())
print(con.execute('SELECT col3 FROM rows WHERE col1 = 3').fetchone())
