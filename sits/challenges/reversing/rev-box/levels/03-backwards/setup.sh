#!/bin/bash
# Backwards (Easy): a Python program that stores its password backwards.
# Reading the code shows `SECRET[::-1]` reverses it. The flag is XORed with the
# password, so it can't be read straight out of the file.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=backwards
FLAG='FLAG{r34d_1t_b4ckw4rds}'
PASSWORD='chocolatecake'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:reverse" | chpasswd
home="/home/$user"
mkdir -p "$home"

python3 - "$PASSWORD" "$FLAG" "$home/backwards.py" <<'PY'
import pathlib
import sys

password, flag, target = sys.argv[1:]
key = password.encode()
locked = bytes(b ^ key[i % len(key)] for i, b in enumerate(flag.encode())).hex()
source = pathlib.Path("backwards.py").read_text()
pathlib.Path(target).write_text(source.replace("@SECRET@", password[::-1]).replace("@LOCKED@", locked))
PY

printf '%s\n' "$PASSWORD" | python3 "$home/backwards.py" | grep -qF "$FLAG"
stored=$(python3 -c 'import sys; print(sys.argv[1][::-1])' "$PASSWORD")
if printf '%s\n' "$stored" | python3 "$home/backwards.py" | grep -qF 'FLAG{'; then echo "the stored text works as it is" >&2; exit 1; fi
if grep -qF -e 'FLAG{' -e "$PASSWORD" "$home/backwards.py"; then echo "backwards.py shows its secrets" >&2; exit 1; fi

chown -R "root:$user" "$home"
chmod 750 "$home" "$home/backwards.py"
