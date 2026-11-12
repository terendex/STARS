#!/bin/bash
# Giausar (demo, Easy): a Python program with its password in plain sight.
# Reading the code finds it. The flag is XORed with the password, so it can't
# be read straight out of the file.
set -euo pipefail

user=giausar
FLAG='STARS{g14us4r_l0ck_1n_pl41n_s1ght}'
PASSWORD='twisting-tail'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:draco" | chpasswd
home="/home/$user"
mkdir -p "$home"

python3 - "$PASSWORD" "$FLAG" "$home/giausar.py" <<'EOF'
import pathlib
import sys

password, flag, target = sys.argv[1:]
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
source = pathlib.Path("giausar.py").read_text()
source = source.replace("@PASSWORD@", password).replace("@LOCKED@", locked)
pathlib.Path(target).write_text(source)
EOF

# Fail the build unless the password unlocks the flag and the file doesn't show it.
printf '%s\n' "$PASSWORD" | python3 "$home/giausar.py" | grep -qF "$FLAG"
if grep -qF STARS "$home/giausar.py"; then echo "giausar.py shows its flag" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/giausar.py"
