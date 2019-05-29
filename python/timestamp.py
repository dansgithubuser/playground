def timestamp():
    import datetime
    return '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())

def timestamp(ambiguous=True):
    import datetime
    format = '{:%Y-%m'
    if not ambiguous: format += '-%b'
    format += '-%d %H:%M:%S.%f}'
    return format.format(datetime.datetime.now()).lower()

if __name__ == '__main__': print(timestamp())
