#!/usr/bin/env python3

import subprocess
import time

p = subprocess.Popen('gst-launch-1.0 -q -e alsasrc ! vorbisenc ! oggmux ! filesink location=lol.ogg'.split())

for _ in range(30):
    subprocess.run('sync lol.ogg'.split())
    time.sleep(1)

p.kill()
