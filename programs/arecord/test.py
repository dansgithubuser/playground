import os
import struct
import subprocess
import wave

SAMPLE_RATE = 48000
FREQS = [480, 619, 757, 887]
HI = struct.pack('B', 255)
LO = struct.pack('B', 0)
THRESHOLD = 2e5

def hi_pass(x, width = 200):
    result = []
    s = sum(x[:width])
    n = width
    for i, x_i in enumerate(x):
        if i + width < len(x):
            s += x[i + width]
            n += 1
        if i - width - 1 >= 0:
            s -= x[i - width - 1]
            n -= 1
        result.append(x_i - s / n)
    return result

def acorr(x, freq):
    offset = SAMPLE_RATE // freq
    return sum(i * j for i, j in zip(x, x[offset:])) / len(x)

# create test sound
if not os.path.exists('play.wav'):
    with wave.open('play.wav', 'wb') as test_wav:
        test_wav.setnchannels(1)
        test_wav.setsampwidth(1)
        test_wav.setframerate(SAMPLE_RATE)
        for freq in FREQS:
            half_period = SAMPLE_RATE // (2 * freq)
            test_wav.writeframes((HI * half_period + LO * half_period) * freq)
            test_wav.writeframes(LO * SAMPLE_RATE)

# play and record
if not os.path.exists('rec.wav'):
    subprocess.Popen('aplay play.wav'.split())
    subprocess.run(f'arecord -c 2 -r {SAMPLE_RATE} -f S16_LE -d 8 rec.wav'.split())

# read recording
with wave.open('rec.wav', 'rb') as rec_wav:
    rec_frames = rec_wav.readframes(rec_wav.getnframes())
rec = list(struct.iter_unpack('<2h', rec_frames))

# check for test sound in each channel
for channel in range(2):
    x = [i[channel] for i in rec]
    x = hi_pass(x)
    channel_good = True
    for i, freq in enumerate(FREQS):
        start = 2 * i * SAMPLE_RATE
        mid = start + SAMPLE_RATE
        end = mid + SAMPLE_RATE
        a_hi = acorr(x[start:mid], freq)
        a_lo = acorr(x[mid:end], freq)
        print(f'freq: {freq}, a_hi: {a_hi}, a_lo: {a_lo}, delta: {a_hi - a_lo}')
        if a_hi - a_lo < THRESHOLD:
            channel_good = False
    print(f'channel: {channel}, good: {channel_good}')
