#! /usr/bin/env python3

#===== imports =====#
import argparse
import collections
import copy
import datetime
import getpass
import glob
import json
import os
import re
import shutil
import signal
import subprocess
import sys

for optional_import in [
    'import requests',
    'import sqlalchemy',
]:
    try:
        exec(optional_import)
    except:
        pass

#===== args =====#
parser = argparse.ArgumentParser()

# setup
parser.add_argument('--full-dev-setup', '--fds', action='store_true', help="Do this if you haven't already! Or use individual steps below.")
parser.add_argument('--dotenv-dev', '--ded', action='store_true', help='Set up an env file, part of dev setup')
parser.add_argument('--db-create', '--dbc', action='store_true')
parser.add_argument('--db-drop', '--dbd', action='store_true')
parser.add_argument('--db-user-create', '--dbuc', action='store_true')
parser.add_argument('--db-user-create-read-only', '--dbucr', action='store_true')
parser.add_argument('--db-user-drop', '--dbud', action='store_true')
parser.add_argument('--db-user-drop-read-only', '--dbudr', action='store_true')
parser.add_argument('--db-fresh', '--dbf', action='store_true')
parser.add_argument('--db-dry-sql', action='store_true', help="print SQL commands; useful for setting up a machine that can't run this script")
parser.add_argument('--certbot', action='store_true', help='to be run on host machine')
parser.add_argument('--certbot-extra', default='', help='extra args to pass to certbot')

# development
parser.add_argument('--run', '-r', action='store_true')
parser.add_argument('--profile', action='store_true')
parser.add_argument('--debug-log', '-d', action='store_true')
parser.add_argument('--lint', '-l', action='store_true')
parser.add_argument('--require-circular', action='store_true')
parser.add_argument('--test', '-t', nargs='?', const='')
parser.add_argument('--db-interact', '--dbi', '-i', action='store_true')
parser.add_argument('--db-query-to-file')
parser.add_argument('--db-export', '--dbe', metavar='query')
parser.add_argument('--sequelize-cli', '--seq', '-s')
parser.add_argument('--db-migrate', '--dbm', action='store_true')
parser.add_argument('--db-rollback', '--dbr')
parser.add_argument('--db-migration-list', '--dbml', action='store_true')
parser.add_argument('--db-migrate-make', '--dbmm', metavar='name:like')

# deploy
parser.add_argument('--docker-build', '--dkrb', action='store_true')
parser.add_argument('--docker-push', '--dkrp', action='store_true')
parser.add_argument('--deploy-staging', '--ds', choices=['only'], nargs='?', const=True)
parser.add_argument('--deploy-production', '--dp', choices=['only'], nargs='?', const=True)
parser.add_argument('--deploy-skip-migrate', action='store_true')

# ops
parser.add_argument('--control-set', metavar='id:value')
parser.add_argument('--control-unset', metavar='id')

# probing
parser.add_argument('--signup', action='store_true')

# config
parser.add_argument('--email',
    default=os.environ.get('{{{project_name.upper().replace('-', '_')}}}_EMAIL'),
    help='defaults to env var {{{project_name.upper().replace('-', '_')}}}_EMAIL',
)
parser.add_argument('--env', '-e', choices=['dev', 'stag', 'prod'], default='dev')
parser.add_argument('--service',
    choices=[
        'main',
        'db',
        'all',
    ],
    default='main',
)

args = parser.parse_args()

if args.deploy_staging:
    args.env = 'stag'
elif args.deploy_production:
    args.env = 'prod'

#===== consts =====#
DIR = os.path.dirname(os.path.realpath(__file__))

DOCKER_REGISTRY = '{{{docker_registry_hostname}}}'
DOCKER_REGISTRY_PW = '{{{docker_registry_password}}}'
DOCKER_TAG = f'{DOCKER_REGISTRY}/{{{project_name}}}-{args.env}'

ENV_PATH = '/root/{{{project_name}}}/env'
STATIC_PATH = '/root/{{{project_name}}}/static'

if args.env == 'dev':
    ORIGIN = 'http://localhost:8000'
elif args.env == 'stag':
    HOSTNAME = '{{{hostname_stag}}}'
    POSTGRES_DATA_PATH = '{{{postgres_data_path_stag}}}'
elif args.env == 'prod':
    HOSTNAME = '{{{hostname_prod}}}'
    POSTGRES_DATA_PATH = '{{{postgres_data_path_prod}}}'

if args.env in ['stag', 'prod']:
    ORIGIN = f'https://{HOSTNAME}'
    ROOT_AT_HOSTNAME = f'root@{HOSTNAME}'

UUID = '5a4958fb-611f-49ed-9227-28c7b94e9e9a'

#===== setup =====#
os.chdir(DIR)

#===== helpers =====#
def blue(text):
    return '\x1b[34m' + text + '\x1b[0m'

def red(text):
    return '\x1b[31m' + text + '\x1b[0m'

def timestamp():
    return '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())

def invoke(
    *args,
    popen=False,
    no_split=False,
    out=False,
    quiet=False,
    **kwargs,
):
    if len(args) == 1 and not no_split:
        args = args[0].split()
    if not quiet:
        print(blue('-'*40))
        print(timestamp())
        print(os.getcwd()+'$', end=' ')
        if any([re.search(r'\s', i) for i in args]):
            print()
            for i in args: print(f'\t{i} \\')
        else:
            for i, v in enumerate(args):
                if i != len(args)-1:
                    end = ' '
                else:
                    end = ';\n'
                print(v, end=end)
        if kwargs: print(kwargs)
        if popen: print('popen')
        print()
    if kwargs.get('env') != None:
        env = copy.copy(os.environ)
        env.update(kwargs['env'])
        kwargs['env'] = env
    if popen:
        return subprocess.Popen(args, **kwargs)
    else:
        if 'check' not in kwargs: kwargs['check'] = True
        if out: kwargs['capture_output'] = True
        result = subprocess.run(args, **kwargs)
        if out:
            result = result.stdout.decode('utf-8')
            if out != 'exact': result = result.strip()
        return result

def invoke_target(*args, **kwargs):
    return invoke('ssh', ROOT_AT_HOSTNAME, ' '.join(args), **kwargs)

def cp_to_target(src, dst, quiet=False):
    invoke('scp', src, f'{ROOT_AT_HOSTNAME}:{dst}', quiet=quiet, out=quiet)

def psqlc(command, db='', quiet=False, use_file=False):
    if not quiet: print(command)
    if args.db_dry_sql: return
    if use_file:
        with open('.tmp.sql', 'w') as file: file.write(command)
    invocation = ['su', '-', 'postgres', '-c']
    if use_file:
        invocation.append(f'psql {db} -f .tmp.sql')
    else:
        invocation.append(f'psql {db} -c "{command}"')
    if getpass.getuser() != 'root':
        invocation.insert(0, 'sudo')
    invoke(*invocation, quiet=quiet)

def psqlc_target(command, options='', quiet=False, use_file=False):
    if not quiet: print(command)
    if use_file:
        with open('.tmp.sql', 'w') as file: file.write(command)
        cp_to_target('.tmp.sql', '.', quiet=True)
        invoke_target('docker cp .tmp.sql {{{project_name}}}-db:.tmp.sql', quiet=True)
    separator = f'({UUID})'
    result = invoke_target(
        ' '.join([
            'docker exec {{{project_name}}}-db',
                f'psql {dotenv_get("DB")} {dotenv_get("DB_USER")}',
                    '-f .tmp.sql' if use_file else f'-c "{command}"',
                    '-t',
                    '--no-align',
                    f'-F "{separator}"',
                    options,
        ]),
        out=True,
        quiet=True,
    )
    return [line.split(separator) for line in result.splitlines()]

def sqlalchemy_connect():
    db_user = dotenv_get('DB_USER')
    db_pw = dotenv_get('DB_PW')
    db_host = dotenv_get('DB_HOST')
    db = dotenv_get('DB')
    engine = sqlalchemy.create_engine(f'postgresql://{db_user}:{db_pw}@{db_host}/{db}')
    return engine.connect()

class Querier:
    def __init__(self, conn=None):
        if conn:
            self.conn = conn
            self.env = None
        else:
            self.env = args.env
        if self.env == 'dev':
            self.conn = sqlalchemy_connect()

    def all(self, query, quiet=False, use_file=False):
        cols = re.search('SELECT(.*)FROM', query, re.DOTALL)
        if cols:
            cols = re.findall(
                r' AS (\w+)(?:,|$)',
                cols.group(1).strip(),
            )
            Row = collections.namedtuple('Row', cols)
        if self.env in [None, 'dev']:
            rows = [i for i in self.conn.execute(query)]
        elif self.env in ['stag', 'prod']:
            rows = [
                [Querier._treat(col) for col in row]
                for row in psqlc_target(query, quiet=quiet, use_file=use_file)
            ]
        if cols:
            return [
                Row(*row)
                for row in rows
            ]
        else:
            return rows

    def one(self, query, quiet=False):
        return self.all(query, quiet)[0]

    def exec(self, query):
        self.conn.execute(query)

    def _treat(col):
        # datetime
        try:
            dt, tz = col.split('+')
            decimal_split = dt.split('.')
            if len(decimal_split) != 1:
                dt += '0' * (3 - len(decimal_split[1]))
            assert tz == '00'
            return datetime.datetime.fromisoformat(dt+'+00:00')
        except:
            pass
        # JSON
        try:
            return json.loads(col)
        except:
            pass
        # boolean
        if col in ['t', 'true']: return True
        if col in ['f', 'false']: return False
        # default
        return col

def dotenv_get(var):
    with open('env/env') as env:
        lines = env.readlines()
    for line in lines:
        if line.startswith(var+'='):
            return line[len(var)+1:].strip()

def git_state():
    diff = invoke('git diff', out=True)
    diff_cached = invoke('git diff --cached', out=True)
    with open('git-state.txt', 'w') as git_state:
        git_state.write(invoke('git show --name-only', out=True)+'\n')
        if diff:
            git_state.write('\n===== diff =====\n')
            git_state.write(diff+'\n')
        if diff_cached:
            git_state.write('\n===== diff --cached =====\n')
            git_state.write(diff_cached+'\n')

def creds_guard():
    if not args.email: raise Exception('Email not set, see `--email` option.')
    if '{{{project_name.upper().replace('-', '_')}}}_PASSWORD' not in os.environ:
        raise Exception('Password not set, please set `{{{project_name.upper().replace('-', '_')}}}_PASSWORD` env var.')

def auth():
    creds_guard()
    session = requests.Session()
    session.post(f'{ORIGIN}/auth/login', json={
        'email': args.email,
        'password': os.environ['{{{project_name.upper().replace('-', '_')}}}_PASSWORD'],
    })
    return session

#===== main =====#
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

#----- setup -----#
if args.full_dev_setup:
    invoke('npm ci')

if args.dotenv_dev or args.full_dev_setup:
    shutil.copy('env/dev', 'env/env')

if args.db_drop or args.db_fresh:
    psqlc(f'DROP DATABASE {dotenv_get("DB")}')

if args.db_user_drop or args.db_fresh:
    db_user = dotenv_get('DB_USER')
    psqlc(f'DROP OWNED BY {db_user}')
    psqlc(f'DROP USER {db_user}')

if args.db_user_drop_read_only:
    db_user = dotenv_get('DB_USER') + '_read_only'
    psqlc(f'DROP OWNED BY {db_user}')
    psqlc(f'DROP USER {db_user}')

if args.db_create or args.full_dev_setup or args.db_fresh:
    psqlc(f'CREATE DATABASE {dotenv_get("DB")};')

if args.db_user_create or args.full_dev_setup or args.db_fresh:
    db_user = dotenv_get('DB_USER')
    psqlc(f'''CREATE USER {db_user} WITH PASSWORD '{dotenv_get("DB_PW")}';''')
    psqlc(f'GRANT ALL PRIVILEGES ON DATABASE {dotenv_get("DB")} TO {db_user};')

if args.db_user_create_read_only:
    db = dotenv_get('DB')
    db_user = dotenv_get('DB_USER') + '_read_only'
    psqlc(f'''CREATE USER {db_user} WITH PASSWORD '{dotenv_get("DB_PW")}';''')
    psqlc(f'GRANT CONNECT ON DATABASE {db} TO {db_user};')
    psqlc(f'GRANT USAGE ON SCHEMA public TO {db_user};', db)
    psqlc(f'GRANT SELECT ON ALL TABLES IN SCHEMA public TO {db_user};', db)
    psqlc(f'ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO {db_user};', db)

if args.full_dev_setup or args.db_fresh:
    invoke('npm run sequelize-cli db:migrate')

if args.certbot:
    try:
        invoke('certbot --version')
    except:
        invoke('snap install core')
        invoke('snap refresh core')
        invoke('snap install --classic certbot')
    if args.env == 'prod':
        extra_hostnames = '-d access.foresightanalytics.ca -d portal.foresightanalytics.ca'
    else:
        extra_hostnames = ''
    invoke(
        'certbot certonly '
        '--webroot '
        '-w ./static '
        '-n '
        f'-d {HOSTNAME} {extra_hostnames} '
        '--agree-tos '
        f'--email daniel@x-matik.com '
        f'{args.certbot_extra} '
    )
    print('now copy live fullchain.pem and privkey.pem to ./letsencrypt and restart')

#----- development -----#
if args.run:
    env = {
        'NODE_ENV': 'development',
    }
    if args.debug_log:
        env = {'LOG_LEVEL': 'debug'}
    invoke('npm run nodemon', env=env)

if args.profile:
    env = {
        'NODE_ENV': 'development',
    }
    p = invoke('npm run profile', popen=True, env=env)
    signal.signal(signal.SIGINT, lambda *args: p.send_signal(signal.SIGINT))
    p.wait()
    log = max(glob.glob('isolate-*'), key=os.path.getctime)
    processed = invoke(f'node --prof-process {log}', out=True)
    with open('profile.txt', 'w') as file: file.write(processed)
    print('output saved to profile.txt')

if args.lint:
    invoke('npm run lint .')

if args.require_circular:
    # npm install -g madge
    invoke('madge --circular .', check=False)

if args.test != None:
    env = {}
    if args.debug_log:
        env = {'LOG_LEVEL': 'debug'}
    shutil.rmtree('logs', ignore_errors=True)
    invoke(f'npm run test -- {args.test}', env=env, check=False)

if args.db_interact:
    if args.env == 'dev':
        invoke(
            'psql',
            '-h', dotenv_get('DB_HOST'),
            '-p', dotenv_get('DB_PORT'),
            dotenv_get('DB'),
            dotenv_get('DB_USER'),
            env={'PGPASSWORD': dotenv_get('DB_PW')},
        )
    elif args.env in ['stag', 'prod']:
        db_user = dotenv_get("DB_USER")
        if os.environ.get('PLZ'):
            print('Are you sure?')
            if input() != 'pigsnout':
                raise Exception('Not sure.')
        else:
            db_user += '_read_only'
        invoke(f'ssh -t {ROOT_AT_HOSTNAME} docker exec -it {{{project_name}}}-db psql {dotenv_get("DB")} {db_user}')

if args.db_query_to_file:
    contents = invoke_target(
        ' '.join([
            'docker exec {{{project_name}}}-db',
                f'psql {dotenv_get("DB")} {dotenv_get("DB_USER")}',
                    f'-c "{args.db_query_to_file}"',
        ]),
        out='exact',
    )
    with open('file', 'w') as file: file.write(contents)

if args.db_export:
    query = args.db_export
    table = re.search('from ([^ ]+)', query.lower()).group(1)
    with open(table+'.json', 'w') as file:
        file.write(
            invoke(
                'psql',
                '-h', dotenv_get('DB_HOST'),
                '-p', dotenv_get('DB_PORT'),
                dotenv_get('DB'),
                dotenv_get('DB_USER'),
                '-c', f"COPY (SELECT json_agg(t) FROM ({query}) t) TO STDOUT",
                env={'PGPASSWORD': dotenv_get('DB_PW')},
                out=True,
            ).replace('\\n', '\n')+'\n'
        )

if args.sequelize_cli != None:
    invoke(f'npm run sequelize-cli -- {args.sequelize_cli}')

if args.db_migrate:
    invocation = 'npm run sequelize-cli db:migrate'
    if args.env == 'dev':
        invoke(invocation)
    else:
        invoke_target(f'docker exec {{{project_name}}}-main {invocation}')

if args.db_rollback:
    invocation = f'npm run sequelize-cli -- db:migrate:undo --name {args.db_rollback}'
    if args.env == 'dev':
        invoke(invocation)
    else:
        print(f'I will roll back {args.db_rollback} on env {args.env}. Is that right? Enter for yes, ctrl-c for no.')
        input()
        invoke_target(f'docker exec {{{project_name}}}-main {invocation}')

if args.db_migration_list:
    invocation = 'npm run sequelize-cli db:migrate:status'
    if args.env == 'dev':
        migrations = invoke(invocation, out=True, quiet=True).splitlines()
    else:
        migrations = invoke_target(
            f'docker exec {{{project_name}}}-main {invocation}',
            out=True,
            quiet=True,
        ).splitlines()
    for i in migrations:
        if (re.match('^down', i)):
            print(red(i))
        else:
            print(blue(i))

if args.db_migrate_make:
    split = args.db_migrate_make.split(':')
    likes = list(filter(lambda i: split[1] in i, glob.glob('migrations/*')))
    if len(likes) != 1: raise Exception(f'ambiguous: {likes}')
    name = split[0]
    like = likes[0]
    invoke(f'npm run sequelize-cli -- migration:generate --name {name}')
    dst = sorted(os.listdir('migrations'))[-1]
    print(f'copying {like} ---> migrations/{dst}')
    shutil.copy(like, f'migrations/{dst}')

#----- deploy -----#
if args.deploy_production:
    print(f'You are deploying production. Service is {args.service}. Enter "PROD" to continue, ctrl-c to abort.')
    assert input() == 'PROD'

if args.docker_build or args.deploy_staging == True or args.deploy_production == True:
    git_state()
    invoke(f'docker image rm {DOCKER_TAG}', check=False)
    invoke(f'docker build -t {DOCKER_TAG} .')

if args.docker_push or args.deploy_staging == True or args.deploy_production == True:
    invoke(f'docker login -u xmatik -p {DOCKER_REGISTRY_PW} {DOCKER_REGISTRY}')
    invoke(f'docker push {DOCKER_TAG}')

if args.deploy_staging or args.deploy_production:
    invoke_target('mkdir {{{project_name}}}', check=False)
    git_state()
    for i in [
        'do.py',
        'docker-compose.yml',
        'git-state.txt',
    ]:
        cp_to_target(i, '{{{project_name}}}')
    invoke_target('mkdir {{{project_name}}}/letsencrypt', check=False)
    invoke_target('mkdir {{{project_name}}}/logs', check=False)
    try:
        invoke_target(f'cp /etc/letsencrypt/live/{HOSTNAME}/privkey.pem {{{project_name}}}/letsencrypt/')
        invoke_target(f'cp /etc/letsencrypt/live/{HOSTNAME}/fullchain.pem {{{project_name}}}/letsencrypt/')
    except Exception as e:
        print("Couldn't grab web creds, it's probably time to run `./do.py --certbot` on host machine.")
        print("This is also a good time to set up the env dotfile and database.")
        print("Here's the exception just in case I'm confused:")
        print(e)
        sys.exit()
    try:
        invoke_target('docker --version')
    except Exception as e:
        invoke_target('apt update')
        invoke_target('apt', 'install',
            'apt-transport-https',
            'ca-certificates',
            'curl',
            'gnupg-agent',
            'software-properties-common',
        )
        invoke_target('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -')
        invoke_target('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
        invoke_target('apt update')
        invoke_target('apt install docker-ce docker-ce-cli containerd.io')
        invoke_target('curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
        invoke_target('chmod +x /usr/local/bin/docker-compose')
    invoke_target(f'docker login -u xmatik -p {DOCKER_REGISTRY_PW} {DOCKER_REGISTRY}')
    invoke_target(f'docker pull {DOCKER_TAG}')
    service_group = args.service
    if service_group == 'all': service_group = ''
    invoke_target(' '.join([
        f'POSTGRES_DATA_PATH={POSTGRES_DATA_PATH}',
        f'DOCKER_TAG={DOCKER_TAG}',
        f'ENV_PATH={ENV_PATH}',
        f'STATIC_PATH={STATIC_PATH}',
        f'docker-compose -f {{{project_name}}}/docker-compose.yml up -d {service_group}',
    ]))
    if not args.deploy_skip_migrate:
        invoke_target(f'docker exec {{{project_name}}}-main npm run sequelize-cli db:migrate')
    invoke_target('docker system prune --force')

#----- ops -----#
if args.control_set:
    name, value = args.control_set.split(':')
    if value != '0':
        res = auth().post(f'{ORIGIN}/admin/control/{name}', json={'value': value})
    else:
        res = auth().post(f'{ORIGIN}/admin/control/{name}')
    print(res, res.text)

if args.control_unset:
    name = args.control_unset
    res = auth().post(f'{ORIGIN}/admin/control/{name}')
    print(res, res.text)

#----- probing -----#
if args.signup:
    creds_guard()
    res = requests.post(f'{ORIGIN}/auth/signup', json={
        'email': args.email,
        'password': os.environ['{{{project_name.upper().replace('-', '_')}}}_PASSWORD'],
    })
    print(res, res.text)
