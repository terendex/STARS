"""Regenerates the player downloads for every SITS Crypto challenge.

Run this after changing a flag, then push the files with scripts\\sits.ps1 sync.
Every block checks its own download: it decodes what it wrote, the way a player
would, and stops with an error if the flag doesn't come back out, or if an
obvious shortcut would give it away.
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


def write(folder, name, text):
    path = ROOT / folder / "dist" / name
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


def atbash(text):
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    return text.translate(str.maketrans(upper + lower, upper[::-1] + lower[::-1]))


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


MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
    "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
    "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
}


def flag_words(decoded):
    """The flag a player writes from the words after FLAG WORDS FOLLOW."""
    return "FLAG{" + "_".join(decoded.split(" FLAG WORDS FOLLOW ")[1].split()) + "}"


# --- Easy -------------------------------------------------------------------

# Not So Secret: Base64, the "start here".
FLAG = "FLAG{b4s3_64_1s_n0t_s3cr3t}"
message = f"Hi there! If you can read this, you just decoded your first Base64. Here is your flag: {FLAG}"
text = wrapped(base64.b64encode(message.encode()).decode())
write("not-so-secret", "message.txt", text)
assert FLAG in base64.b64decode(text).decode() and "FLAG" not in text

# Thirty-Two: Base32. The description says it uses half as many symbols as
# Base64 (capitals and 2-7), so players work out the name.
FLAG = "FLAG{h4lf_th3_symb0ls_b4s3_32}"
message = f"Not Base64 this time, but close. Here is your flag: {FLAG}"
text = wrapped(base64.b32encode(message.encode()).decode())
write("thirty-two", "message.txt", text)
assert set(text) <= set(string.ascii_uppercase + "234567=\n") and "=" in text
assert FLAG in base64.b32decode(text.replace("\n", "")).decode()

# Hex Marks the Spot: hex, in pairs separated by spaces.
FLAG = "FLAG{h3x_m4rks_th3_sp0t}"
message = f"Ahoy! The treasure map says: {FLAG}"
text = wrapped(message.encode().hex(" "))
write("hex-marks-the-spot", "map.txt", text)
assert FLAG in bytes.fromhex(text.replace("\n", " ")).decode()

# Ones and Zeros: binary, one character per group of eight digits, eight
# groups a line. CyberChef's From Binary reads it with its default settings.
FLAG = "FLAG{0n3s_4nd_z3r0s}"
message = f"Beep. Computer says: {FLAG}"
groups = [f"{byte:08b}" for byte in message.encode()]
text = "\n".join(" ".join(groups[i:i + 8]) for i in range(0, len(groups), 8)) + "\n"
write("ones-and-zeros", "signal.txt", text)
assert bytes(int(g, 2) for g in text.split()).decode() == message

# Beep Boop: Morse code, one word per line, letters separated by spaces (From
# Morse Code's default). Morse has no { } or _, so players write the flag from
# the words, and CTFd ignores capitals.
FLAG = "FLAG{DOTS_AND_DASHES}"
message = "HELLO FROM THE RADIO ROOM FLAG WORDS FOLLOW DOTS AND DASHES"
text = "\n".join(" ".join(MORSE[c] for c in word) for word in message.split()) + "\n"
write("beep-boop", "message.txt", text)
back = {code: letter for letter, code in MORSE.items()}
decoded = " ".join("".join(back[c] for c in line.split()) for line in text.splitlines())
assert decoded == message and flag_words(decoded) == FLAG

# Easy as ABC: A1Z26, each letter as its place in the alphabet. One word per
# line, letters separated by spaces.
FLAG = "FLAG{NUMBERS_TO_LETTERS}"
message = "THIS ONE IS EASY AS ABC FLAG WORDS FOLLOW NUMBERS TO LETTERS"
text = "\n".join(" ".join(str(ord(c) - 64) for c in word) for word in message.split()) + "\n"
write("easy-as-abc", "message.txt", text)
numbers = [int(n) for n in text.split()]
assert max(numbers) <= 26 and min(numbers) >= 1
decoded = " ".join("".join(chr(int(n) + 64) for n in line.split()) for line in text.splitlines())
assert decoded == message and flag_words(decoded) == FLAG

# --- Medium -----------------------------------------------------------------

# Mirror, Mirror: Atbash under Base64.
FLAG = "FLAG{m1rr0r_m1rr0r_0n_th3_w4ll}"
message = f"Mirror, mirror, on the wall, who has the flag after all? You do: {FLAG}"
inner = atbash(message)
text = wrapped(base64.b64encode(inner.encode()).decode())
write("mirror-mirror", "message.txt", text)
once = base64.b64decode(text).decode()
assert once == inner and "FLAG{" not in once and atbash(once) == message

# Shift Work: hex over a Caesar cipher. CyberChef's ROT13 Brute Force only
# shows the first 100 characters at each shift, so the whole message stays
# under 100 characters.
FLAG = "FLAG{sh1ft_w0rk_cl0ck3d_0ut}"
SHIFT = 17
message = f"Night shift report. All quiet. Flag follows: {FLAG}"
assert len(message) < 100
text = wrapped(caesar(message, SHIFT).encode().hex(" "))
write("shift-work", "report.txt", text)
inner = bytes.fromhex(text.replace("\n", " ")).decode()
assert "FLAG" not in inner and caesar(inner, 26 - SHIFT) == message
# Exactly one shift shows FLAG, so ROT13 Brute Force's crib leaves one line.
assert [s for s in range(1, 26) if "FLAG" in caesar(inner, s)] == [26 - SHIFT]

# Family Name: Vigenere with the key SIMPSON (the cartoon family from
# Springfield). The letters before FLAG{ are a multiple of seven, so FLAG lines
# up with the start of the key and the crib trick spells SIMP.
FLAG = "FLAG{f4m1ly_n4m3_unl0cks_1t}"
KEY = "SIMPSON"
message = f"Mmm, donuts. The whole family says hello from Evergreen Terrace. Flag follows: {FLAG}"
before = sum(c.isalpha() for c in message[: message.index(FLAG)])
assert before % len(KEY) == 0, before
text = vigenere(message, KEY)
write("family-name", "message.txt", text + "\n")
assert vigenere(text, KEY, decode=True) == message and "FLAG" not in text
crib = text[text.index("{") - 4: text.index("{")]
assert vigenere(crib, "FLAG", decode=True) == KEY[:4]

# Repeat After Me: repeating-key XOR with TACO, written out as hex. The message
# opens with the flag, so XORing the start with FLAG{ shows the key.
FLAG = "FLAG{t4c0_tu3sd4y_x0r}"
KEY = b"TACO"
message = f"{FLAG} See you next Tuesday."
text = wrapped(xor(message.encode(), KEY).hex())
write("repeat-after-me", "message.txt", text)
raw = bytes.fromhex(text.replace("\n", ""))
assert xor(raw, KEY).decode() == message
assert xor(raw[:5], b"FLAG{") == b"TACOT"

# Letter Swap: a simple substitution cipher, long enough for letter
# frequencies (and quipqiup) to work. Only letters are swapped, no letter
# stands for itself, and the flag is letters only so quipqiup reads it whole.
FLAG = "FLAG{LETTERS_IN_DISGUISE}"
message = (
    "THE SANDWICH IS SAID TO BE NAMED AFTER JOHN MONTAGU, THE FOURTH EARL OF SANDWICH, WHO "
    "LIVED IN ENGLAND IN THE EIGHTEENTH CENTURY. THE STORY GOES THAT HE DID NOT WANT TO LEAVE "
    "HIS CARD GAME TO EAT A PROPER MEAL, SO HE ASKED FOR SOME MEAT TUCKED BETWEEN TWO SLICES OF "
    "BREAD. THAT WAY HE COULD EAT WITH ONE HAND AND KEEP PLAYING WITH THE OTHER. HIS FRIENDS "
    "STARTED TO ORDER THE SAME AS SANDWICH, AND THE NAME STUCK. IN A SIMPLE SUBSTITUTION CIPHER "
    "EVERY LETTER IS ALWAYS REPLACED BY THE SAME OTHER LETTER, SO THE MOST COMMON LETTERS IN THE "
    f"MESSAGE STAND FOR THE MOST COMMON LETTERS IN ENGLISH. THE FLAG FOLLOWS: {FLAG}"
)
rng = random.Random("sits-letter-swap")
while True:
    shuffled = list(string.ascii_uppercase)
    rng.shuffle(shuffled)
    if all(a != b for a, b in zip(string.ascii_uppercase, shuffled)):
        break
table = str.maketrans(string.ascii_uppercase, "".join(shuffled))
text = message.translate(table)
write("letter-swap", "message.txt", wrapped(text))
assert text.translate(str.maketrans("".join(shuffled), string.ascii_uppercase)) == message
assert sum(c.isalpha() for c in message) > 400
assert FLAG in message and "FLAG" not in text

# Common Password: an MD5 hash of a very common password, which online lookup
# tables such as CrackStation already know. The flag is FLAG{password}.
PASSWORD = "sunshine"
FLAG = f"FLAG{{{PASSWORD}}}"
digest = hashlib.md5(PASSWORD.encode()).hexdigest()
write(
    "common-password",
    "leaked.txt",
    "THE COFFEE CLUB - STAFF LOGIN (leaked)\n"
    "\n"
    "username: barista\n"
    f"password (MD5 hash): {digest}\n",
)
assert digest == "0571749e2ac330a7455809c6b0e7af90"

# --- Hard -------------------------------------------------------------------

# Shared Secret: two 2048-bit RSA keys that share a prime, so a gcd breaks them
# both. The seed keeps the download the same every time this script runs.
FLAG = "FLAG{sh4r3d_pr1m3_br0k3_b0th}"
E = 65537
rng = random.Random("sits-shared-secret")
SHARED = random_prime(1024, rng)
ANA_OTHER = random_prime(1024, rng)
BEN_OTHER = random_prime(1024, rng)
N_ANA = SHARED * ANA_OTHER
N_BEN = SHARED * BEN_OTHER
message = f"Hi Ben, it's Ana. Don't tell anyone: {FLAG}"
number = int.from_bytes(message.encode(), "big")
assert len({SHARED, ANA_OTHER, BEN_OTHER}) == 3
assert number < N_BEN
assert math.gcd(E, (SHARED - 1) * (BEN_OTHER - 1)) == 1
text = (
    "# Public keys. Ana publishes n_ana, Ben publishes n_ben, and both use e.\n"
    f"n_ana = {N_ANA}\n"
    f"n_ben = {N_BEN}\n"
    f"e = {E}\n"
    "\n"
    "# A message someone sent to Ben, encrypted with Ben's public key.\n"
    f"c = {pow(number, E, N_BEN)}\n"
)
write("shared-secret", "keys.txt", text)
values = dict(re.findall(r"(\w+)\s*=\s*(\d+)", text))
p = math.gcd(int(values["n_ana"]), int(values["n_ben"]))
q = int(values["n_ben"]) // p
d = pow(E, -1, (p - 1) * (q - 1))
plain = pow(int(values["c"]), d, int(values["n_ben"]))
assert FLAG in plain.to_bytes((plain.bit_length() + 7) // 8, "big").decode()
print(f"Shared Secret: p starts {str(p)[:12]}, q starts {str(q)[:12]}")

# No Key Given: Vigenere with a key nobody gives you (BRUNCH). The text is long
# ordinary English, so an automatic solver can find the key from it.
FLAG = "FLAG{th3_k3y_f0und_1ts3lf}"
KEY = "BRUNCH"
message = (
    "Breakfast is often called the most important meal of the day, although nobody seems to "
    "agree on who first said it. Around the world, people start their mornings in very "
    "different ways. In the Philippines, a plate of garlic fried rice with egg and dried fish "
    "is a favourite. In Japan, many families eat rice, miso soup and grilled fish. In England, "
    "a full breakfast comes with eggs, beans, toast, sausages and grilled tomatoes. In the "
    "United States, a stack of fluffy pancakes covered in butter and syrup is hard to beat. "
    "Whatever you eat, a good breakfast gives you the energy to think clearly, which is "
    "exactly what you need for a long day of puzzles. The flag follows: " + FLAG
)
text = vigenere(message, KEY)
write("no-key-given", "message.txt", wrapped(text))
assert vigenere(text, KEY, decode=True) == message and "FLAG" not in text
assert sum(c.isalpha() for c in message) > 500

# Onion: four layers. From the outside in: hex, XOR with one byte, Base64, and a
# Caesar shift. The Base64 layer ends in ==, so XOR Brute Force with the crib ==
# leaves just the right key. XOR Brute Force and ROT13 Brute Force only look at
# the first 100 characters, so every layer stays under 100.
FLAG = "FLAG{p33l3d_3v3ry_l4y3r}"
XOR_KEY = 0x5A
SHIFT = 6
message = f"You made it to the middle of the onion! Flag: {FLAG}"
assert len(message) % 3 == 1 and len(message) < 100
layer3 = caesar(message, SHIFT)
layer2 = base64.b64encode(layer3.encode())
assert layer2.endswith(b"==") and len(layer2) < 100
layer1 = xor(layer2, bytes([XOR_KEY]))
text = wrapped(layer1.hex(" "))
write("onion", "onion.txt", text)
raw = bytes.fromhex(text.replace("\n", " "))
assert [k for k in range(256) if b"==" in xor(raw, bytes([k]))] == [XOR_KEY]
peeled = base64.b64decode(xor(raw, bytes([XOR_KEY]))).decode()
assert peeled == layer3 and "FLAG" not in peeled
assert [s for s in range(1, 26) if "FLAG" in caesar(peeled, s)] == [26 - SHIFT]

print("SITS Crypto downloads written and checked.")
