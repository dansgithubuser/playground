import datetime

def timestamp():
    return datetime.datetime.now().astimezone().isoformat(' ', 'seconds')

def timestamp_file():
    return datetime.datetime.utcnow().isoformat('_', 'seconds').replace(':', '-')

def timestamp():
    return '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())

def timestamp(ambiguous=True):
    format = '{:%Y-%m'
    if not ambiguous: format += '-%b'
    format += '-%d %H:%M:%S.%f}'
    return format.format(datetime.datetime.now()).lower()

if __name__ == '__main__': print(timestamp())
