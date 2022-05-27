#!/usr/bin/env python3

#===== imports =====#
import argparse
import os
import re
import secrets
import string
import subprocess

#===== early helpers =====#
def make_password():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))

def git_repo_url():
    try:
        return (
            subprocess
                .run('git remote get-url origin'.split(), capture_output=True)
                .stdout
                .decode('utf-8')
                .strip()
        )
    except:
        return '<git repo URL>'

#===== consts =====#
DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_PROJECT_NAME = os.path.basename(os.getcwd())
DEFAULT_GIT_REPO_URL = git_repo_url()

#===== args =====#
parser = argparse.ArgumentParser(description='Populate the current directory with a generalist express.js starter project.')
parser.add_argument('--project-name',
    default=DEFAULT_PROJECT_NAME,
    help=f'default: {DEFAULT_PROJECT_NAME}; for best results ensure this is in lower-kebab-case',
)
parser.add_argument('--node-image-tag', default='latest', help='default: latest')
parser.add_argument('--git-repo-url', default=DEFAULT_GIT_REPO_URL, help=f'default: {DEFAULT_GIT_REPO_URL}')
parser.add_argument('--postgres-image-tag', default='latest', help='default: latest')
parser.add_argument('--postgres-password', default=make_password(), help='default: random')
parser.add_argument('--postgres-data-path-prod', help=f'default: /root/{DEFAULT_PROJECT_NAME}/postgres-data')
parser.add_argument('--postgres-data-path-stag', help=f'default: /root/{DEFAULT_PROJECT_NAME}/postgres-data')
parser.add_argument('--docker-registry-hostname', default='<docker registry hostname>', help='default: invalid stand-in')
parser.add_argument('--docker-registry-password', default='<docker registry password>', help='default: invalid stand-in')
parser.add_argument('--hostname-prod', default='<hostname prod>', help='default: invalid stand-in')
parser.add_argument('--hostname-stag', default='<hostname stag>', help='default: invalid stand-in')
parser.add_argument('--emailer-email-prod', default='<emailer email prod>', help='default: invalid stand-in')
parser.add_argument('--emailer-email-stag', default='<emailer email stag>', help='default: invalid stand-in')
args = parser.parse_args()

if not args.postgres_data_path_prod:
    args.postgres_data_path_prod = f'/root/{args.project_name}/postgres-data'

if not args.postgres_data_path_stag:
    args.postgres_data_path_stag = f'/root/{args.project_name}/postgres-data'

#===== helpers =====#
def repl(match):
    return eval('args.' + match.group(1))

#===== main =====#
print('I will create a project in the current directory. Arguments:')
for arg in sorted(dir(args)):
    if arg.startswith('_'): continue
    print(f'\t{arg:.<32}: {getattr(args, arg)}')
print('Okay? Enter to continue, ctrl-c to exit.')
input()

templates_path = os.path.join(DIR, 'templates')
for path, dir_names, file_names in os.walk(templates_path):
    template_path = os.path.relpath(path, templates_path)
    for file_name in file_names:
        input_path = os.path.join(path, file_name)
        with open(input_path) as file:
            contents = file.read()
        input_mode = os.stat(input_path).st_mode
        contents = re.sub(r'\{\{\{(.*?)\}\}\}', repl, contents)
        os.makedirs(template_path, exist_ok=True)
        if file_name.startswith('dot.'):
            file_name = file_name[3:]
        output_path = os.path.join(template_path, file_name)
        with open(output_path, 'w') as file:
            file.write(contents)
        os.chmod(output_path, input_mode)
