#!/bin/bash
# Alifa: the flag isn't in a file. sshd sets it as an environment variable when
# this account logs in, among a few ordinary-looking ones, so players learn env.
set -euo pipefail

user=alifa
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:inherited" | chpasswd

home="/home/$user"
mkdir -p "$home"
cat > "$home/notes.txt" <<'TEXT'
Alifa's signal isn't stored in any file on this server.
It's handed to you the moment you log in.
TEXT

FLAG='STARS{4l1f4_l1v3s_1n_th3_3nv1r0nm3nt}'
# A Match block, so only this account gets these. Match blocks run to the end of
# the file, which is why every level adds its own at the end.
cat >> /etc/ssh/sshd_config <<CONF

Match User $user
    SetEnv OBSERVATORY=ursa-minor DOME_STATE=open CAMERA=allsky-2 ALIFA_SIGNAL=$FLAG SKY_QUALITY=21.4
CONF

# Fail the build if the setting didn't land.
grep -qF "ALIFA_SIGNAL=$FLAG" /etc/ssh/sshd_config

chown -R "root:$user" "$home"
chmod 750 "$home"
chmod 640 "$home/notes.txt"
