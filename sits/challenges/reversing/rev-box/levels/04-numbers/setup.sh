#!/bin/bash
# By the Numbers (Easy): a Python program that keeps its password as a list of
# character codes. Players turn them back into letters, with chr() in python3
# or CyberChef's From Decimal.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=numbers
FLAG='FLAG{ch4r_c0d3s_t0_l3tt3rs}'
PASSWORD='movie-night'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

python3 - "$PASSWORD" "$FLAG" "$home/numbers.py" <<'PY'
import pathlib
import sys

password, flag, target = sys.argv[1:]
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
codes = ", ".join(str(ord(c)) for c in password)
source = pathlib.Path("numbers.py").read_text()
pathlib.Path(target).write_text(source.replace("@CODES@", codes).replace("@LOCKED@", locked))
PY

printf '%s\n' "$PASSWORD" | python3 "$home/numbers.py" | grep -qF "$FLAG"
if printf 'wrong\n' | python3 "$home/numbers.py" | grep -qF 'FLAG{'; then echo "numbers.py accepts a wrong password" >&2; exit 1; fi
if grep -qF -e 'FLAG{' -e "$PASSWORD" "$home/numbers.py"; then echo "numbers.py shows its secrets" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/numbers.py"
