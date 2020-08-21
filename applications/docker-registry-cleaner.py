import argparse
import glob
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--container', default='docker-registry')
parser.add_argument('--config', default='/etc/docker/registry/config.yml')
args = parser.parse_args()

v2 = os.path.realpath(__file__)
while not v2.endswith('v2'):
    v2 = os.path.dirname(v2)

repos = os.path.join(v2, 'repositories')

def rm_safe(rev, tag_revs):
    for tag_rev in tag_revs:
        if rev.endswith(os.path.join(*tag_rev)):
            return
    print('removing', rev)
    shutil.rmtree(rev)

for repo in os.listdir(repos):
    print(repo)
    manifests = os.path.join(repos, repo, '_manifests')
    tags_glob = os.path.join(manifests, 'tags', '*')
    tag_links = glob.glob(os.path.join(tags_glob, 'current', 'link'))
    tag_revs = []
    for link in tag_links:
        with open(link) as f:
            rev = f.read().split(':')
            tag_revs.append(rev)
            print(link, rev)
    for rev in glob.glob(os.path.join(tags_glob, 'index', '*', '*')):
        rm_safe(rev, tag_revs)
    for rev in glob.glob(os.path.join(manifests, 'revisions', '*', '*')):
        rm_safe(rev, tag_revs)

subprocess.run([
    'docker', 'exec', args.container,
    'bin/registry', 'garbage-collect', args.config,
])
