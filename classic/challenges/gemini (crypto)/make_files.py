"""Regenerates the player downloads for every Gemini star.

Run this after changing a flag, then push the files with ctfcli challenge sync.
"""
import base64
import math
import pathlib
import random
import string
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent


def write(star, name, text):
    path = ROOT / star / "dist" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode())


def wrapped(text):
    return "\n".join(textwrap.wrap(text, 64)) + "\n"


def caesar(text, shift):
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    table = str.maketrans(
        upper + lower,
        upper[shift:] + upper[:shift] + lower[shift:] + lower[:shift],
    )
    return text.translate(table)


def vigenere(text, key):
    letters = []
    position = 0
    for char in text:
        if char in string.ascii_letters:
            base = ord("A") if char.isupper() else ord("a")
            shift = ord(key[position % len(key)]) - ord("A")
            letters.append(chr((ord(char) - base + shift) % 26 + base))
            position += 1
        else:
            letters.append(char)
    return "".join(letters)


SMALL_PRIMES = [n for n in range(2, 2000) if all(n % d for d in range(2, int(n**0.5) + 1))]


def is_probable_prime(n, rng, rounds=40):
    """Miller-Rabin, so this script keeps needing only the standard library."""
    for prime in SMALL_PRIMES:
        if n % prime == 0:
            return n == prime
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def random_prime(bits, rng):
    while True:
        # The top two bits make every product exactly 2 * bits long.
        candidate = rng.getrandbits(bits) | (3 << (bits - 2)) | 1
        if is_probable_prime(candidate, rng):
            return candidate


# Pollux: Base64
FLAG = "STARS{p0llux_sp34ks_b4s3_64}"
message = f"POLLUX RELAY, CHANNEL ONE. FLAG FOLLOWS: {FLAG}"
write("pollux", "message.txt", wrapped(base64.b64encode(message.encode()).decode()))

# Alhena: hex
FLAG = "STARS{4lh3n4_t4lks_1n_h3x}"
message = f"ALHENA RELAY. FLAG FOLLOWS: {FLAG}"
write("alhena", "message.txt", wrapped(message.encode().hex(" ")))

# Castor: Base64 over a Caesar cipher. Players solve it with CyberChef's ROT13
# Brute Force, which only shows the first 100 characters at each shift, so the
# whole message must stay under 100 characters or the flag gets cut off.
FLAG = "STARS{c4st0r_4nd_p0llux_tw1n_s1gn4ls}"
SHIFT = 7
message = f"GEMINI RELAY, CHANNEL TWO. FLAG FOLLOWS: {FLAG}"
assert len(message) < 100
write(
    "castor",
    "transmission.txt",
    wrapped(base64.b64encode(caesar(message, SHIFT).encode()).decode()),
)

# Wasat: Vigenere cipher with an unknown five-letter key. Players recover it from
# the flag format. Keep the letters before the flag a multiple of five, so that
# STARS lines up with the start of the key.
FLAG = "STARS{w4s4t_k3pt_th3_k3y}"
message = f"THE MIDDLE OF THE TWINS KEEPS ITS SECRETS. FLAG FOLLOWS: {FLAG}"
write("wasat", "message.txt", vigenere(message, "TWINS") + "\n")

# Mebsuta: repeating-key XOR, written out as hex. The message opens with the flag,
# so XORing the start with the flag format reveals the key.
FLAG = "STARS{m3bsut4_r3p34t1ng_x0r}"
KEY = b"LEDA"
message = f"{FLAG} END OF MEBSUTA RELAY."
write(
    "mebsuta",
    "message.txt",
    wrapped(bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(message.encode())).hex()),
)

# Tejat: two 2048-bit RSA keys that share a prime, so a gcd breaks them both.
# The seed keeps the download the same every time this script runs.
FLAG = "STARS{t3j4t_tw1ns_sh4r3d_4_pr1m3}"
E = 65537
rng = random.Random("tejat")
SHARED = random_prime(1024, rng)
PRIOR_OTHER = random_prime(1024, rng)
TEJAT_OTHER = random_prime(1024, rng)
N_PRIOR = SHARED * PRIOR_OTHER
N_TEJAT = SHARED * TEJAT_OTHER
message = f"TEJAT RELAY. FLAG FOLLOWS: {FLAG}"
number = int.from_bytes(message.encode(), "big")
assert len({SHARED, PRIOR_OTHER, TEJAT_OTHER}) == 3
assert number < N_TEJAT
assert math.gcd(E, (SHARED - 1) * (TEJAT_OTHER - 1)) == 1
write(
    "tejat",
    "transmission.txt",
    "# Public keys. Tejat Prior publishes n_prior, Tejat publishes n_tejat, and both use e.\n"
    f"n_prior = {N_PRIOR}\n"
    f"n_tejat = {N_TEJAT}\n"
    f"e = {E}\n"
    "\n"
    "# Intercepted message, encrypted for Tejat.\n"
    f"c = {pow(number, E, N_TEJAT)}\n",
)
