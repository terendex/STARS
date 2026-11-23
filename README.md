# STARS CTF

A Jeopardy-style CTF hosted from one PC. Each category is a constellation and each challenge is one of its stars. Players join over the same Wi-Fi. Only the admin can see the scoreboard.

Made by Axel Jonas C. Tangalin. This folder also holds a separate competition CTF, [SITS Capture The Flag Competition 2026](#sits-capture-the-flag-competition-2026).

**This folder contains every flag and both answer sheets. Keep it in a private repo, and share it only with organizers.** See [Giving STARS to someone else](#giving-stars-to-someone-else).

## What players use

| What | Address |
|---|---|
| Login, challenges, flag submission, downloads | `http://<host>:8000` |
| Ursa Minor (Linux), shared SSH box | `ssh <star>@<host> -p 2220` |
| Orion (Web) | `http://<host>:8081` to `8090` |
| Gemini (Crypto), Lyra (Forensics) | Files downloaded from CTFd |
| Scorpius (Pwn) | `ssh <star>@<host> -p 2220`, or `nc <host> 9002` to `9006` |
| Antares (Pwn, Hard) | `nc <host> 9001` |
| Draco (Reversing), its own SSH box | `ssh <star>@<host> -p 2222`, password `draco` |
| The mission clock, for the projector | `http://localhost:8001/timer`, on the CTF PC only |

Every category has 5 Easy, 4 Medium and 1 Hard challenge, except Scorpius, which has 3 Easy, 2 Medium and 1 Hard: 56 challenges in all. The real CTF is called **2nd Star**: the second orientation's challenges, with every flag changed from the first. The first orientation's 36 are kept as [STARS Classic](#stars-classic). Draco's SSH box has `strings`, `ltrace`, `gdb`, `objdump` and `python3` installed, so players don't need to install anything for it. Every hint costs points: the first one on a challenge is 5 on Easy and Medium and 10 on Hard. CTFd won't sell a hint that costs more than a team's current score, so a team on 0 points has to solve something first. Easy and Medium descriptions also end with a line listing the commands or tools that help, as OverTheWire does. Hard ones don't.

Players can't sign up or make teams. You create every account and team (see [Registering players](#registering-players)), and players only see the login page and the challenges. They solve a challenge on its port and paste the flag into CTFd, which is what awards the points. Solves and hints belong to the team: once one member solves a challenge, it's marked solved for the others and CTFd won't take it again. Wrong flags are shared too: each team gets 3 per challenge, then CTFd locks that challenge for them. To unlock it, delete one of the team's wrong submissions for it in **Admin Panel > Submissions**, then have them wait a minute before trying again.

| Difficulty | Starts at | Each solve takes off | Never below | Hint costs | Tag |
|---|---|---|---|---|---|
| Easy | 30 | 1 | 15 | 5 each | `★ Easy` |
| Medium | 60 | 3 | 30 | 5, then 5 or 10 | `★★ Medium` |
| Hard | 100 | 5 | 50 | 10, then 10 or 20 | `★★★ Hard` |

Points are dynamic and shared: see [Scoring](#scoring).

The CTFd home page has a short **How to play** guide for beginners, covering flags, submitting, the 3 tries and hints. It also lists each category's walkthrough level: Pherkad, Betelgeuse, Pollux, Sheliak, Shaula and Thuban each start with "Start here" and give every step. The pages live in `scripts/home_page.py`. After editing one, push it to the running CTFd with `docker compose run --rm --entrypoint python ctfcli scripts/home_page.py main`, or `demo` for the demo (see the script for that command).

## First-time setup

On **Windows**, install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and start it. On **Linux**, install Docker Engine with the Compose plugin, and make sure your account can run `docker` without `sudo` (see [Linux](#linux)). Then connect to the network the players will use, and run one command from this folder:

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

```bash
# Linux
bash scripts/setup.sh
```

The first run downloads and builds everything, so it takes a few minutes. It:

1. Makes `.env` with new random passwords.
2. Starts CTFd on this PC only and claims the admin account, because the first person to open CTFd's setup page becomes admin.
3. Sets CTFd up for the event: teams of 3, private registration, and scoreboard and team lists hidden from players. It also uploads the STARS logo from `branding\`.
4. Installs all 56 challenges.
5. Opens the CTF on this PC's network address.
6. Sets up the [demo CTF](#demo-ctf).
7. Turns on [auto-host](#if-your-ip-changes), so the CTF follows your network, and puts **Start STARS** and **Stop STARS** buttons on the desktop (Windows). Nothing starts STARS by itself after that: see [Running it](#running-it).

The admin password goes into `LOGINS.txt`. Running setup again is safe, because anything already set up is skipped. Options: `-Ip <address>` / `--ip <address>` to choose the address yourself, `-NoDemo` / `--no-demo`, and `-NoAutoHost` / `--no-auto-host`.

When it's done, [register the players](#registering-players), then test from a phone or another laptop. Connections from this PC to its own address don't prove other devices can reach it.

## Running it

STARS never starts by itself when the PC starts, and Docker doesn't restart its containers. Use the two buttons on the desktop:

- **Start STARS** starts Docker Desktop if it's closed, then the real CTF on this PC's current network. When it's done, its window shows the players' address and the Mission Clock's.
- **Start SITS CTF** does the same for the [SITS competition](#sits-capture-the-flag-competition-2026).
- **Stop STARS** stops the real CTF, STARS Classic, the demo and SITS. Accounts, scores and the clock are kept.

First-time setup puts the buttons there. To add them again, for example after moving this folder, run `scripts\install-shortcuts.ps1`. STARS Classic and the demo start with their own scripts (see [Demo CTF](#demo-ctf) and [STARS Classic](#stars-classic)).

The same from a terminal, in this folder:

```powershell
scripts\start-stars.ps1   # start (or: docker compose up -d, if the IP hasn't changed)
scripts\stop-stars.ps1    # stop, keeping scores and accounts
docker compose logs -f    # watch logs
```

If something stops during the event, **Start STARS** (or `docker compose up -d`) brings it back. Disable sleep on the PC while it's running. To have the CTF start whenever you sign in instead, run `scripts\install-auto-host.ps1 -StartAtSignIn` (Linux: `bash scripts/install-auto-host.sh --start-at-boot`). The buttons are Windows only; on Linux, use `docker compose up -d` and `docker compose stop`.

## Mission clock

The mission clock decides when players can play. While it's running, players see the challenges and can submit flags. Before it starts, CTFd says the CTF hasn't started yet, and when it reaches zero, flag submissions close. Players never see a countdown, so they aren't put under pressure: their challenges page just opens when you press Start and closes at the end, by itself. Admins can always see and submit everything, so you can test while it's stopped.

Sign in as admin and open **Admin Panel > Mission Clock**. It has:

- **Length:** type hours, minutes and seconds, or pick a preset (30 minutes to 3 hours).
- **Start:** opens the challenges and starts the countdown from the length.
- **Restart:** starts the countdown again from the full length. It doesn't touch scores; to clear those, see [Resetting](#resetting).
- **+5 min / −5 min:** moves the end time while it's running. Adding time after it has ended reopens it.
- **End now:** closes submissions straight away.
- **Standby:** stops the clock and hides the challenges until you press Start. Put the clock in standby before players arrive.
- **No time limit:** turns the clock off, so the CTF is open for as long as you like. That's how it was at the first orientation.
- **Music:** where the music plays: **This page** (the Mission Clock page), **Projector page**, or **Off**. Only the chosen page plays, so it never plays twice.
- **Full screen** (or press F): fills your screen with the countdown, for showing it on the projector.

**On the projector,** either press **Full screen** on the Mission Clock page, or open `http://localhost:8001/timer` on the CTF PC, which shows the same countdown with no controls (`localhost:8001` only works on the CTF PC itself). Both have **Full screen** and the F key.

**Music:** while the clock runs, the chosen page plays the tracks of a Spotify album in a new random order, moving to another random track when one ends, and a new order on every Start or Restart. N or **Skip** skips a track. It pauses when the clock ends or goes back to standby. Browsers only allow sound after a click on the page:

- With **This page**, pressing Start is that click, so the music starts with the clock. Only the browser where you pressed Start plays. If you reload the page while the clock runs, press **Turn on sound**.
- With **Projector page**, click the projector page once when it says so, before or after Start.

It also needs:

- **Internet on the CTF PC.** Without it, the page says so, and the clock still works.
- **`localhost:8001`, for whole songs.** Spotify only plays whole songs on a secure page, and browsers count `http://localhost` as secure but not `http://<host>`. So for whole songs, open the Mission Clock as `http://localhost:8001/admin/stars-timer` (sign in there once) or the projector page as `http://localhost:8001/timer`. On `http://<host>:8000`, the music only plays previews, and the Mission Clock page says so.
- **Spotify signed in, in that browser,** for whole songs. Otherwise Spotify only plays short previews.

The tracks are listed in `ctfd-plugin/assets/playlist.json`. To use another album or playlist, run `python scripts/set-playlist.py <Spotify link>`, then refresh the projector page. It only needs Python, no extra packages.

## First blood and help requests

**First blood** is the first team to solve a challenge. Hidden teams and admins never count, so testing doesn't take one.

- **On the projector page,** each new first blood shows at the top for 8 seconds: the team, and the challenge it solved. Only ones that happen while the page is open are shown, one at a time.
- **Admin Panel > Statistics** has a **First Bloods** table above Player Progression: every challenge solved so far, which team solved it first, the player who did, the time, and how long after the start.

**Help requests:** players press **Ask for help** in the corner of the challenges page. The challenge they have open is chosen for them, and they can say what they've tried. Each team has one request at a time; asking again changes it.

- **Admin Panel > Help Queue** lists the requests, oldest first, with how long each team has waited. **On my way** tells the team someone is coming, and **Done** clears it from their screen. The page checks every 5 seconds, and plays a short sound for each new request once you've clicked anywhere on it.
- The **Help Queue** link in the admin menu shows how many teams are waiting, on every admin page.
- The player sees their place in the queue, then "An organizer is on the way". They can also cancel.
- Finished requests stay listed until you press **Clear finished**. CTFd's own Reset doesn't clear them.

STARS Classic has both too. The demo doesn't.

## Registering players

Players can't register themselves, so make their teams and accounts before the event. Say how many teams you want:

```
docker compose run --rm --entrypoint python ctfcli scripts/make-teams.py 15
```

Teams are named with NATO call signs (Alpha, Bravo, Charlie, and so on), and each gets 3 accounts with random names, like `otter42`. The first player is the captain, and nobody needs an email. No account belongs to anyone in particular, so on the day you can give any team's logins to any group. Running the script again adds more teams after the last call sign.

The passwords go into `LOGINS.txt`, which stays out of git, and aren't printed. Each is two words and a number, like `maple-anvil-318`, so it's easy to type. Give each player a name and its password. Players log in with the name, in any capitals. They're already on their team, so they don't need the team's password.

On Windows, Docker Desktop makes every player reach CTFd from the same address, so CTFd's login limit covers the whole room. Once 10 people have logged in within a few seconds of each other, it answers "Too many requests" until 5 seconds pass with no new login. Have teams log in one at a time, or tell players to wait a few seconds and try again.

To add a team or player by hand, sign in as admin:

1. **Admin Panel > Teams**, then **+** (Create Team). Give each team a name and a password.
2. **Admin Panel > Users**, then **+** (Create User) for each player. Give them a name and a password. You can leave the email empty: `ctfd-plugin\` makes it optional, because no one here needs one.
3. Open each team and use the **Add Team Members** icon to add its 3 players.
4. Hand each player their name and password.

Put every player on a team. A player without one gets stuck on CTFd's "join a team" page after logging in, because team creation is off. To see the scores yourself, open **Admin Panel > Scoreboard**.

## Demo CTF

`demo\` holds a separate small CTF for showing people how STARS works: 2 Easy challenges per category, 12 in all. None of them are in the real event, so it's safe to demo in front of players. Its navbar is purple so you can tell the two apart.

**No login needed.** Anyone who opens the demo is signed in automatically as `demo1` on the **Demo Team**, so everyone who opens it shares that one team. A challenge solved by one person shows as solved for everyone, and wrong flags count against everyone's 3 tries. The scoreboard is hidden, as in the real event. To require logins again, empty `STARS_DEMO_AUTOLOGIN` in `demo\docker-compose.yml` and run `scripts\demo.ps1 start`.

It has its own CTFd, accounts and scores, and runs beside the real CTF on the same IP:

| What | Address |
|---|---|
| Demo CTFd | `http://<host>:8100` |
| Ursa Minor (Linux), and SSH into Scorpius | `ssh <star>@<host> -p 2221` |
| Orion (Web) | `http://<host>:8091` and `8092` |
| Scorpius (Pwn) | `nc <host> 9021` and `9022` |
| Draco (Reversing) | `ssh <star>@<host> -p 2223`, password `draco` |

```powershell
scripts\demo.ps1 start   # start it          (Linux: bash scripts/demo.sh start)
scripts\demo.ps1 stop    # stop it, keeping accounts and scores
scripts\demo.ps1 sync    # after editing a demo challenge.yml
```

To manage the demo, open `http://<host>:8100/login` and sign in as admin. Signing out puts you back on the Demo Team. The admin password is in `demo\LOGINS.txt`, which stays out of git, and the solutions are in `demo\ANSWERS.md`. Signing in to one CTFd doesn't sign you out of the other.

The demo doesn't start when you sign in. If your IP changes while it's running, it moves with the real CTF.

To clear the demo between showings, use **Admin Panel > Config > Reset** in the demo CTFd, and reset submissions only. To unlock one challenge after 3 wrong flags, delete one of the Demo Team's wrong submissions in **Admin Panel > Submissions**. To start over completely, run `docker compose -f demo\docker-compose.yml down -v`, delete `demo\.env`, `demo\.ctf` and `demo\LOGINS.txt`, then run `scripts\demo.ps1 setup` (Linux: `bash scripts/demo.sh setup`). Setup claims the admin account while CTFd is reachable from this PC only.

The demo has no mission clock, and its points don't drop.

## STARS Classic

`classic\` keeps the first orientation's 36 challenges exactly as they were, as their own CTF, for a group that hasn't played them yet. It has the same features as the real CTF: [dynamic scoring](#scoring), its own [mission clock](#mission-clock) with the music, and teams of 3. Its navbar is green, so you can tell it apart from the real CTF (dark) and the demo (purple).

It has its own CTFd, accounts, scores and ports, and runs beside the real CTF on the same IP:

| What | Address |
|---|---|
| Classic CTFd | `http://<host>:8200` |
| Ursa Minor (Linux), and SSH into Scorpius | `ssh <star>@<host> -p 2230` |
| Orion (Web) | `http://<host>:8201` to `8206` |
| Scorpius (Pwn) | `nc <host> 9032` to `9036` (Antares: `9031`) |
| Draco (Reversing) | `ssh <star>@<host> -p 2232`, password `draco` |
| Its mission clock, for the projector | `http://localhost:8002/timer` on the CTF PC, and **Admin Panel > Mission Clock** in Classic's CTFd |

```powershell
scripts\classic.ps1 setup      # first time only   (Linux: bash scripts/classic.sh setup)
scripts\classic.ps1 teams 15   # makes 15 teams of 3; logins go in classic\LOGINS.txt
scripts\classic.ps1 start      # start it
scripts\classic.ps1 stop       # stop it, keeping accounts and scores
scripts\classic.ps1 sync       # after editing a challenge.yml in classic\challenges
```

The admin password and the players' logins are in `classic\LOGINS.txt`, which stays out of git, and the solutions are in `classic\ANSWERS.md`. Signing in to Classic doesn't sign you out of the real CTF or the demo.

Classic doesn't start when you sign in, and first-time setup doesn't set it up, so a fresh install stays small. If your IP changes while it's running, it moves with the real CTF. To clear its scores, use **Admin Panel > Config > Reset** in Classic's CTFd, as in [Resetting](#resetting).

## SITS Capture The Flag Competition 2026

`sits\` is a separate, casual-themed 4-hour competition, made by Axel Jonas C. Tangalin. Its flags look like `FLAG{...}`, and its challenges remix STARS's with new passwords, keys, files and flags, so players who did the orientations still have something to solve. It's aimed at beginners: every challenge was played by following only its description and hints. There are **83 challenges**.

| Category | Challenges | Where |
|---|---|---|
| Linux | 15 (6 Easy, 6 Medium, 3 Hard) | `ssh <account>@<host> -p 2240` |
| Web | 15 | `http://<host>:8301` to `8315` |
| Crypto | 15 | downloads |
| Forensics | 15 | downloads |
| Reversing | 15 | `ssh <account>@<host> -p 2242`, password `reverse` |
| Pwn | 8 (5 Easy, 2 Medium, 1 Hard) | `nc <host> 9041` to `9048`, or SSH gate accounts on 2240 (password `pwnit`) |

The Pwn programs are the 8 from Scorpius, reused unchanged except for their flags, so their own menus and text still mention stars. Each has an SSH gate account on 2240 (password `pwnit`) that drops the player straight into the program, for Windows players without `nc`. Return to Sender needs raw bytes, so it has no gate: players use `nc` from a Linux challenge account, where `printf` builds the bytes.

It has the same features as 2nd Star: [dynamic scoring](#scoring), the [mission clock](#mission-clock) (no countdown for players) with music on the projector, [first blood and help requests](#first-blood-and-help-requests), hidden scores, and teams of 3. Its admin is the same as the real CTF's. CTFd is on `http://<host>:8300`, and the projector page is `http://localhost:8003/timer` on the CTF PC.

```powershell
scripts\sits.ps1 setup      # done already on this PC: the admin and the challenges
scripts\sits.ps1 teams 15   # makes 15 teams of 3; logins go in sits\LOGINS.txt
scripts\sits.ps1 start      # or the Start SITS CTF button
scripts\sits.ps1 stop       # or Stop STARS; keeps accounts and scores
scripts\sits.ps1 sync       # after editing a challenge.yml in sits\challenges
```

On Linux, use `bash scripts/sits.sh` with the same words, and open ports 8300, 8301-8315, 9041-9048, 2240 and 2242 in ufw.

The answer key is `sits\ANSWERS.md`: a step-by-step walkthrough of all 83 challenges, with the outputs a player sees. The Crypto and Forensics downloads are made by `make_files.py` in their folders, which also checks each one can be solved. The SSH and Pwn programs check themselves when their boxes are built. The Pwn programs' C source is in each `sits\challenges\pwn\<star>\dist\`, and their flags in each `src\flag.txt`.

The SSH boxes' host keys are saved in `sits\challenges\linux\linux-box\host-keys\` and `sits\challenges\reversing\rev-box\host-keys\`, as in [Troubleshooting](#troubleshooting).

## If your IP changes

Your IP comes from the router, so it changes when you join another network, and sometimes on the same one. The ports stay the same.

**Automatically:** run `scripts\install-auto-host.ps1` once (first-time setup does it for you). It sets up a task that runs as you, hidden, with no admin rights. When Windows connects to a network, and every 5 minutes, it moves the CTF to your new IP, and updates the addresses in CTFd and `ANSWERS.md`.

It never starts the CTF. A CTF that isn't running stays off, and only its files are updated, so it starts on the right address next time. If Docker Desktop is closed, the task does nothing. Everything it does is logged to `logs\auto-host.log`. To turn it off, run `scripts\install-auto-host.ps1 -Remove`. `-StartAtSignIn` adds a second task that starts Docker Desktop and the CTF when you sign in.

The task follows **any** network this PC joins, so a running CTF opens to everyone on it, including public Wi-Fi. Stop the CTF before you join an untrusted network.

**By hand:** run `scripts\set-host.ps1 -Ip <new IP>`.

**On Linux:** `bash scripts/install-auto-host.sh` adds a cron job for your account that moves the CTF to your new IP within 5 minutes of a network change. `--start-at-boot` adds a second one that starts the CTF at boot. Remove them with `bash scripts/install-auto-host.sh --remove`. By hand, run `bash scripts/set-host.sh <new IP>`.

All of these only change the addresses in CTFd, so they're safe during an event. Students still need the new address, so tell them `http://<new IP>:8000`. To keep the same address at a venue, reserve it for this PC in the router's DHCP settings.

## Adding a challenge

1. Copy `challenges/_template` to `challenges/<constellation> (<skill>)/<star>` and edit `challenge.yml`. Keep the category text identical to other stars in that constellation, such as `Orion (Web)`.
2. For a download-only challenge, put player files in `dist/`. Gemini and Lyra generate theirs with `make_files.py` in the category folder.
3. For a challenge with a port:
   - **Simple web star:** add `<star>.py` to `challenges/orion (web)/web-box`, using `betelgeuse.py` as the pattern, then add a service with `<<: *web`.
   - **Pwn star:** add `dist/<star>.c` and `src/flag.txt` in its folder, then add a service like `shaula` in `docker-compose.yml` with its name as `STAR`. To let players connect with SSH, add it to `ssh-box/levels/scorpius-gates.sh`.
   - **Then, for either:** add a `server` line to `edge/nginx.conf`, widen the matching port range on the `edge` service, and run `docker compose up -d --build`, then `docker compose restart edge`.
4. For another Linux level on the SSH box:
   - Add `challenges/ursa-minor (linux)/ssh-box/levels/<star>.sh`, using `polaris.sh` as the pattern.
   - Run `docker compose up -d --build ssh-box`.
5. For another Draco level:
   - Add a folder `challenges/draco (reversing)/draco-box/levels/<star>/` with the program's source and a `setup.sh`. Use `eltanin` as the pattern for a C program and `rastaban` for a Python one. `setup.sh` creates the player account, builds the program into its home folder, and fails the build if the level can't be solved.
   - Run `docker compose up -d --build draco-box`.
6. Register and install it. Keep the quotes, because the folder names contain spaces:
   ```powershell
   docker compose run --rm ctfcli challenge add "challenges/<constellation> (<skill>)/<star>"
   docker compose run --rm ctfcli challenge install "challenges/<constellation> (<skill>)/<star>"
   ```

After editing a `challenge.yml`, push the change with `docker compose run --rm ctfcli challenge sync`. Sync can reset some things that were changed in the CTFd admin panel, so make challenge edits in the YAML files.

### If you change a flag

Each flag lives in `challenge.yml` and in one other place, and they have to match:

| Star | Other place | Then run |
|---|---|---|
| Ursa Minor, except 11 UMi | `ssh-box/levels/<star>.sh` | `docker compose up -d --build ssh-box` |
| 11 UMi | `ursa-minor (linux)/beacon/message.txt` | `docker compose up -d --build beacon` |
| Rigel | `rigel/app/init_db.py` | `docker compose up -d --build rigel` |
| The other Orion stars, except Alnitak | `web-box/<star>.py` | `docker compose up -d --build <star>` |
| Alnitak | `web-box/init_alnitak_db.py` | `docker compose up -d --build alnitak` |
| All of Gemini | `gemini (crypto)/make_files.py` | `python "challenges/gemini (crypto)/make_files.py"` |
| All of Lyra | `lyra (forensics)/make_files.py` | `python "challenges/lyra (forensics)/make_files.py"` |
| All of Scorpius | `<star>/src/flag.txt` | `docker compose up -d --build <star>` |
| All of Draco | `draco-box/levels/<star>/setup.sh` | `docker compose up -d --build draco-box` |

For Gemini and Lyra, run `ctfcli challenge sync` afterwards to upload the new files. Some Lyra flags are drawn on a picture (Sulafat, Ring Nebula, Kepler-62, M56 and Zeta Lyrae), so they can only use capital letters, `_`, `{` and `}`, the characters in the script's font. Those flags are case-insensitive in their `challenge.yml`, because players read them off the picture. Both scripts check every file they make, and stop with an error if a level can't be solved.

If you change `antares.c`, also re-export the download so it matches the running binary. From `challenges/scorpius (pwn)`, run `docker build --target dist --build-arg STAR=antares --output antares/dist .`

## Scoring

Points drop as more teams solve a challenge, and everyone who solved it shares the lower value. The first team gets the starting value. Each later solve takes `decay` points off that challenge for every team that has it, until it reaches `minimum`. Each `challenge.yml` has the numbers:

```yaml
type: standard
value: 60
extra:
  function: linear
  initial: 60
  decay: 3
  minimum: 30
```

To change them, edit `initial`, `decay` or `minimum` (keep `value` the same as `initial`), then run `docker compose run --rm ctfcli challenge sync`. Keep `type: standard`. In this version of CTFd, the points dropping is built into `standard`, and changing a challenge to `type: dynamic` with sync breaks it. For fixed points, use `decay: 0`.

Admin accounts are hidden, so their solves don't lower anyone's points. CTFd only recalculates a challenge's value when someone solves it or it's synced, so after deleting solves, run sync to put the values back. `ctfcli challenge verify` reports a difference in `extra` for every challenge. That's a limit of this ctfcli version, and it's harmless.

## Resetting

- **Clear scores between runs:** in CTFd, **Admin Panel > Config > Backup** first, to keep a copy of the results. Then **Admin Panel > Config > Reset**, and tick **Submissions** only, which keeps the accounts and teams. Then run `docker compose run --rm ctfcli challenge sync`, so every challenge goes back to its starting value, and put the [mission clock](#mission-clock) in standby.
- **Delete everything, including accounts and challenges:** remove auto-host first (`scripts\install-auto-host.ps1 -Remove`), or it can open CTFd to the network before setup has claimed it. Then run `docker compose down -v`, delete `.env`, `.ctf\config` and `LOGINS.txt`, and run [first-time setup](#first-time-setup) again. Setup turns auto-host back on.

## Replacing the admin token

1. In CTFd, go to **Settings > Access Tokens** and generate a new token.
2. Replace the `access_token` value in `.ctf/config`.
3. Delete the old token on the same page.
4. Check it works with `docker compose run --rm ctfcli challenge sync`.

## Troubleshooting

- **Other devices can't connect:** Check they're on the same network. Guest networks and some routers block devices from reaching each other. Then check the IP with `ipconfig` (Linux: `ip -4 addr`). On Linux, also check the firewall (see [Linux](#linux)).
- **The SSH box is stuck, for example after a fork bomb:** `docker compose restart ssh-box` (or `draco-box` for Draco)
- **`REMOTE HOST IDENTIFICATION HAS CHANGED` when connecting:** The SSH box got new keys, so anyone who connected before sees this. They can clear it with `ssh-keygen -R "[<host>]:2220"`, or `2222` for the Draco box. To stop it happening, see [Keeping the SSH keys](#keeping-the-ssh-keys).
- **A challenge port doesn't respond:** Check `docker compose ps`, then `docker compose logs <service>`. Containers don't restart by themselves, so `docker compose up -d` starts anything that stopped.
- **Players see "2nd Star has not started yet" or "2nd Star has ended":** that's the [mission clock](#mission-clock). Press Start, or **No time limit** to turn it off.

### Keeping the SSH keys

Each SSH box has its own keys, which players' computers remember. Normally, rebuilding a box would make new ones. To avoid that, each box installs the keys in its `host-keys` folder when it's built, if there are any: `challenges/ursa-minor (linux)/ssh-box/host-keys/` and `challenges/draco (reversing)/draco-box/host-keys/`, and the same two folders under `classic\challenges\`. These folders stay out of git, because they're this server's private keys. A copy of STARS on another PC makes its own.

To save a running box's keys into its folder, for example after a fresh install, run this from this folder:

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force "challenges/ursa-minor (linux)/ssh-box/host-keys", "challenges/draco (reversing)/draco-box/host-keys" | Out-Null
foreach ($type in "rsa", "ecdsa", "ed25519") {
    foreach ($file in "ssh_host_${type}_key", "ssh_host_${type}_key.pub") {
        docker compose cp "ssh-box:/etc/ssh/$file" "challenges/ursa-minor (linux)/ssh-box/host-keys/"
        docker compose cp "draco-box:/etc/ssh/$file" "challenges/draco (reversing)/draco-box/host-keys/"
    }
}
```

```bash
# Linux
mkdir -p "challenges/ursa-minor (linux)/ssh-box/host-keys" "challenges/draco (reversing)/draco-box/host-keys"
for file in ssh_host_{rsa,ecdsa,ed25519}_key{,.pub}; do
    docker compose cp "ssh-box:/etc/ssh/$file" "challenges/ursa-minor (linux)/ssh-box/host-keys/"
    docker compose cp "draco-box:/etc/ssh/$file" "challenges/draco (reversing)/draco-box/host-keys/"
done
```

Copy the key files one by one, as here. Copying the whole `/etc/ssh` folder fails on Windows, because it holds a link Windows won't create. For Classic, add `-f classic/docker-compose.yml` after `docker compose`, and put `classic/` in front of each folder.

## Linux

Everything runs the same on Linux. Every Windows script except the desktop buttons has a bash version in `scripts\`: `setup.sh`, `set-host.sh`, `demo.sh`, `classic.sh`, `install-auto-host.sh` and `auto-host.sh`. Run them with `bash scripts/<name>.sh`.

- **Docker without sudo:** the scripts and the cron jobs run as you, so add yourself to the `docker` group with `sudo usermod -aG docker "$USER"`, then log out and back in.
- **Docker at boot:** `sudo systemctl enable --now docker`, if you use `--start-at-boot` so the CTF starts after a reboot.
- **Firewall:** if players can't connect and you use `ufw`, open the ports:
  ```bash
  sudo ufw allow 8000/tcp && sudo ufw allow 2220/tcp && sudo ufw allow 2222/tcp && sudo ufw allow 8081:8090/tcp && sudo ufw allow 9001:9006/tcp
  # The demo CTF:
  sudo ufw allow 8100/tcp && sudo ufw allow 2221/tcp && sudo ufw allow 2223/tcp && sudo ufw allow 8091:8092/tcp && sudo ufw allow 9021:9022/tcp
  # STARS Classic:
  sudo ufw allow 8200/tcp && sudo ufw allow 2230/tcp && sudo ufw allow 2232/tcp && sudo ufw allow 8201:8206/tcp && sudo ufw allow 9031:9036/tcp
  ```
- **Network address:** setup and auto-host use the address of the network card that reaches the internet. On a VPN, pass your Wi-Fi or LAN address with `--ip`.

## Giving STARS to someone else

Use a **private** GitHub repository, because the challenge files and answer sheets contain every flag. Only give access to other organizers.

**What's in git:** all the challenges and their downloads, the Docker setup, the scripts, the logo, and both answer sheets. `.gitattributes` makes git deliver the player downloads byte for byte. Without it, Git for Windows would change some of them, and the two PDFs would break.

**What isn't:** passwords and tokens (`.env`, `.ctf/config`, `LOGINS.txt`, and the same files in `demo\`, `classic\` and `sits\`), the SSH boxes' keys (`host-keys\`) and logs. Setup makes new ones on each PC. Your CTFd's accounts, teams and solves aren't in git either, because they live in Docker on your PC. The other person's setup starts with a fresh, empty CTF.

To put it on GitHub, create an empty **private** repository on github.com, then run this from this folder:

```bash
git init -b main
git add .
git commit -m "STARS CTF"
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

Then add the other organizer under the repository's **Settings > Collaborators**. They download it with `git clone https://github.com/<you>/<repo>.git`, start Docker, and run [first-time setup](#first-time-setup).

## How it's isolated

- Challenge containers sit on an internal Docker network with no route to your PC, your LAN, or the internet. The `edge` proxy is the only thing publishing their ports.
- CTFd, MariaDB and Redis are on a separate network that challenges can't reach.
- Ports are published on the address in `CTF_BIND_IP` only, so they aren't exposed on Radmin VPN or Tailscale.
- Challenge containers have read-only filesystems, limited capabilities, and CPU, memory and process limits.
- As on OverTheWire, players on the SSH box can see each other's processes and anything left world-readable in `/tmp`.

## Credits

STARS (2nd Star, STARS Classic and the demo) and the SITS Capture The Flag Competition 2026 were made by Axel Jonas C. Tangalin.
