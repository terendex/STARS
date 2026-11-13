# STARS demo answer sheet

**Organizers only.** None of these challenges are in the real event, so it's fine to walk through these solutions in front of players during a demo.

CTFd checks flags automatically and they're case-sensitive. The maximum score is 360: 60 per category. Every challenge is ★ Easy and worth 30 points, and every hint costs 5. CTFd won't sell a hint that costs more than the team's current score, so the Demo Team has to solve something before it can buy one.

Nobody needs to log in: everyone who opens the demo plays as `demo1` on the **Demo Team**. Everyone shares that team, so a solve by one person shows as solved for everyone. The admin login is in `LOGINS.txt` in this folder.

The 3-wrong-flags limit is shared too, so 3 wrong guesses from anyone lock that challenge for everyone. To unlock it, delete one of the Demo Team's wrong submissions for it in **Admin Panel > Submissions**, then wait a minute before trying again. To clear everything between showings, use **Admin Panel > Config > Reset** and reset submissions only.

The demo CTFd is at `http://192.168.68.104:8100`.

The commands use `192.168.68.104`. If your IP has changed, use the new one.

## Ursa Minor (Linux)

| Star | Difficulty | Points | Password | Flag |
|---|---|---|---|---|
| Anwar | ★ Easy | 30 | `farkadain` | `STARS{4nw4r_qu0t3s_th3_sp4c3s}` |
| Dingolay | ★ Easy | 30 | `ramajay` | `STARS{d1ng0l4y_n33dl3_1n_th3_l0g}` |

Each star starts the same way: log in, then enter the password from the table when asked. Nothing shows on screen while you type it. Run `exit` before moving on to the next star. I ran both against the live SSH box.

### Anwar

1. Log in: `ssh anwar@192.168.68.104 -p 2221`
2. List the files with `ls`. You'll see `'anwar al farkadain.txt'`. The quotes are `ls` showing you that the name has spaces in it.
3. Try `cat anwar al farkadain.txt`. It fails with three `No such file or directory` errors, one for each word, because `cat` reads the spaces as gaps between three separate file names. This mistake is the point of the challenge, so it's worth showing.
4. Read it with `cat "anwar al farkadain.txt"`. That's the flag.

Two other ways that work: `cat anwar\ al\ farkadain.txt`, or type `cat anw` and press Tab to let the terminal finish the name.

### Dingolay

1. Log in: `ssh dingolay@192.168.68.104 -p 2221`
2. List the files with `ls`. You'll see `sky_survey.log`.
3. See why scrolling won't work with `wc -l sky_survey.log`. It prints `20000`.
4. Search for the flag with `grep "STARS{" sky_survey.log`. It prints one line ending in `note: STARS{...}`. That's the flag.

`grep STARS sky_survey.log` works too. `grep stars sky_survey.log` finds nothing, because `grep` is case-sensitive, which makes a useful "close but wrong" to show players. `grep -i` ignores case.

## Orion (Web)

| Star | Difficulty | Points | Address | Flag |
|---|---|---|---|---|
| Saiph | ★ Easy | 30 | `:8091` | `STARS{s41ph_s3nds_h34d3rs}` |
| Meissa | ★ Easy | 30 | `:8092` | `STARS{m31ss4_3ntry_z3r0}` |

Open each address in a browser. The `:8091` means `http://192.168.68.104:8091`. I checked both against the live sites.

### Saiph

The flag isn't on the page or in its source. The server sends it in a response header.

1. Open `http://192.168.68.104:8091`. It only shows a status message.
2. Press F12 to open the developer tools and go to the **Network** tab.
3. Reload the page (F5), then click the first request in the list, which is the page itself.
4. Under **Headers**, find **Response Headers**. The `X-Archive-Key` header is the flag.

Command-line alternative: `curl -I http://192.168.68.104:8091` prints the headers, including `X-Archive-Key: STARS{...}`. In PowerShell, type `curl.exe`, because plain `curl` there is a different command.

### Meissa

1. Open `http://192.168.68.104:8092`. It lists Entry 1 to Entry 5.
2. Click **Entry 1**. The address becomes `http://192.168.68.104:8092/entry/1`.
3. Change the number at the end to `0`: `http://192.168.68.104:8092/entry/0`. The page shows **Entry 0: Staff only** with `Archive key: STARS{...}`. That's the flag.

Numbers above 5 show "There's no entry with that number", which is a useful "close but wrong" to show players.

## Gemini (Crypto)

| Star | Difficulty | Points | Flag |
|---|---|---|---|
| Propus | ★ Easy | 30 | `STARS{pr0pus_sp34ks_b1n4ry}` |
| Alzirr | ★ Easy | 30 | `STARS{4lz1rr_fl1ps_th3_4lph4b3t}` |

Both are solved from the file CTFd gives the player to download, using [CyberChef](https://gchq.github.io/CyberChef/): paste the file's contents into the **Input** box (top right), drag operations into the **Recipe** column (middle), and read the answer in **Output** (bottom right). The flag is the `STARS{...}` part of the decoded text. I checked both files decode correctly with Python. CyberChef itself hasn't been tried on them yet.

### Propus

1. Open the downloaded `signal.txt` and copy its contents into CyberChef's Input. It's groups of eight 0s and 1s.
2. Drag **From Binary** into the Recipe. The default settings work, line breaks included.
3. The Output reads `PROPUS BEACON. FLAG FOLLOWS: STARS{...}`.

Each group of eight is one character's code. `01010011` is 83, which is `S`.

### Alzirr

1. Copy the contents of `message.txt` into the Input. It starts `TVNRMR IVOZB, XSZMMVO GSIVV.`
2. Drag **Atbash Cipher** into the Recipe.
3. The Output reads `GEMINI RELAY, CHANNEL THREE. ALZIRR SENDS ITS REGARDS. FLAG FOLLOWS: STARS{...}`. Digits and symbols were never changed, so the flag's numbers come out as they should.

Players who know the Caesar cipher often try **ROT13** first. It won't work, because Atbash mirrors the alphabet (A↔Z, B↔Y) instead of shifting it.

## Lyra (Forensics)

| Star | Difficulty | Points | Flag |
|---|---|---|---|
| RR Lyrae | ★ Easy | 30 | `STARS{RR_LYRAE_HIDES_IN_THE_DARK}` |
| Delta Lyrae | ★ Easy | 30 | `STARS{d3lt4_lyr43_m3t4d4t4}` |

Each one starts from the file CTFd gives the player to download. I checked both files hold their flags, but not yet in Paint or a browser's PDF viewer.

### RR Lyrae

The flag is drawn in colour (8, 8, 8), one shade off the pure black (0, 0, 0) sky, so you can't see it on screen.

1. Open `rr_lyrae.png` in Paint (right-click the file, then **Open with > Paint**).
2. Pick a bright colour, choose **Fill** (the paint bucket), and click an empty part of the black sky.
3. The sky fills with your colour, but the letters don't, because they aren't exactly the colour you clicked. Read the flag off the image.

Brightness sliders don't help much here. They lift the sky and the letters by the same amount, so the letters stay just as hard to see. The fill bucket works because it only fills pixels of exactly one colour.

### Delta Lyrae

The flag is in the PDF's metadata, as its Subject. It isn't on the page.

1. Open `delta_lyrae_report.pdf` in Chrome.
2. Open the ⋮ menu at the top right of the PDF viewer and choose **Document properties**.
3. The **Subject** reads `Archive key: STARS{...}`. That's the flag.

In Firefox, **Document Properties** is in the » menu at the top right of the PDF viewer. If your browser's PDF viewer has no such option, use Chrome or Firefox. Command-line alternatives: `pdfinfo delta_lyrae_report.pdf` or `exiftool delta_lyrae_report.pdf`.

Searching the file for `STARS` in Notepad finds nothing, because the metadata is stored as hex. A metadata viewer is the way in.

## Scorpius (Pwn)

| Star | Difficulty | Points | Flag |
|---|---|---|---|
| Fang | ★ Easy | 30 | `STARS{f4ng_3mpty_p4ssc0d3}` |
| Larawag | ★ Easy | 30 | `STARS{l4r4w4g_c0mm4nd_1nj3ct10n}` |

Connect with `ssh <star>@192.168.68.104 -p 2221` and the password `scorpius`. The login drops straight into the program. On a computer that has `nc`, you can instead connect to the matching port: Fang 9021, Larawag 9022. I ran both over SSH and `nc`, and each returned its flag.

### Fang

The passcode is random every time anyone connects, so it can't be guessed. The bug is in the check: `strncmp(guess, passcode, strlen(guess))` only compares as many characters as you typed. Type nothing, and it compares zero characters, which always counts as a match.

1. Connect: `ssh fang@192.168.68.104 -p 2221`, password `scorpius`.
2. At the `Passcode:` prompt, just press Enter.
3. It prints `Access granted.` and the flag.

A wrong passcode prints `Access denied. The passcode has already changed.` A single letter also has a 1 in 26 chance of working, for the same reason, which is a good way to show players that the check is broken.

### Larawag

The greeter puts your name into the command `echo Hello, <name>` and runs it in a shell. A `;` ends one command and starts the next, so a "name" can carry a second command.

1. Connect: `ssh larawag@192.168.68.104 -p 2221`, password `scorpius`.
2. At `Which star should we greet?`, enter `Vega; cat /flag.txt`.
3. It prints `Hello, Vega`, then the flag, then `Clear skies from Larawag.`

`Vega && cat /flag.txt` works the same way. `$(cat /flag.txt)` works too, and prints `Hello, STARS{...}`.

This gives players a real shell inside the Larawag container. It holds only Larawag's own flag, has no network access, and its filesystem is read-only.

## Draco (Reversing)

| Star | Difficulty | Points | Flag |
|---|---|---|---|
| Giausar | ★ Easy | 30 | `STARS{g14us4r_l0ck_1n_pl41n_s1ght}` |
| Grumium | ★ Easy | 30 | `STARS{grum1um_k33ps_1t_1ns1d3}` |

Both are on the demo's Draco SSH box: `ssh <star>@192.168.68.104 -p 2223`, password `draco`. It has `strings`, `ltrace`, `gdb` and `python3` installed, like the real one. I solved both over SSH on the live box.

### Giausar

A Python program with its password in plain sight. It shows that reversing can be as simple as reading the code.

1. Log in: `ssh giausar@192.168.68.104 -p 2223`, password `draco`.
2. `cat giausar.py` shows the check `if guess == "twisting-tail":`.
3. Run `python3 giausar.py` and type `twisting-tail`. It prints `Giausar opens its vault. STARS{...}`.

The flag in the file is XORed with the password, so it can't be read without the password.

### Grumium

The flag is stored in the program as plain text, but the program never prints it.

1. Log in: `ssh grumium@192.168.68.104 -p 2223`, password `draco`.
2. `./grumium` prints three lines and no flag.
3. Run `strings grumium | grep STARS`. It prints the flag.
