"""Regenerates the player downloads for the demo's Gemini stars.

Run this after changing a flag, then push the files with scripts\\demo.ps1 sync.
"""
import pathlib
import string
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent


def write(star, name, text):
    path = ROOT / star / "dist" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode())


def atbash(text):
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    return text.translate(str.maketrans(upper + lower, upper[::-1] + lower[::-1]))


# Propus: binary, one character per group of eight digits, eight groups a line
FLAG = "STARS{pr0pus_sp34ks_b1n4ry}"
message = f"PROPUS BEACON. FLAG FOLLOWS: {FLAG}"
groups = [f"{byte:08b}" for byte in message.encode()]
lines = [" ".join(groups[i : i + 8]) for i in range(0, len(groups), 8)]
write("propus", "signal.txt", "\n".join(lines) + "\n")

# Alzirr: Atbash, which flips the alphabet and leaves digits and symbols alone
FLAG = "STARS{4lz1rr_fl1ps_th3_4lph4b3t}"
message = f"GEMINI RELAY, CHANNEL THREE. ALZIRR SENDS ITS REGARDS. FLAG FOLLOWS: {FLAG}"
write("alzirr", "message.txt", "\n".join(textwrap.wrap(atbash(message), 64)) + "\n")
