#!/bin/bash
# Mixed Up (Medium): a Python program that scrambles the password in three steps
# (shift 5 letters, reverse, hex). Players undo them in the opposite order, for
# example with CyberChef: From Hex, Reverse, ROT13 by 21.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=mixedup
FLAG='FLAG{h3x_r3v3rs3_sh1ft_und0n3}'
PASSWORD='thunderstorm'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

python3 - "$PASSWORD" "$FLAG" "$home/mixedup.py" <<'PY'
import pathlib
import sys

password, flag, target = sys.argv[1:]
source = pathlib.Path("mixedup.py").read_text()
helpers = source.split("guess = input")[0]
namespace = {}
exec(helpers.replace("@SCRAMBLED@", "").replace("@LOCKED@", ""), namespace)
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
source = source.replace("@SCRAMBLED@", namespace["scramble"](password)).replace("@LOCKED@", locked)
pathlib.Path(target).write_text(source)
PY

printf '%s\n' "$PASSWORD" | python3 "$home/mixedup.py" | grep -qF "$FLAG"
if grep -qF -e 'FLAG{' -e "$PASSWORD" "$home/mixedup.py"; then echo "mixedup.py shows its secrets" >&2; exit 1; fi
python3 - "$PASSWORD" "$home/mixedup.py" <<'PY'
import re
import sys

password, target = sys.argv[1:]
stored = re.search(r'SCRAMBLED = "([^"]+)"', open(target).read()).group(1)
abc = "abcdefghijklmnopqrstuvwxyz"
letters = bytes.fromhex(stored).decode()[::-1]
assert "".join(abc[(abc.index(c) + 21) % 26] for c in letters) == password
PY

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/mixedup.py"
