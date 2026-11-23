# Making and editing challenges

How to add a challenge to one of the CTFs, change one, or take one out. You don't need to understand everything in this folder to do it: most challenges are a copy of an existing one with the details changed. When in doubt, find a challenge that works like yours and copy it.

- [The short version](#the-short-version)
- [Where things are](#where-things-are)
- [challenge.yml, field by field](#challengeyml-field-by-field)
- [Points and difficulty](#points-and-difficulty)
- [Writing the description and hints](#writing-the-description-and-hints)
- [Making each kind of challenge](#making-each-kind-of-challenge)
- [Putting it in CTFd](#putting-it-in-ctfd)
- [Editing a challenge](#editing-a-challenge)
- [If you change a flag](#if-you-change-a-flag)
- [Hiding or removing a challenge](#hiding-or-removing-a-challenge)
- [The answer sheet](#the-answer-sheet)
- [Testing it](#testing-it)
- [Common mistakes](#common-mistakes)

## The short version

1. Copy [challenge-template/](challenge-template/) into the CTF's `challenges` folder, under the right category, and give the folder the challenge's name.
2. Fill in `challenge.yml`. Make the files players download, or the program or level that runs on a server.
3. Run the checker from the STARS folder: `scripts\check.ps1` (Linux: `bash scripts/check.sh`). Fix every ERROR.
4. Go into the CTF's folder and put the challenge into CTFd:
   ```powershell
   cd sits
   docker compose run --rm ctfcli challenge add "challenges/web/my-challenge"
   docker compose run --rm ctfcli challenge install "challenges/web/my-challenge"
   ```
5. Play it yourself as a player, from another laptop. Then add its walkthrough to the CTF's `ANSWERS.md`.
6. Save your changes to GitHub, so the next organizer gets them (see [start-here.md](start-here.md#7-saving-your-changes)).

Never done this before? Do the practice challenge in [start-here.md](start-here.md#6-your-first-challenge) first.

The rest of this page explains each step. These steps were tested on 2026-11-23 by following this page to add one new challenge to each SITS category on a test copy, then solving each one as a player.

## Where things are

Each CTF is a folder: `2nd-star`, `classic`, `demo` and `sits`. Inside each, every challenge has its own folder with a `challenge.yml`. Challenges that run on a server also have a part in a shared "box" (an SSH server or a web app container).

The STARS CTFs (2nd Star, Classic and the demo) name each category after a constellation and each challenge after one of its stars. SITS uses plain names.

| What | STARS CTFs | SITS |
|---|---|---|
| A challenge | `challenges/<constellation> (<skill>)/<star>/`, like `challenges/orion (web)/bellatrix/` | `challenges/<category>/<name>/`, like `challenges/web/robots-only/` |
| Linux levels (SSH box) | `challenges/ursa-minor (linux)/ssh-box/levels/` | `challenges/linux/linux-box/levels/` |
| Web apps | `challenges/orion (web)/web-box/` | `challenges/web/web-box/` |
| Reversing levels (SSH box) | `challenges/draco (reversing)/draco-box/levels/` | `challenges/reversing/rev-box/levels/` |
| Pwn programs | `challenges/scorpius (pwn)/<star>/` | `challenges/pwn/<name>/` |
| Crypto downloads | made by `challenges/gemini (crypto)/make_files.py` | made by `challenges/crypto/make_files.py` |
| Forensics downloads | made by `challenges/lyra (forensics)/make_files.py` | made by `challenges/forensics/make_files.py` |
| Ports and services | `docker-compose.yml` and `edge/nginx.conf` | the same |
| Answer sheet | `ANSWERS.md` | the same |

The demo has fewer challenges and uses 2nd Star's SSH box and pwn Dockerfiles with its own levels.

Folder names in the STARS CTFs contain spaces, so always put quotes around their paths in commands.

## challenge.yml, field by field

Start from [challenge-template/challenge.yml](challenge-template/challenge.yml). For a real example, open `2nd-star/challenges/orion (web)/bellatrix/challenge.yml`.

| Field | What it is |
|---|---|
| `name` | What players see. It must be different from every other challenge in the CTF, because ctfcli finds challenges in CTFd by name. |
| `author` | Your name. CTFd doesn't show it, but it records who made the challenge. |
| `attribution` | The credit players see under the name, like `Made by Your name`. |
| `category` | Copy it exactly from another challenge in the same category, like `Orion (Web)` or `Web`. A different spelling makes a new category. |
| `type` | Always `standard`. See [Points and difficulty](#points-and-difficulty). |
| `value`, `extra` | The points. See [Points and difficulty](#points-and-difficulty). |
| `attempts` | Wrong flags a team gets before the challenge locks for them. Every challenge uses `3`. |
| `description` | What players read. See [Writing the description and hints](#writing-the-description-and-hints). It's Markdown: `**bold**`, `` `code` ``, numbered lists. |
| `connection_info` | Only for challenges with a port: `http://<ip>:8083`, `ssh polaris@<ip> -p 2220` or `nc <ip> 9002`. Copy it from another challenge in the same CTF and change the port or account. The IP updates by itself whenever the CTF moves. |
| `files` | Only for download challenges: the files players get, usually in `dist/` in the challenge's folder. |
| `flags` | The answer. See below. |
| `tags` | Exactly one difficulty: `"★ Easy"`, `"★★ Medium"` or `"★★★ Hard"`. |
| `hints` | Optional. Each has `content` and a `cost`, which comes off the team's score when they open it. |
| `state` | `visible`, or `hidden` to keep it out of players' sight. |

**Flags.** The STARS CTFs use `STARS{...}`, and SITS uses `FLAG{...}`. Inside the braces, use lowercase letters, numbers and `_`, often with numbers for letters, like `STARS{b3t3lg3us3_r34d_th3_c0mm3nts}`, so players can't guess it. If players read the flag off a picture, make it capital letters and accept any capitals:

```yaml
flags:
  - type: static
    content: "STARS{FIX_THE_MAGIC_BYTES}"
    data: case_insensitive
```

## Points and difficulty

| Difficulty | Starts at | Each solve takes off | Never below | First hint costs |
|---|---|---|---|---|
| Easy | 30 | 1 | 15 | 5 |
| Medium | 60 | 3 | 30 | 5 |
| Hard | 100 | 5 | 50 | 10 |

Points drop as more teams solve a challenge, and everyone who solved it shares the lower value. The first team gets the starting value. Each later solve takes `decay` points off for every team that has it, until it reaches `minimum`. In `challenge.yml`, a Medium looks like this:

```yaml
type: standard
value: 60
extra:
  function: linear
  initial: 60
  decay: 3
  minimum: 30
```

CTFd won't sell a hint that costs more than a team's current score, so a team on 0 points has to solve something first. That's one more reason every category needs an Easy challenge that can be solved without hints.

Keep `value` the same as `initial`, and keep `type: standard`. In this version of CTFd, the dropping is built into `standard`, and `type: dynamic` breaks with sync. For fixed points, leave out `extra` (the demo does this) or use `decay: 0`. If you change these numbers for a whole event, also change the table at the top of `scripts/check-challenges.py`, so the checker agrees.

Look at how many Easy, Medium and Hard challenges a category already has, and keep the mix. 2nd Star has 5 Easy, 4 Medium and 1 Hard in each category, so beginners always have something to start on.

## Writing the description and hints

The players are mostly beginners. A description must tell them clearly what to do, without doing it for them. A good one has three parts:

1. **One or two sentences of story or background.** Keep it short. If it explains the idea behind the challenge, even better.
2. **A bold `**Your goal:**` line** that says what to find and where the flag shows up. If the game calls it something else, like a key or a password, say that's the flag.
3. **On Easy and Medium only,** a last line naming the tools: `**Commands you may need to solve this level:**` for things typed in a terminal, or `**Tools you may need to solve this level:**` for anything else. Name the tools, not the steps. Hard challenges don't have this line.

The Bellatrix example:

```text
Search engines send robots to crawl websites. Most sites keep a file telling those robots
which pages to skip. Anyone can read that file, though, so it also points out the very
pages the owner wanted hidden.

**Your goal:** open Bellatrix Station's website at the address below and find its file for
search engine robots. Then visit the pages that file tells them to skip. One of those pages
still has something on it: the flag.

**Tools you may need to solve this level:** Your browser's address bar
```

Rules:

- **Name the idea, not the answer.** When working out the method is the puzzle, give a term players can search for ("robots file", "ROT13", "file signature"), not the exact command.
- **Say where things are:** "the address below" for web, "(download it below)" for files, "Log in with the command below and the password X" for SSH. For pwn, say which terminal to use (PowerShell on Windows).
- **No unexplained leaps.** Every step needs a clue a beginner could reason from without buying a hint. If the answer to "how would a beginner know that?" is "they wouldn't", put the clue in the description.
- **Hints add something new.** Never sell a hint that repeats the description. A good first hint names the next step, and a second one gets closer to the answer.
- **One "Start here" challenge per category** walks through every step, for people who have never done that kind of challenge. Its description starts with "Start here" and its hints become troubleshooting tips. These are listed on each CTF's home page, in `scripts/home_page.py`.
- **Don't make players install anything.** Players use their own Windows laptops. The reversing boxes already have `strings`, `ltrace`, `gdb`, `objdump` and `python3`. Websites like CyberChef are fine.
- **Plain language.** Short sentences, no jokes that hide the instructions.

## Making each kind of challenge

After any change to a box or a service, rebuild it from the CTF's folder with `docker compose up -d --build <service>`. Every box checks its own levels while it builds, and the build stops with an error if a level can't be solved.

### Download challenges (Crypto, Forensics, anything with a file)

1. Make the file any way you like: a text editor, CyberChef, an image editor, a Python script of your own. Solve it yourself afterwards, the way a player would, to be sure the flag comes back out.
2. Put it in a `dist/` folder inside the challenge's folder, and list it under `files:` in `challenge.yml`:
   ```yaml
   files:
     - dist/message.txt
   ```
3. Keep flags out of the files unless finding them is the puzzle.

That's all a new download challenge needs. You don't have to touch `make_files.py`.

**About `make_files.py`:** the existing Crypto and Forensics files were made by `make_files.py` in the category folder. Each block in it writes one challenge's file and then solves it, and the script stops with an error if a flag doesn't come back out. It only writes the files it makes, so files you add by hand are safe. You only need it to change an existing challenge's file (see [If you change a flag](#if-you-change-a-flag)). You can also add your own challenge to it, by copying a block for a similar challenge. It only needs Python, with no extra packages:

```powershell
python "2nd-star/challenges/gemini (crypto)/make_files.py"
python sits/challenges/forensics/make_files.py
```

No Python on your PC? Run it in Docker instead, from the CTF's folder:

```powershell
cd sits
docker compose run --rm --entrypoint python ctfcli challenges/forensics/make_files.py
```

The script remakes every file in its category, not just yours. With a different Python version than the one that first made them, a few files that contain zip data (like `party_plan.docx` and `holiday.png` in SITS Forensics) come out slightly different. They still work, because the script checked them, but git shows them as changed. If you didn't mean to change them, put them back with `git checkout -- <file>`.

### Web challenges

1. In the web box folder, copy a simple app: `betelgeuse.py` in the STARS CTFs, or `view_source.py` in SITS. Each one is a small Flask app called `app`, and `common.py` has the page layout they share. Put the flag in the new file.
2. In the CTF's `docker-compose.yml`, add a service next to the other web ones:
   ```yaml
   my-challenge:
     <<: *web
     command: ["my_challenge:app"]   # the file name, without .py
   ```
3. In `edge/nginx.conf`, add a line with the next free port:
   ```nginx
   server { listen 8316; set $upstream my-challenge:8000; proxy_pass $upstream; }
   ```
4. In `docker-compose.yml`, widen the `edge` service's port range to include it, for example `8301-8315` → `8301-8316`. Check that no other CTF uses that port (the port table is in the main [README](../README.md)).
5. Rebuild, then restart the proxy so it reads the new line:
   ```powershell
   docker compose up -d --build my-challenge edge
   docker compose restart edge
   ```
6. In `challenge.yml`, set `connection_info: http://<ip>:8316`.

Apps with a database keep their data in a setup script: `init_alnitak_db.py` and `rigel/app/init_db.py` in 2nd Star, and `init_dbs.py` in SITS.

### Linux levels (SSH box)

Each level is one script in the box's `levels/` folder. It runs once, as root, while the box is built. It creates the player's account, sets the password, and fills the home folder. Most levels end with a few checks that stop the build if the level can't be solved, like `ls -a "$home" | grep -q '^\.secret\.txt$'`. Add some to yours: they catch a broken level before players do.

1. Copy a simple level: `polaris.sh` in the STARS CTFs, or `01-welcome.sh` in SITS (SITS numbers its scripts so they run in order).
2. Change the account name, password, files and flag, and the checks at the end.
3. Rebuild: `docker compose up -d --build ssh-box` (SITS: `linux-box`). If it fails, the output says `LEVEL FAILED:` and the script's name.
4. In `challenge.yml`, set `connection_info: ssh <account>@<ip> -p 2220` (SITS: `2240`), and say the password in the description.

### Reversing levels (SSH box)

Each level is a folder in the reversing box's `levels/` with the program's source and a `setup.sh`. `setup.sh` creates the account, compiles the program into the player's home folder, and checks it can be solved.

1. Copy a level that works like yours: in the STARS CTFs, `eltanin` (a C program) or `rastaban` (a Python one). In SITS, copy one of the numbered folders, like `02-compare`.
2. Hide the flag so `strings` doesn't show it, unless that is the lesson. The existing levels XOR it with a key.
3. Rebuild: `docker compose up -d --build draco-box` (SITS: `rev-box`).
4. Log in over SSH and solve it yourself, typing as a player would. Some problems only show up in a real session.

Things that trip people up:

- `ltrace` only sees calls in programs built with `-no-pie -Wl,-z,lazy`.
- For `gdb` levels, compile with `-g`, so `info args`, `set var` and `return` work for beginners.
- A program that asks a question while running under `ltrace` mixes its prompt into ltrace's output. Take the input on the command line instead, like `./eltanin hello`.

### Pwn challenges

Each pwn challenge is a folder with `dist/<name>.c` (the source, which players download) and `src/flag.txt` (the flag, which only the running program can read). The category's `Dockerfile` compiles every program the same way, with the protections off on purpose.

1. Copy a challenge folder like `shaula`, and rename it and the `.c` file.
2. In `docker-compose.yml`, copy the `shaula` service and change the name and `STAR`.
3. In `edge/nginx.conf`, add a `server` line for the next free port, pointing at `<name>:9001`, and widen the `edge` port range.
4. Windows has no `nc`, so most pwn challenges also get an SSH "gate" account that drops players straight into the program. Add it to the list in the gates script: `ssh-box/levels/scorpius-gates.sh` in the STARS CTFs, or `linux-box/levels/16-pwn-gates.sh` in SITS (as `account:program`). Then rebuild that box. A program that needs raw bytes, like Antares, can't have a gate, because a terminal would mangle them.
5. Rebuild, then restart the proxy: `docker compose up -d --build <name> edge`, then `docker compose restart edge`.
6. If players download the compiled program too (like Antares), export it again after every change. From the pwn folder: `docker build --target dist --build-arg STAR=<name> --output <name>/dist .`

### Something else

A challenge that needs its own server, like 11 UMi's beacon in 2nd Star or Knock Knock's doorbell in SITS, gets its own folder with a `Dockerfile` and its own service in `docker-compose.yml` (start it with `<<: *challenge` for the safety limits). Without an `edge` line it can only be reached from the SSH box, which is how those two work.

## Putting it in CTFd

The CTF must be running. From that CTF's folder:

```powershell
cd 2nd-star
docker compose run --rm ctfcli challenge add "challenges/orion (web)/my-star"
docker compose run --rm ctfcli challenge install "challenges/orion (web)/my-star"
```

`add` lists the challenge in the CTF's `.ctf\config` on this PC, and `install` creates it in CTFd. `.ctf\config` isn't in git: on another PC, first-time setup lists every challenge by itself.

## Editing a challenge

To change the text, hints, points or tags, edit `challenge.yml`, run the checker, then sync from the CTF's folder:

```powershell
cd 2nd-star
docker compose run --rm ctfcli challenge sync                                  # every challenge
docker compose run --rm ctfcli challenge sync "challenges/orion (web)/bellatrix"   # just one
```

Classic, the demo and SITS also have a shortcut: `scripts\classic.ps1 sync`, `scripts\demo.ps1 sync`, `scripts\sits.ps1 sync`.

- **Always edit the YAML, not the admin panel.** Sync replaces what's in CTFd with what's in the files, so changes made only in the admin panel are lost.
- **Avoid syncing while teams are playing.** Sync recreates flags, hints and files, so teams can lose hints they already bought. If something must be fixed mid-event, fix just that challenge in the admin panel, then make the same change in the YAML afterwards.

## If you change a flag

Each flag lives in `challenge.yml` and in one other place, and the two have to match. After changing both, run the command, then sync. Teams that already solved the challenge with the old flag keep their solve.

**2nd Star and Classic** (paths inside `challenges/`, commands from the CTF's folder):

| Challenge | Other place | Then run |
|---|---|---|
| Ursa Minor, except 11 UMi | `ursa-minor (linux)/ssh-box/levels/<star>.sh` | `docker compose up -d --build ssh-box` |
| 11 UMi | `ursa-minor (linux)/beacon/message.txt` | `docker compose up -d --build beacon` |
| Rigel | `orion (web)/rigel/app/init_db.py` | `docker compose up -d --build rigel` |
| Alnitak | `orion (web)/web-box/init_alnitak_db.py` | `docker compose up -d --build alnitak` |
| The other Orion stars | `orion (web)/web-box/<star>.py` | `docker compose up -d --build <star>` |
| Gemini | `gemini (crypto)/make_files.py` | `python "challenges/gemini (crypto)/make_files.py"` |
| Lyra | `lyra (forensics)/make_files.py` | `python "challenges/lyra (forensics)/make_files.py"` |
| Scorpius | `scorpius (pwn)/<star>/src/flag.txt` | `docker compose up -d --build <star>` |
| Draco | `draco (reversing)/draco-box/levels/<star>/setup.sh` | `docker compose up -d --build draco-box` |

**SITS:**

| Challenge | Other place | Then run |
|---|---|---|
| Linux, except Knock Knock | `linux/linux-box/levels/<NN-name>.sh` | `docker compose up -d --build linux-box` |
| Knock Knock | `linux/doorbell/message.txt` | `docker compose up -d --build doorbell` |
| Web | `web/web-box/<name>.py`, or `web/web-box/init_dbs.py` for the database ones | `docker compose up -d --build <service>` |
| Crypto | `crypto/make_files.py` | `python challenges/crypto/make_files.py` |
| Forensics | `forensics/make_files.py` | `python challenges/forensics/make_files.py` |
| Reversing | `reversing/rev-box/levels/<NN-name>/setup.sh` | `docker compose up -d --build rev-box` |
| Pwn | `pwn/<name>/src/flag.txt` | `docker compose up -d --build <name>` |

The demo works like 2nd Star, with its own folders under `demo/challenges/`.

Some forensics flags are drawn on a picture by `make_files.py`, so they can only use the characters in its font: capital letters, `_`, `{` and `}`. Those flags are `case_insensitive` in their `challenge.yml`.

## Hiding or removing a challenge

- **Hide it:** set `state: hidden` and sync. Players stop seeing it, and you can bring it back later with `state: visible`.
- **Remove it for good:** delete it in **Admin Panel > Challenges**. Then delete its folder, its line in `.ctf\config`, and its walkthrough in `ANSWERS.md`. If it had a level script, a web app, a service or an `edge` port, remove those too, and rebuild the box.

## The answer sheet

Each CTF has an `ANSWERS.md` with a step-by-step walkthrough of every challenge, for organizers. It's what you read when a team asks for help. Add one for each new challenge, in the same style as the others: what to open, the commands to type, what the player sees, and the flag. The checker warns when a flag isn't in it. The IP in the commands is updated by itself when the CTF moves.

## Testing it

1. Run `scripts\check.ps1`.
2. **Check the flag as admin:** **Admin Panel > Challenges**, click the challenge, then the first icon under its name (**Preview Challenge**). It shows the challenge as players see it. Type the flag and press **Submit**: it says whether it's correct, without recording a solve. Preview works for hidden challenges, and while the clock is in standby.
3. **Play it as a player** on another laptop, solving it using only the description and hints. Wherever you get stuck, a beginner will get stuck too. The admin account can't do this, because it isn't on a team. Use a test team instead: in **Admin Panel > Teams**, create one with **Hidden** ticked, and add a player to it (see [Registering players](running-an-event.md#registering-players)). A hidden team's solves don't lower anyone's points and never take first blood.
4. If you can, ask someone who hasn't seen it to try it.

CTFd allows only about 10 wrong flags a minute for each account, so test wrong answers sparingly.

## Common mistakes

- **`type: dynamic`.** Keep `type: standard`. Dynamic breaks with sync.
- **`value` different from `initial`.** The checker catches this.
- **Category spelled differently** from the others in that category, which makes a new category.
- **Two challenges with the same name.** ctfcli treats them as one.
- **No quotes around paths with spaces**, like `"challenges/orion (web)/bellatrix"`.
- **Editing in the admin panel**, then losing it at the next sync.
- **Forgetting to sync after a Reset**, so points stay at their lowered values.
- **A script saved with Windows line endings.** Git fixes this for you (see `.gitattributes`). If a box fails with `$'\r': command not found`, the file has Windows line endings: save it with LF.
- **Expecting `author` to show.** This ctfcli version never sends it. Players only see `attribution`.
- **Worrying about `ctfcli challenge verify`.** It reports a difference in `extra` for every challenge. That's a limit of this ctfcli version, and it's harmless.
