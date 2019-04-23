import argparse
import json
import pprint
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--trello-json-export-file', '-f', default='trello.json')
parser.add_argument('--info-under-key', '-i')
parser.add_argument('--value-under-key', '-v')
parser.add_argument('--card-history', '-c', action='store_true')
args = parser.parse_args()
if len(sys.argv) == 1: parser.print_help()

def descend(x, k):
    if k == '.': return x
    for i in k.split('.'):
        if type(x) == list: i = int(i)
        x = x[i]
    return x

with open(args.trello_json_export_file) as f: exported = json.loads(f.read())

if args.info_under_key != None:
    x = descend(exported, args.info_under_key)
    if type(x) == list:
        print('0..{}'.format(len(x)))
    elif type(x) == dict:
        pprint.pprint(x.keys())
    else:
        print(type(x))

if args.value_under_key != None:
    x = descend(exported, args.value_under_key)
    pprint.pprint(x)

if args.card_history:
    class CardHistory:
        def __init__(self, action):
            self.name = action['data']['card']['name']
            self.history = [(action['date'], action['data']['list']['name'])]
    
        def update(self, action):
            self.history.append((action['date'], action['data']['listAfter']['name']))
    
    cards = {}
    
    for action in reversed(exported['actions']):
        if action['type'] == 'createCard':
            cards[action['data']['card']['id']] = CardHistory(action)
        elif action['type'] == 'updateCard' and 'listAfter' in action['data']:
            cards[action['data']['card']['id']].update(action)
    
    for k, v in cards.items():
        print(v.name)
        for i in v.history:
            print('\t', i)
