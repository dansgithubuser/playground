#!/usr/bin/env python3

'''
trust all local connections as postgres
find the `hba_file`
`psql -c "SHOW hba_file"`
edit this line
`local all postgres peer`
change `peer` to `trust
`local all postgres trust`
'''

import sqlalchemy
import sqlalchemy.orm

import os
import typing

class Querier:
    def __init__(self, db_name, db_user='postgres'):
        self.engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{db_user}@/{db_name}')
        self.conn = self.engine.connect()

    def __call__(self, s, ok_errs=[]):
        try:
            return self.conn.execute(sqlalchemy.text(s))
        except sqlalchemy.exc.ProgrammingError as e:
            if e.orig.__class__.__name__ not in ok_errs:
                raise

    def session(self):
        return Session(self.engine)

class Session(sqlalchemy.orm.Session):
    def select(self, *args, **kwargs):
        return self.execute(sqlalchemy.select(*args, **kwargs))

def ensure_db(db_name):
    q = Querier('postgres')
    q('COMMIT')  # can't make a db inside a transaction
    q(f'CREATE DATABASE {db_name}', ['DuplicateDatabase'])

ensure_db('dansgithubuser_playground_pg')
q = Querier('dansgithubuser_playground_pg')
q(
    '''
        CREATE TABLE people (
            id SERIAL PRIMARY KEY,
            name TEXT
        )
    ''',
    ['DuplicateTable'],
)
q('COMMIT')
for name in ['alice', 'bob', 'charlie']:
    q(f'''INSERT INTO people(name) VALUES ('{name}')''')
q('COMMIT')
print('SQL substr is awful. It is 1-indexed and silently handles out-of-bound indices.')
for row in q('SELECT id, substr(name, 0, 3) FROM people'):
    print(row)

class Base(sqlalchemy.orm.DeclarativeBase):
    '''
    Without this, we get:
    `sqlalchemy.exc.InvalidRequestError: Cannot use 'DeclarativeBase' directly as a declarative base class. Create a Base by creating a subclass of it.`
    '''
    pass

class People(Base):
    __tablename__ = 'people'
    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)
    name: sqlalchemy.orm.Mapped[typing.Optional[str]]

with q.session() as s:
    print('''Would you look at that? SQLAlchemy's substr is the exact same awfulness.''')
    for row in s.select(sqlalchemy.func.substr(People.name, 0, 3)):
        print(row)
