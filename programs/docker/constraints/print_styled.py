import re

def print_styled(string):
    def replace(match):
        if match.group(2) == '/': return match.group()
        if match.group(1) == '/': return '\x1b[0m'
        return {
            'red': '\x1b[31m',
            'yellow': '\x1b[33m',
            'green': '\x1b[32m',
            'blue': '\x1b[34m',
        }[match.group(2)]
    print(re.sub('<(/?)(.+?)>', replace, string) + '\x1b[0m')
    return re.sub('<(/?)(.+?)>', '', string)
