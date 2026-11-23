#!/bin/bash
# Spare Key (Hard): a private SSH key left in this account's home opens another
# account, "caretaker", whose home holds the flag. caretaker can't log in with a
# password, only with that key. ssh only refuses a readable key file that the
# player owns, and this one belongs to root, so ssh -i ~/spare_key works as is.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=sparekey
other=caretaker
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:underthemat" | chpasswd
useradd -M -d "/home/$other" -s /bin/bash -G players "$other"
# A random password nobody knows: caretaker only ever logs in with the key.
echo "$other:$(head -c 24 /dev/urandom | base64)" | chpasswd

home="/home/$user"
mkdir -p "$home" "/home/$other"
ssh-keygen -q -t ed25519 -N '' -C 'spare key for the caretaker' -f "$home/spare_key"
mkdir -p /etc/ssh/keys
cp "$home/spare_key.pub" "/etc/ssh/keys/$other"
# Fail the build unless the key matches the caretaker's authorized key.
cmp -s "$home/spare_key.pub" "/etc/ssh/keys/$other"
rm "$home/spare_key.pub"
cat > "$home/note.txt" <<'TEXT'
Left the spare key here in case I get locked out.
It opens the caretaker's account on this same server.
- the caretaker
TEXT
echo 'FLAG{sp4r3_k3y_und3r_th3_m4t}' > "/home/$other/flag.txt"

cat >> /etc/ssh/sshd_config <<CONF

Match User $other
    PubkeyAuthentication yes
    PasswordAuthentication no
    AuthorizedKeysFile /etc/ssh/keys/%u
CONF

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/spare_key" "$home/note.txt"
chown -R "root:$other" "/home/$other"
chmod 750 "/home/$other"
chmod 640 "/home/$other/flag.txt"
chown root:root "/etc/ssh/keys/$other"
chmod 644 "/etc/ssh/keys/$other"

