"""Regenerates the player downloads for every Gemini star.

Run this after changing a flag, then push the files with ctfcli challenge sync.
Every star checks its own download: each block decodes what it wrote, the way a
player would, and stops with an error if the flag doesn't come back out.
"""
import base64
import hashlib
import math
import pathlib
import random
import re
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


def vigenere(text, key, decode=False):
    """Shifts letters only, and only letters move the key along, as in CyberChef."""
    letters = []
    position = 0
    for char in text:
        if char in string.ascii_letters:
            base = ord("A") if char.isupper() else ord("a")
            shift = ord(key[position % len(key)].upper()) - ord("A")
            letters.append(chr((ord(char) - base + (-shift if decode else shift)) % 26 + base))
            position += 1
        else:
            letters.append(char)
    return "".join(letters)


def xor(data, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


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
FLAG = "STARS{p0llux_b4s3_64_d3c0d3d}"
message = f"POLLUX RELAY, CHANNEL ONE. GOOD EVENING, NEW CREW. FLAG FOLLOWS: {FLAG}"
text = wrapped(base64.b64encode(message.encode()).decode())
write("pollux", "message.txt", text)
assert FLAG in base64.b64decode(text).decode()

# Alhena: Base32. The description says it uses half as many symbols as Base64
# (capitals and 2-7), so players work out the name.
FLAG = "STARS{4lh3n4_h4lf_th3_symb0ls}"
message = f"ALHENA RELAY. NOT BASE64 THIS TIME. FLAG FOLLOWS: {FLAG}"
text = wrapped(base64.b32encode(message.encode()).decode())
write("alhena", "message.txt", text)
assert set(text) <= set(string.ascii_uppercase + "234567=\n")
assert FLAG in base64.b32decode(text.replace("\n", "")).decode()

# Castor: hex over a Caesar cipher. Players solve it with CyberChef's ROT13
# Brute Force, which only shows the first 100 characters at each shift, so the
# whole message must stay under 100 characters or the flag gets cut off.
FLAG = "STARS{c4st0r_sh1ft3d_by_3l3v3n}"
SHIFT = 11
message = f"GEMINI RELAY, CHANNEL TWO. FLAG FOLLOWS: {FLAG}"
assert len(message) < 100
text = wrapped(caesar(message, SHIFT).encode().hex(" "))
write("castor", "transmission.txt", text)
inner = bytes.fromhex(text.replace("\n", " ")).decode()
assert caesar(inner, 26 - SHIFT) == message and FLAG not in inner

# Mekbuda: Morse code, one word per line, letters separated by spaces. That's
# CyberChef's default for From Morse Code. Morse has no { } or _, so the
# description says how to write the flag, and CTFd ignores capitals.
MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
    "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
    "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
}
FLAG = "STARS{SIGNAL_IN_THE_STATIC}"
message = "MEKBUDA RELAY CHANNEL THREE FLAG WORDS FOLLOW SIGNAL IN THE STATIC"
text = "\n".join(" ".join(MORSE[c] for c in word) for word in message.split()) + "\n"
write("mekbuda", "message.txt", text)
back = {code: letter for letter, code in MORSE.items()}
decoded = [" ".join("".join(back[c] for c in line.split()) for line in text.splitlines())]
words = decoded[0].split(" FLAG WORDS FOLLOW ")[1].split()
assert "STARS{" + "_".join(words) + "}" == FLAG

# Jishui: A1Z26, each letter as its place in the alphabet. One word per line,
# letters separated by spaces, so it works by hand as well as on dcode.
FLAG = "STARS{TWENTY_SIX_STEPS}"
message = "JISHUI RELAY FLAG WORDS FOLLOW TWENTY SIX STEPS"
text = "\n".join(" ".join(str(ord(c) - 64) for c in word) for word in message.split()) + "\n"
write("jishui", "message.txt", text)
numbers = [int(n) for n in text.split()]
assert max(numbers) <= 26 and min(numbers) >= 1
decoded = " ".join("".join(chr(int(n) + 64) for n in line.split()) for line in text.splitlines())
assert "STARS{" + "_".join(decoded.split(" FLAG WORDS FOLLOW ")[1].split()) + "}" == FLAG

# Wasat: Vigenere cipher with the five-letter key HELEN (the twins' sister). The
# letters before the flag are a multiple of five, so that STARS lines up with
# the start of the key and the hint's crib trick spells HELEN.
FLAG = "STARS{w4s4t_s1st3r_kn0ws_th3_k3y}"
KEY = "HELEN"
message = f"THE MIDDLE STAR KEEPS THE FAMILY SECRETS. FLAG FOLLOWS: {FLAG}"
before = sum(c.isalpha() for c in message[: message.index(FLAG)])
assert before % len(KEY) == 0, before
text = vigenere(message, KEY)
write("wasat", "message.txt", text + "\n")
assert vigenere(text, KEY, decode=True) == message
crib = text[text.index("{") - 5: text.index("{")]
assert vigenere(crib, "STARS", decode=True) == KEY

# Mebsuta: repeating-key XOR with ZEUS (Pollux's father), written out as hex. The
# message opens with the flag, so XORing the start with STARS{ shows the key.
FLAG = "STARS{m3bsut4_x0r_tw1c3_1s_n0th1ng}"
KEY = b"ZEUS"
message = f"{FLAG} END OF MEBSUTA RELAY."
text = wrapped(xor(message.encode(), KEY).hex())
write("mebsuta", "message.txt", text)
raw = bytes.fromhex(text.replace("\n", ""))
assert xor(raw, KEY).decode() == message
assert xor(raw[:6], b"STARS{") == b"ZEUSZE"

# Geminga: a simple substitution cipher. Long enough for letter frequencies (and
# quipqiup) to work. Only letters are swapped, and no letter stands for itself.
FLAG = "STARS{g3m1ng4_fr3qu3ncy_4n4lys1s}"
message = (
    "GEMINGA IS A NEUTRON STAR IN THE CONSTELLATION GEMINI. IT IS THE COLLAPSED CORE OF A GIANT "
    "STAR THAT EXPLODED ABOUT THREE HUNDRED THOUSAND YEARS AGO. FOR YEARS ASTRONOMERS COULD SEE IT "
    "IN GAMMA RAYS BUT NOT IN ORDINARY LIGHT, SO THEY NAMED IT GEMINGA, WHICH MEANS IT IS NOT THERE "
    "IN THE DIALECT OF MILAN. IN A SIMPLE SUBSTITUTION CIPHER EVERY LETTER IS ALWAYS REPLACED BY THE "
    "SAME OTHER LETTER, SO THE MOST COMMON LETTERS IN THE MESSAGE STAND FOR THE MOST COMMON LETTERS "
    f"IN ENGLISH. THE FLAG FOLLOWS: {FLAG.upper()}"
)
rng = random.Random("geminga")
while True:
    shuffled = list(string.ascii_uppercase)
    rng.shuffle(shuffled)
    if all(a != b for a, b in zip(string.ascii_uppercase, shuffled)):
        break
table = str.maketrans(string.ascii_uppercase, "".join(shuffled))
text = message.translate(table)
write("geminga", "message.txt", wrapped(text))
assert text.translate(str.maketrans("".join(shuffled), string.ascii_uppercase)) == message
assert sum(c.isalpha() for c in message) > 400
assert FLAG.upper() in message and FLAG.upper() not in text

# Eskimo: an MD5 hash of a very common password, which online lookup tables
# such as CrackStation already know. The flag is STARS{password}.
PASSWORD = "starwars"
FLAG = f"STARS{{{PASSWORD}}}"
digest = hashlib.md5(PASSWORD.encode()).hexdigest()
write(
    "eskimo",
    "vault.txt",
    "ESKIMO NEBULA OBSERVATORY - VAULT LOGIN (leaked)\n"
    "\n"
    "username: keeper\n"
    f"password (MD5 hash): {digest}\n",
)
assert digest == "5badcaf789d3d1d09794d8f021f40f0e"

# Tejat: two 2048-bit RSA keys that share a prime, so a gcd breaks them both.
# The seed keeps the download the same every time this script runs.
FLAG = "STARS{t3j4t_gcd_spl1ts_th3_tw1ns}"
E = 65537
rng = random.Random("tejat-second-orientation")
SHARED = random_prime(1024, rng)
PRIOR_OTHER = random_prime(1024, rng)
TEJAT_OTHER = random_prime(1024, rng)
N_PRIOR = SHARED * PRIOR_OTHER
N_TEJAT = SHARED * TEJAT_OTHER
message = f"TEJAT RELAY, SECOND PASS. FLAG FOLLOWS: {FLAG}"
number = int.from_bytes(message.encode(), "big")
assert len({SHARED, PRIOR_OTHER, TEJAT_OTHER}) == 3
assert number < N_TEJAT
assert math.gcd(E, (SHARED - 1) * (TEJAT_OTHER - 1)) == 1
text = (
    "# Public keys. Tejat Prior publishes n_prior, Tejat publishes n_tejat, and both use e.\n"
    f"n_prior = {N_PRIOR}\n"
    f"n_tejat = {N_TEJAT}\n"
    f"e = {E}\n"
    "\n"
    "# Intercepted message, encrypted for Tejat.\n"
    f"c = {pow(number, E, N_TEJAT)}\n"
)
write("tejat", "transmission.txt", text)
values = dict(re.findall(r"(\w+)\s*=\s*(\d+)", text))
p = math.gcd(int(values["n_prior"]), int(values["n_tejat"]))
q = int(values["n_tejat"]) // p
d = pow(E, -1, (p - 1) * (q - 1))
plain = pow(int(values["c"]), d, int(values["n_tejat"]))
assert FLAG in plain.to_bytes((plain.bit_length() + 7) // 8, "big").decode()
print(f"Tejat: p starts {str(p)[:12]}, q starts {str(q)[:12]}")

print("Gemini downloads written and checked.")
