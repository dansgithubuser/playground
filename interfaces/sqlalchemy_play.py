import argparse
import pprint
import subprocess
import sys
import traceback

#sudo apt install mysql-server
#sudo apt install libmysqlclient-dev
#sudo python3 -m pip install mysqlclient
#sudo python3 -m pip install sqlalchemy
import sqlalchemy

#=====args=====#
parser=argparse.ArgumentParser()
parser.add_argument('database')
parser.add_argument('--dbms', choices=['postgres', 'mysql'], default='postgres')
parser.add_argument('--user', '-u')
parser.add_argument('--password', '-p')
args=parser.parse_args()

#=====infrastructure=====#
engine=sqlalchemy.create_engine(
    {
        'postgres': 'postgres:///{database}',
        'mysql': 'mysql://{user}{password}@localhost:5432/{database}',
    }[args.dbms].format(
        database=args.database,
        user=args.user or subprocess.check_output('whoami').decode().strip(),
        password=':'+args.password if args.password else '',
    )
)
table_names = engine.table_names()
connection = engine.connect()

#=====basics=====#
def query(q):
    try:
        result = connection.execute(q)
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        try:
            result = connection.execute(sqlalchemy.text(q))
        except Exception:
            print('exception when querying normally')
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            print('exception when querying converted to text')
            raise
    if result.returns_rows: return [i for i in result]
    return result

def table_detail(name):
    return sqlalchemy.Table(name, sqlalchemy.MetaData(),
        autoload=True, autoload_with=engine)

def table_columns(name):
    return [i.name for i in table_detail(name).columns]

def dictify_row(r, columns):
    return {columns[i]: r[i] for i in range(len(columns))}

def dictify_rows(r, columns):
    return [dictify_row(i, columns) for i in r]

#=====niceties=====#
class TableQuerier:
    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = table_columns(table_name)

    def __repr__(self):
        return self.table_name+'\n'+pprint.pformat(self.columns)

    def __call__(self, q):
        return dictify_rows(query(q), self.columns)

    def all(self):
        return self('select * from {}'.format(self.table_name))

    def where(self, **kwargs):
        field, value = [(k, v) for k, v in kwargs.items()][0]
        if type(value) == str: value = "'{}'".format(value)
        return self('select * from {} where {} = {}'.format(self.table_name, field, value))

def table_size(name):
    return query('SELECT COUNT(*) from {};'.format(name))[0][0]

#=====postgres=====#
def pg_table_count_approx(name):
    return query("SELECT reltuples FROM pg_class WHERE relname='{}';".format(name))[0]

#=====aliases=====#
q=query
