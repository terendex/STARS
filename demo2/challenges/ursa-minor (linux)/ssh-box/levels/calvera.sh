#!/bin/bash
# Calvera (Medium): some of this account's commands are fakes. ~/.local/bin comes
# first in its PATH (Debian puts it there for every user that has one), and it
# holds look-alike cat, grep, head and friends. They run the real program, then
# hide anything shaped like a flag. Players have to notice (type cat, echo
# $PATH) and run the real programs by their full paths, like /usr/bin/cat.
# No pipefail: the checks pipe output into grep -q, which can stop the
# writer early, and only grep's answer matters.
set -eu

user=calvera
FLAG='STARS{c4lv3r4_tru5ts_n0_p4th}'

useradd -M -d "/home/$user" -s /bin/bash -G players "$user"
echo "$user:neutronstar" | chpasswd

home="/home/$user"
fakes="$home/.local/bin"
mkdir -p "$fakes"

cat > "$home/report.txt" <<TEXT
Calvera survey report

Object:     Calvera (1RXS J141256.0+792204)
Type:       isolated neutron star
Distance:   unknown, but probably closer than it looks
Brightness: none we can see. It only shows up in X-rays.

Catalogue entry: $FLAG

Next survey: when someone works out what it's hiding.
TEXT

# Login shells read ~/.bash_profile, which reads ~/.bashrc, as on Debian.
echo '[ -f ~/.bashrc ] && . ~/.bashrc' > "$home/.bash_profile"
cat > "$home/.bashrc" <<'TEXT'
# Programs in ~/.local/bin run before the system's own.
export PATH="$HOME/.local/bin:$PATH"
TEXT

# Each fake runs the real program, then hides anything shaped like a flag.
for tool in cat tac nl head tail grep egrep fgrep sed awk sort uniq cut paste fold; do
    real=$(command -v "$tool" || true)
    [ -n "$real" ] || continue
    cat > "$fakes/$tool" <<EOF
#!/bin/bash
"$real" "\$@" | /usr/bin/sed -E 's/STARS\\{[^}]*\\}/[hidden]/g'
EOF
done
# The pagers show the hidden version too.
for pager in less more; do
    real=$(command -v "$pager" || true)
    [ -n "$real" ] || continue
    cat > "$fakes/$pager" <<EOF
#!/bin/bash
/usr/bin/cat "\$@" | /usr/bin/sed -E 's/STARS\\{[^}]*\\}/[hidden]/g' | "$real"
EOF
done

chown -R "root:$user" "$home"
find "$home" -type d -exec chmod 750 {} +
chmod 640 "$home/report.txt" "$home/.bash_profile" "$home/.bashrc"
chmod 750 "$fakes"/*

# Fail the build unless the fakes hide the flag in a login shell, type shows
# where cat really comes from, and the real cat still shows the flag.
as_player() { runuser -l "$user" -s /bin/bash -c "$1" 2>&1; }
as_player 'cat report.txt' | grep -qF '[hidden]'
as_player 'grep Catalogue report.txt' | grep -qF '[hidden]'
if as_player 'cat report.txt; grep STARS report.txt; head report.txt; tail report.txt' | grep -qF 'STARS{'; then
    echo "calvera's fakes don't hide the flag" >&2; exit 1
fi
as_player 'type cat' | grep -qF "$fakes/cat"
as_player '/usr/bin/cat report.txt' | grep -qF "$FLAG"
