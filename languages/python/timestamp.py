from datetime import datetime, timezone

def timestamp():
    return datetime.now().astimezone().isoformat(' ', 'seconds')

def timestamp_utc():
    return datetime.now(timezone.utc).isoformat(' ', 'seconds').replace('+00:00', 'Z')

def timestamp_file():
    return datetime.utcnow().isoformat('_', 'seconds').replace(':', '-') + 'Z'

def timestamp_file_non_utc():
    return datetime.now().astimezone().strftime('%Y-%m-%d_%H-%M-%S%z')

def datetime_from_unix_timestamp(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp, timezone.utc)

def utc_from_naive(s):
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)

if __name__ == '__main__': print(timestamp())
