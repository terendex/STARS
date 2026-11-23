#!/bin/bash
# Unscramble (Medium): a Python program that scrambles the password in three
# steps (reverse, shift 3 letters, Base64). Players undo them in the opposite
# order, for example with CyberChef: From Base64, ROT13 by 23, Reverse.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=unscramble
FLAG='FLAG{und0n3_1n_r3v3rs3_0rd3r}'
PASSWORD='rainbowsprinkles'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

python3 - "$PASSWORD" "$FLAG" "$home/unscramble.py" <<'PY'
import pathlib
import sys

password, flag, target = sys.argv[1:]
source = pathlib.Path("unscramble.py").read_text()
helpers = source.split("guess = input")[0]
namespace = {}
exec(helpers.replace("@SCRAMBLED@", "").replace("@LOCKED@", ""), namespace)
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
source = source.replace("@SCRAMBLED@", namespace["scramble"](password)).replace("@LOCKED@", locked)
pathlib.Path(target).write_text(source)
PY

printf '%s\n' "$PASSWORD" | python3 "$home/unscramble.py" | grep -qF "$FLAG"
if grep -qF -e 'FLAG{' -e "$PASSWORD" "$home/unscramble.py"; then echo "unscramble.py shows its secrets" >&2; exit 1; fi
python3 - "$PASSWORD" "$home/unscramble.py" <<'PY'
import base64
import re
import sys

password, target = sys.argv[1:]
stored = re.search(r'SCRAMBLED = "([^"]+)"', open(target).read()).group(1)
abc = "abcdefghijklmnopqrstuvwxyz"
letters = base64.b64decode(stored).decode()
assert "".join(abc[(abc.index(c) + 23) % 26] for c in letters)[::-1] == password
PY

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/unscramble.py"
