import asyncio
import datetime

class ClockTranslator(asyncio.SubprocessProtocol):
    def pipe_data_received(self, fd, data):
        if fd == 1:  # stdout
            print(datetime.datetime.fromtimestamp(float(data)).isoformat())

loop = asyncio.get_event_loop()
p = loop.subprocess_exec(ClockTranslator, 'python3', '-u', 'clock.py')
loop.run_until_complete(p)
loop.run_forever()
