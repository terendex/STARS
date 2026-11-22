#!/bin/bash
# Edasich (Medium): a Python program that scrambles the password in three steps
# (shift 5 letters, reverse, hex). Players undo them in the opposite order,
# for example with CyberChef: From Hex, Reverse, ROT13 by 21.
set -euo pipefail

user=edasich
FLAG='STARS{3d4s1ch_unw0und_th3_c01ls}'
PASSWORD='tailofthedragon'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

# Uses the program's own scramble(), so the stored value always matches it.
python3 - "$PASSWORD" "$FLAG" "$home/edasich.py" <<'EOF'
import pathlib
import sys

password, flag, target = sys.argv[1:]
source = pathlib.Path("edasich.py").read_text()
helpers = source.split("guess = input")[0]
namespace = {}
exec(helpers.replace("@SCRAMBLED@", "").replace("@LOCKED@", ""), namespace)
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
source = source.replace("@SCRAMBLED@", namespace["scramble"](password)).replace("@LOCKED@", locked)
pathlib.Path(target).write_text(source)
EOF

# Fail the build unless the password unlocks the flag, the file doesn't show it,
# and the CyberChef recipe in the answer sheet recovers the password.
printf '%s\n' "$PASSWORD" | python3 "$home/edasich.py" | grep -qF "$FLAG"
if grep -qF -e STARS -e "$PASSWORD" "$home/edasich.py"; then echo "edasich.py shows its secrets" >&2; exit 1; fi
python3 - "$PASSWORD" "$home/edasich.py" <<'EOF'
import re
import sys

password, target = sys.argv[1:]
stored = re.search(r'SCRAMBLED = "([^"]+)"', open(target).read()).group(1)
letters = bytes.fromhex(stored).decode()[::-1]
abc = "abcdefghijklmnopqrstuvwxyz"
undone = "".join(abc[(abc.index(c) + 21) % 26] for c in letters)
assert undone == password, undone
EOF

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/edasich.py"
