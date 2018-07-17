import argparse
import subprocess

#sudo apt install mysql-server
#sudo apt install libmysqlclient-dev
#sudo python3 -m pip install mysqlclient
#sudo python3 -m pip install sqlalchemy
import sqlalchemy

#=====args=====#
parser=argparse.ArgumentParser()
parser.add_argument('database')
parser.add_argument('--dbms', choices=['postgres', 'mysql'], default='postgres')
args=parser.parse_args()

#=====infrastructure=====#
user=subprocess.check_output('whoami').decode().strip()
engine=sqlalchemy.create_engine(
	{
		'postgres': 'postgres:///{database}',
		'mysql': 'mysql://{user}@localhost:5432/{database}',
	}[args.dbms].format(database=args.database, user=user)
)
table_names=engine.table_names()
connection=engine.connect()

#=====basics=====#
def query(q):
	result=connection.execute(sqlalchemy.text(q))
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
	return [dictify_row(i) for i in r]

#=====niceties=====#
class TableQuerier:
	def __init__(self, table_name):
		self.columns=table_columns(table_name)

	def query(q):
		return dictify_rows(query(q), self.columns)

def table_size(name):
	return query('SELECT COUNT(*) from {};'.format(name))[0][0]

#=====postgres=====#
def pg_table_count_approx(name):
	return query("SELECT reltuples FROM pg_class WHERE relname='{}';".format(name))[0]

#=====aliases=====#
q=query
