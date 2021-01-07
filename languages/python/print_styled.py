import re

def print_styled(string, end=None):
    def replace(match):
        if match.group(2) == '/': return match.group()
        if match.group(1) == '/': return '\x1b[0m'
        split = match.group(2).split('-')
        while len(split) < 2: split.append('none')
        color = split[0]
        background = split[1]
        decorations = split[2:]
        if color.startswith('#'):
            color = f'\x1b[38;5;{color[1:]}m'
        else: color = {
            'black': '\x1b[30m',
            'red': '\x1b[31m',
            'green': '\x1b[32m',
            'yellow': '\x1b[33m',
            'blue': '\x1b[34m',
            'magenta': '\x1b[35m',
            'cyan': '\x1b[36m',
            'white': '\x1b[37m',
            'lightblack': '\x1b[30;1m',
            'lightred': '\x1b[31;1m',
            'lightyellow': '\x1b[33;1m',
            'lightgreen': '\x1b[32;1m',
            'lightblue': '\x1b[34;1m',
            'lightmagenta': '\x1b[35;1m',
            'lightcyan': '\x1b[36;1m',
            'lightwhite': '\x1b[37;1m',
            'none': '',
        }[color]
        if background.startswith('#'):
            background = f'\x1b[48;5;{background[1:]}m'
        else: background = {
            'black': '\x1b[40m',
            'red': '\x1b[41m',
            'green': '\x1b[42m',
            'yellow': '\x1b[43m',
            'blue': '\x1b[44m',
            'magenta': '\x1b[45m',
            'cyan': '\x1b[46m',
            'white': '\x1b[47m',
            'lightblack': '\x1b[40;1m',
            'lightred': '\x1b[41;1m',
            'lightyellow': '\x1b[43;1m',
            'lightgreen': '\x1b[42;1m',
            'lightblue': '\x1b[44;1m',
            'lightmagenta': '\x1b[45;1m',
            'lightcyan': '\x1b[46;1m',
            'lightwhite': '\x1b[47;1m',
            'none': '',
        }[background]
        decorations = ''.join([
            {
                'bold': '\x1b[1m',
                'underlined': '\x1b[4m',
                'reversed': '\x1b[7m',
                'none': '',
            }[i]
            for i in decorations
        ])
        return color + background + decorations
    print(re.sub('<(/?)(.*?)>', replace, string) + '\x1b[0m', end=end)
    return re.sub('<(/?)(.*?)>', '', string)

for decorations in ['none', 'underlined', 'underlined-bold', 'reversed']:
    for color in ['red', 'green', 'blue', 'lightyellow', 'lightcyan', 'lightmagenta', '#210']:
        for background in ['none', 'lightblack', 'blue', '#52']:
            print_styled(f'<{color}-{background}-{decorations}> hi </>', end='')
        print()
    print()
