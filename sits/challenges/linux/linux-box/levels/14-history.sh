#!/bin/bash
# Undo History (Hard): a git repository of recipes. The flag was committed in a
# secret file, then deleted in the next commit, so it's not in the folder any
# more, but git remembers. git log -p (or git log, then git show) finds it.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=history
useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:undoredo" | chpasswd

home="/home/$user"
repo="$home/recipes"
mkdir -p "$repo"

FLAG='FLAG{g1t_n3v3r_f0rg3ts}'
export GIT_AUTHOR_NAME=Lola GIT_AUTHOR_EMAIL=lola@kitchen.invalid
export GIT_COMMITTER_NAME=Lola GIT_COMMITTER_EMAIL=lola@kitchen.invalid
commit() { GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git -C "$repo" commit -q -m "$2"; }

git -C "$repo" init -q -b main
printf 'Pancakes\n- 1 cup flour\n- 1 egg\n- 1 cup milk\n' > "$repo/pancakes.txt"
git -C "$repo" add pancakes.txt
commit '2026-01-03 09:00 +0800' 'Add pancakes'
printf 'Adobo\n- chicken\n- soy sauce\n- vinegar\n- garlic\n' > "$repo/adobo.txt"
git -C "$repo" add adobo.txt
commit '2026-01-10 18:30 +0800' 'Add adobo'
printf "Grandma's secret sauce\nThe secret ingredient: %s\n" "$FLAG" > "$repo/secret-sauce.txt"
git -C "$repo" add secret-sauce.txt
commit '2026-01-17 20:15 +0800' "Add grandma's secret sauce"
git -C "$repo" rm -q secret-sauce.txt
commit '2026-01-17 20:16 +0800' 'Oops, that one is a family secret. Remove it.'
printf 'Champorado\n- sticky rice\n- cocoa\n- milk\n' > "$repo/champorado.txt"
git -C "$repo" add champorado.txt
commit '2026-01-24 07:45 +0800' 'Add champorado'

chown -R "root:$user" "$home"
find "$home" -type d -exec chmod 750 {} +
find "$home" -type f -exec chmod 640 {} +

# Fail the build unless the flag is gone from the folder, still in the history,
# and the hint's command finds it as a player (read-only, other owner).
if grep -rq FLAG "$repo" --exclude-dir=.git; then echo "the flag is still in the folder" >&2; exit 1; fi
runuser -u "$user" -- git -C "$repo" log -p | grep -qF "$FLAG"
