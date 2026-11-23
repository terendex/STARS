#!/bin/bash
# Letter by Letter (Easy): a Python program that checks the password one letter
# at a time, by position, in a jumbled order. Players line the letters up by
# their position (Python counts from 0).
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=letters
FLAG='FLAG{c0unt1ng_st4rts_4t_z3r0}'
PASSWORD='basketball'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

python3 - "$PASSWORD" "$FLAG" "$home/letters.py" <<'PY'
import pathlib
import random
import sys

password, flag, target = sys.argv[1:]
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
order = list(range(len(password)))
random.Random("letters").shuffle(order)
assert order != sorted(order) and order != sorted(order, reverse=True)
checks = "\n".join(f'    if guess[{i}] != "{password[i]}":\n        return False' for i in order)
source = pathlib.Path("letters.py").read_text()
source = source.replace("@LOCKED@", locked).replace("@LENGTH@", str(len(password))).replace("@CHECKS@", checks)
pathlib.Path(target).write_text(source)
PY

printf '%s\n' "$PASSWORD" | python3 "$home/letters.py" | grep -qF "$FLAG"
if grep -qF -e 'FLAG{' -e "$PASSWORD" "$home/letters.py"; then echo "letters.py shows its secrets" >&2; exit 1; fi
python3 - "$PASSWORD" "$home/letters.py" <<'PY'
import re
import sys

password, target = sys.argv[1:]
pairs = re.findall(r'guess\[(\d+)\] != "(.)"', open(target).read())
found = dict(pairs)
assert "".join(found[str(i)] for i in range(len(found))) == password
assert "".join(letter for _, letter in pairs) != password
PY

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/letters.py"
