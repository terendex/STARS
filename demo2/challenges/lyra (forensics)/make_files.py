"""Regenerates the player downloads for the 2nd demo's Lyra star, using only the
standard library.

Run this after changing a flag, then push the files with scripts\\demo2.ps1 sync.
It checks the download can be solved, and stops with an error if it can't.
"""
import io
import math
import pathlib
import random
import struct
import wave

ROOT = pathlib.Path(__file__).resolve().parent
RATE = 8000  # samples a second, like a phone line


def write(star, name, data):
    path = ROOT / star / "dist" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


# A phone's keypad tones (DTMF): each key is two tones at once, one for its row
# and one for its column.
ROWS = [697, 770, 852, 941]
COLUMNS = [1209, 1336, 1477, 1633]
KEYPAD = ["123A", "456B", "789C", "*0#D"]
TONES = {key: (ROWS[r], COLUMNS[c]) for r, line in enumerate(KEYPAD) for c, key in enumerate(line)}


def dtmf(keys, on=0.18, off=0.12, seed="lyrids"):
    """A recording of the keys being pressed, with a little line hiss."""
    noise = random.Random(seed)
    samples = [0.0] * int(RATE * 0.6)
    for key in keys:
        low, high = TONES[key]
        for n in range(int(RATE * on)):
            t = n / RATE
            samples.append(0.35 * math.sin(2 * math.pi * low * t) + 0.35 * math.sin(2 * math.pi * high * t))
        samples += [0.0] * int(RATE * off)
    samples += [0.0] * int(RATE * 0.6)
    samples = [s + noise.uniform(-0.02, 0.02) for s in samples]
    out = io.BytesIO()
    with wave.open(out, "wb") as recording:
        recording.setnchannels(1)
        recording.setsampwidth(2)
        recording.setframerate(RATE)
        recording.writeframes(b"".join(struct.pack("<h", int(s * 32767)) for s in samples))
    return out.getvalue()


def goertzel(block, frequency):
    """How strongly one frequency sounds in a block of samples."""
    w = 2 * math.cos(2 * math.pi * frequency / RATE)
    a = b = 0.0
    for sample in block:
        a, b = sample + w * a - b, a
    return a * a + b * b - w * a * b


def decode(data, frame=0.02):
    """Reads the keys back out of a recording, the way a DTMF decoder does."""
    with wave.open(io.BytesIO(data)) as recording:
        raw = recording.readframes(recording.getnframes())
    samples = [s / 32767 for s in struct.unpack(f"<{len(raw) // 2}h", raw)]
    size = int(RATE * frame)
    keys, current = [], None
    for start in range(0, len(samples) - size, size):
        block = samples[start:start + size]
        if sum(s * s for s in block) / size < 0.01:  # silence between presses
            current = None
            continue
        row = max(ROWS, key=lambda f: goertzel(block, f))
        column = max(COLUMNS, key=lambda f: goertzel(block, f))
        key = KEYPAD[ROWS.index(row)][COLUMNS.index(column)]
        if key != current:
            keys.append(key)
            current = key
    return "".join(keys)


# Lyrids: the flag typed as character codes, with * between them.
FLAG = "STARS{lyr1ds_d14l_t0n3s}"
keys = "*".join(str(ord(c)) for c in FLAG)
call = dtmf(keys)
write("lyrids", "call.wav", call)

heard = decode((ROOT / "lyrids" / "dist" / "call.wav").read_bytes())
assert heard == keys, (heard, keys)
assert "".join(chr(int(code)) for code in heard.split("*")) == FLAG
assert b"STARS" not in call

print("2nd demo Lyra downloads written and checked.")
