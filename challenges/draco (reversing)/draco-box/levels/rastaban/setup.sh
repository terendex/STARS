#!/bin/bash
# Rastaban (Easy): a Python program that keeps its password as a list of
# character codes. Players turn them back into letters, with chr() in python3
# or CyberChef's From Decimal. The flag is XORed with the password, so it can't
# be read straight out of the file.
set -euo pipefail

user=rastaban
FLAG='STARS{r4st4b4n_sp34ks_1n_numb3rs}'
PASSWORD='beta-draconis'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

python3 - "$PASSWORD" "$FLAG" "$home/rastaban.py" <<'PY'
import pathlib
import sys

password, flag, target = sys.argv[1:]
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
codes = ", ".join(str(ord(c)) for c in password)
source = pathlib.Path("rastaban.py").read_text()
source = source.replace("@CODES@", codes).replace("@LOCKED@", locked)
pathlib.Path(target).write_text(source)
PY

# Fail the build unless the password unlocks the flag, a wrong one doesn't, the
# file shows neither, and the codes in the file spell the password.
printf '%s\n' "$PASSWORD" | python3 "$home/rastaban.py" | grep -qF "$FLAG"
if printf 'wrong\n' | python3 "$home/rastaban.py" | grep -qF STARS; then echo "rastaban accepts a wrong password" >&2; exit 1; fi
if grep -qF -e STARS -e "$PASSWORD" "$home/rastaban.py"; then echo "rastaban.py shows its secrets" >&2; exit 1; fi
python3 - "$PASSWORD" "$home/rastaban.py" <<'PY'
import re
import sys

password, target = sys.argv[1:]
codes = re.search(r"CODES = \[([^\]]+)\]", open(target).read()).group(1)
assert "".join(chr(int(n)) for n in codes.split(",")) == password
PY

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/rastaban.py"
