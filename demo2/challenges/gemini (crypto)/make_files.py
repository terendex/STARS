"""Regenerates the player downloads for the 2nd demo's Gemini star.

Run this after changing a flag, then push the files with scripts\\demo2.ps1 sync.
It checks the download can be solved the way a player would, and stops with an
error if it can't.
"""
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parent


def write(star, name, text):
    path = ROOT / star / "dist" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode())


def xor(data, key):
    return bytes(byte ^ key[i % len(key)] for i, byte in enumerate(data))


# Jellyfish: two messages encrypted with the same one-time key. The first one
# was published, so XORing its signal with it gives the key, and the key opens
# the second signal. The key is random but the same on every run, so the files
# only change when the text does.
FLAG = "STARS{tw1n_k3ys_c4nc3l_0ut}"
published = ("JELLYFISH STATION BULLETIN 443. ALL TWIN ARRAYS ARE ONLINE. "
             "THE NEXT SWEEP OF IC 443 STARTS AT 2200 HOURS. OVER AND OUT.")
private = f"Private, for the twins only: the vault phrase is {FLAG}. Burn this."
assert len(private) <= len(published), "the published message must be at least as long as the private one"

key = random.Random("jellyfish").randbytes(len(published))
signal_1 = xor(published.encode(), key)
signal_2 = xor(private.encode(), key)

write("jellyfish", "signals.txt",
      "Jellyfish Station: two signals, sent with the same one-time key.\n"
      "Each signal is written in hex.\n\n"
      f"Signal 1:\n{signal_1.hex()}\n\n"
      f"Signal 2:\n{signal_2.hex()}\n")
write("jellyfish", "newsletter.txt",
      "Jellyfish Station Newsletter, issue 443\n\n"
      "This season's first signal, now that it's no longer secret, word for word:\n\n"
      f"{published}\n")

# Solve it as a player would in CyberChef: Signal 2, From Hex, XOR with Signal 1
# (as hex), then XOR with the published message (as text).
signals = (ROOT / "jellyfish" / "dist" / "signals.txt").read_text().split("\n")
newsletter = (ROOT / "jellyfish" / "dist" / "newsletter.txt").read_text().splitlines()
one = bytes.fromhex(signals[signals.index("Signal 1:") + 1])
two = bytes.fromhex(signals[signals.index("Signal 2:") + 1])
solved = xor(xor(two, one), newsletter[-1].encode()).decode()
assert FLAG in solved, solved
# The other way round works too: recover the key first, then use it.
assert FLAG in xor(two, xor(one, newsletter[-1].encode())).decode()
for name in ("signals.txt", "newsletter.txt"):
    assert "STARS" not in (ROOT / "jellyfish" / "dist" / name).read_text()

print("2nd demo Gemini downloads written and checked.")
