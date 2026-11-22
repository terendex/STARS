#!/bin/bash
# Alsafi (Easy): a Python program that checks the password one letter at a time,
# by position, in a jumbled order. Players line the letters up by their index
# (Python counts from 0). The flag is XORed with the password.
set -euo pipefail

user=alsafi
FLAG='STARS{4ls4f1_c0unts_fr0m_z3r0}'
PASSWORD='skywatcher'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

python3 - "$PASSWORD" "$FLAG" "$home/alsafi.py" <<'PY'
import pathlib
import random
import sys

password, flag, target = sys.argv[1:]
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
order = list(range(len(password)))
random.Random("alsafi").shuffle(order)
assert order != sorted(order) and order != sorted(order, reverse=True)
checks = "\n".join(f'    if guess[{i}] != "{password[i]}":\n        return False' for i in order)
source = pathlib.Path("alsafi.py").read_text()
source = source.replace("@LOCKED@", locked).replace("@LENGTH@", str(len(password))).replace("@CHECKS@", checks)
pathlib.Path(target).write_text(source)
PY

# Fail the build unless the password unlocks the flag, a wrong one doesn't, the
# file shows neither, and lining the checks up by position spells the password.
printf '%s\n' "$PASSWORD" | python3 "$home/alsafi.py" | grep -qF "$FLAG"
if printf 'skywatches\n' | python3 "$home/alsafi.py" | grep -qF STARS; then echo "alsafi accepts a wrong password" >&2; exit 1; fi
if grep -qF -e STARS -e "$PASSWORD" "$home/alsafi.py"; then echo "alsafi.py shows its secrets" >&2; exit 1; fi
python3 - "$PASSWORD" "$home/alsafi.py" <<'PY'
import re
import sys

password, target = sys.argv[1:]
found = dict(re.findall(r'guess\[(\d+)\] != "(.)"', open(target).read()))
assert "".join(found[str(i)] for i in range(len(found))) == password
PY

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/alsafi.py"
