#===== imports =====#
#----- 3rd party -----#
import sqlalchemy
from sqlalchemy import orm

#----- standard -----#
import argparse
from datetime import datetime
import math

#===== args =====#
parser = argparse.ArgumentParser()
parser.add_argument('--batch-size', '-n', type=int, default=10_000)
parser.add_argument('--primary-key', '-k', default='id')
parser.add_argument('--soft-limit', '-l', type=int, default=math.inf)
parser.add_argument('src', help='username:password@host:port/db')
parser.add_argument('dst', help='username:password@host:port/db')
parser.add_argument('tables', nargs='+')
args = parser.parse_args()

#===== main =====#
# check
print(f'Destination: {args.dst}')
print('Enter yes to continue.')
assert input() == 'yes'

# engines
engine_src = sqlalchemy.create_engine('postgresql+psycopg2://' + args.src)
engine_dst = sqlalchemy.create_engine('postgresql+psycopg2://' + args.dst)

def execute(q, executor):
    return executor.execute(sqlalchemy.text(q))

def query(q, engine):
    print(engine.url, q)
    if engine == engine_dst:
        assert not globals().get('session_dst')
    with orm.Session(engine) as session:
        ret = execute(q, session)
        session.commit()
        return ret

# get tables and max IDs
table_meta = {}
for table in args.tables:
    print(f'getting metadata for {table}')
    table_src = sqlalchemy.Table(table, sqlalchemy.schema.MetaData(), autoload_with=engine_src)
    table_dst = sqlalchemy.Table(table, sqlalchemy.schema.MetaData(), autoload_with=engine_dst)
    id_src = query(f'SELECT max({args.primary_key}) FROM {table}', engine_src).scalar_one() or 0
    id_dst = query(f'SELECT max({args.primary_key}) FROM {table}', engine_dst).scalar_one() or 0
    table_meta[table] = (table_src, id_src, table_dst, id_dst)

# siphon
session_dst = orm.Session(engine_dst)
for table in args.tables:
    table_src, id_src, table_dst, id_dst = table_meta[table]
    print(f'\n===== {table} =====')
    print(f'dst max ID: {id_dst}')
    print(f'src max ID: {id_src}')
    inserted = 0
    while id_dst < id_src:
        print(f'{datetime.now().isoformat()} {id_dst} / {id_src}')
        with orm.Session(engine_src) as session:
            rows = session.execute(
                sqlalchemy.select(table_src)
                .where(table_src.c[args.primary_key] > id_dst)
                .order_by(table_src.c[args.primary_key] )
                .limit(args.batch_size)
            )
        rows = [row._mapping for row in rows]
        session_dst.execute(
            sqlalchemy.insert(table_dst),
            rows,
        )
        id_dst = max(row[args.primary_key] for row in rows)
        inserted += len(rows)
        execute(f'''SELECT setval('{table}_id_seq', {id_dst+1})''', session_dst)
        session_dst.commit()
        if inserted >= args.soft_limit: break
