import subprocess

subprocess.run(['cargo', 'build'], check=True)

names = [
    'alice',
    'bob',
    'charlie',
    'denise',
    'emily',
    'frank',
    'gary',
    'harry',
    'ingrid',
    'jerry',
]

for name in names:
    subprocess.Popen(['target/debug/rusqlite', name])
