#!/bin/bash
# Rastaban (Easy): a Python program that stores its password backwards. Reading
# the code shows that `SECRET[::-1]` reverses it. The flag is XORed with the
# password, so it can't be read straight out of the file.
set -euo pipefail

user=rastaban
FLAG='STARS{r4st4b4n_r34d_th3_c0d3}'
PASSWORD='headofthedragon'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

python3 - "$PASSWORD" "$FLAG" "$home/rastaban.py" <<'EOF'
import pathlib
import sys

password, flag, target = sys.argv[1:]
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
source = pathlib.Path("rastaban.py").read_text()
source = source.replace("@SECRET@", password[::-1]).replace("@LOCKED@", locked)
pathlib.Path(target).write_text(source)
EOF

# Fail the build unless the password unlocks the flag and the file doesn't show it.
printf '%s\n' "$PASSWORD" | python3 "$home/rastaban.py" | grep -qF "$FLAG"
if grep -qF -e STARS -e "$PASSWORD" "$home/rastaban.py"; then echo "rastaban.py shows its secrets" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/rastaban.py"
