# STARS CTF

A Jeopardy-style CTF hosted from one PC. Each category is a constellation and each challenge is one of its stars. Players join over the same Wi-Fi. Only the admin can see the scoreboard.

**This folder contains every flag and both answer sheets. Keep it in a private repo, and share it only with organizers.** See [Giving STARS to someone else](#giving-stars-to-someone-else).

## What players use

| What | Address |
|---|---|
| Login, challenges, flag submission, downloads | `http://<host>:8000` |
| Ursa Minor (Linux), shared SSH box | `ssh <star>@<host> -p 2220` |
| Orion (Web) | `http://<host>:8081` to `8086` |
| Gemini (Crypto), Lyra (Forensics) | Files downloaded from CTFd |
| Scorpius (Pwn) | `ssh <star>@<host> -p 2220`, or `nc <host> 9002` to `9006` |
| Antares (Pwn, Hard) | `nc <host> 9001` |
| Draco (Reversing), its own SSH box | `ssh <star>@<host> -p 2222`, password `draco` |

Every category has 3 Easy, 2 Medium and 1 Hard challenge, for 36 challenges and a maximum score of 1860. Draco's SSH box has `strings`, `ltrace`, `gdb` and `python3` installed, so players don't need to install anything for it. Every hint costs points: the first one on a challenge is 5 on Easy and Medium and 10 on Hard. CTFd won't sell a hint that costs more than a team's current score, so a team on 0 points has to solve something first. Easy and Medium descriptions also end with a line listing the commands or tools that help, as OverTheWire does. Hard ones don't.

Players can't sign up or make teams. You create every account and team (see [Registering players](#registering-players)), and players only see the login page and the challenges. They solve a challenge on its port and paste the flag into CTFd, which is what awards the points. Solves and hints belong to the team: once one member solves a challenge, it's marked solved for the others and CTFd won't take it again. Wrong flags are shared too: each team gets 3 per challenge, then CTFd locks that challenge for them. To unlock it, delete one of the team's wrong submissions for it in **Admin Panel > Submissions**, then have them wait a minute before trying again.

| Difficulty | Points | Hint costs | Tag |
|---|---|---|---|
| Easy | 30 | 5 each | `★ Easy` |
| Medium | 60 | 5, then 5 or 10 | `★★ Medium` |
| Hard | 100 | 10, then 10 or 20 | `★★★ Hard` |

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
4. Installs all 30 challenges.
5. Opens the CTF on this PC's network address.
6. Sets up the [demo CTF](#demo-ctf).
7. Turns on [auto-host](#if-your-ip-changes), so the CTF follows your network.

The admin password goes into `LOGINS.txt`. Running setup again is safe, because anything already set up is skipped. Options: `-Ip <address>` / `--ip <address>` to choose the address yourself, `-NoDemo` / `--no-demo`, and `-NoAutoHost` / `--no-auto-host`.

When it's done, [register the players](#registering-players), then test from a phone or another laptop. Connections from this PC to its own address don't prove other devices can reach it.

## Running it

Run these from this folder.

```powershell
docker compose up -d     # start
docker compose stop      # stop, keeping scores and accounts
docker compose logs -f   # watch logs
```

With auto-host installed, the CTF starts when you sign in (Windows) or when the PC boots (Linux). Without it, nothing starts after a reboot, so run `docker compose up -d` before the event. Either way, disable sleep on the PC.

## Registering players

Players can't register themselves, so make their teams and accounts before the event. Give the script the team names, and it makes each team with 3 players named after it (`nebula1`, `nebula2` and `nebula3` for Nebula), with the first as captain:

```
docker compose run --rm --entrypoint python ctfcli scripts/make-teams.py Nebula Comet Quasar Pulsar Nova
```

The passwords go into `LOGINS.txt`, which stays out of git, and aren't printed. Each is two words and a number, like `maple-otter-318`, so it's easy to type. Hand each player their name and password. They're already on their team, so they don't need the team's password. If any name is already taken, the script changes nothing, so it's safe to run again later to add more teams.

On Windows, Docker Desktop makes every player reach CTFd from the same address, so CTFd's login limit covers the whole room. Once 10 people have logged in within a few seconds of each other, it answers "Too many requests" until 5 seconds pass with no new login. Have teams log in one at a time, or tell players to wait a few seconds and try again.

To add a team or player by hand, sign in as admin:

1. **Admin Panel > Teams**, then **+** (Create Team). Give each team a name and a password.
2. **Admin Panel > Users**, then **+** (Create User) for each player. Give them a name, an email (a made-up one is fine) and a password.
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

## If your IP changes

Your IP comes from the router, so it changes when you join another network, and sometimes on the same one. The ports stay the same.

**Automatically:** run `scripts\install-auto-host.ps1` once. It sets up two tasks that run as you, hidden, with no admin rights:

- When you sign in, they start Docker Desktop and the CTF.
- When Windows connects to a network, and every 5 minutes, they move the CTF to your new IP. They also update the addresses in CTFd and `ANSWERS.md`.

A CTF you've stopped with `docker compose stop` stays stopped until you next sign in, and if Docker Desktop is closed, the tasks do nothing. Everything they do is logged to `logs\auto-host.log`. To turn them off, run `scripts\install-auto-host.ps1 -Remove`.

The tasks follow **any** network this PC joins, so the CTF opens to everyone on it, including public Wi-Fi. Stop the CTF or remove the tasks before you join an untrusted network.

**By hand:** run `scripts\set-host.ps1 -Ip <new IP>`.

**On Linux:** `bash scripts/install-auto-host.sh` adds two cron jobs for your account: one starts the CTF at boot, and one moves it to your new IP within 5 minutes of a network change. Remove them with `bash scripts/install-auto-host.sh --remove`. By hand, run `bash scripts/set-host.sh <new IP>`.

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
| All of Ursa Minor | `ssh-box/levels/<star>.sh` | `docker compose up -d --build ssh-box` |
| Rigel | `rigel/app/init_db.py` | `docker compose up -d --build rigel` |
| Betelgeuse, Bellatrix, Mintaka, Alnilam | `web-box/<star>.py` | `docker compose up -d --build <star>` |
| Alnitak | `web-box/init_alnitak_db.py` | `docker compose up -d --build alnitak` |
| All of Gemini | `gemini (crypto)/make_files.py` | `python "challenges/gemini (crypto)/make_files.py"` |
| All of Lyra | `lyra (forensics)/make_files.py` | `python "challenges/lyra (forensics)/make_files.py"` |
| All of Scorpius | `<star>/src/flag.txt` | `docker compose up -d --build <star>` |
| All of Draco | `draco-box/levels/<star>/setup.sh` | `docker compose up -d --build draco-box` |

For Gemini and Lyra, run `ctfcli challenge sync` afterwards to upload the new files. Sulafat's flag is drawn on an image, so it can only use capital letters and the characters already in the script's font.

If you change `antares.c`, also re-export the download so it matches the running binary. From `challenges/scorpius (pwn)`, run `docker build --target dist --build-arg STAR=antares --output antares/dist .`

## Scoring options

To make points drop as more players solve a challenge, change these lines in its `challenge.yml`, then sync:

```yaml
type: dynamic
extra:
  initial: 100
  decay: 20
  minimum: 30
```

## Resetting

- **Clear scores between runs:** CTFd Admin Panel > Config > Reset.
- **Delete everything, including accounts and challenges:** remove auto-host first (`scripts\install-auto-host.ps1 -Remove`), or it can open CTFd to the network before setup has claimed it. Then run `docker compose down -v`, delete `.env`, `.ctf\config` and `LOGINS.txt`, and run [first-time setup](#first-time-setup) again. Setup turns auto-host back on.

## Replacing the admin token

1. In CTFd, go to **Settings > Access Tokens** and generate a new token.
2. Replace the `access_token` value in `.ctf/config`.
3. Delete the old token on the same page.
4. Check it works with `docker compose run --rm ctfcli challenge sync`.

## Troubleshooting

- **Other devices can't connect:** Check they're on the same network. Guest networks and some routers block devices from reaching each other. Then check the IP with `ipconfig` (Linux: `ip -4 addr`). On Linux, also check the firewall (see [Linux](#linux)).
- **The SSH box is stuck, for example after a fork bomb:** `docker compose restart ssh-box` (or `draco-box` for Draco)
- **`REMOTE HOST IDENTIFICATION HAS CHANGED` when connecting:** Rebuilding an SSH box gives it new keys, so anyone who connected before sees this. They can clear it with `ssh-keygen -R "[<host>]:2220"`, or `2222` for the Draco box. Avoid rebuilding either during an event.
- **A challenge port doesn't respond:** Check `docker compose ps`, then `docker compose logs <service>`.

## Linux

Everything runs the same on Linux. Every Windows script has a bash version in `scripts\`: `setup.sh`, `set-host.sh`, `demo.sh`, `install-auto-host.sh` and `auto-host.sh`. Run them with `bash scripts/<name>.sh`.

- **Docker without sudo:** the scripts and the cron jobs run as you, so add yourself to the `docker` group with `sudo usermod -aG docker "$USER"`, then log out and back in.
- **Docker at boot:** `sudo systemctl enable --now docker`, so auto-host can start the CTF after a reboot.
- **Firewall:** if players can't connect and you use `ufw`, open the ports:
  ```bash
  sudo ufw allow 8000/tcp && sudo ufw allow 2220/tcp && sudo ufw allow 2222/tcp && sudo ufw allow 8081:8086/tcp && sudo ufw allow 9001:9006/tcp
  # The demo CTF:
  sudo ufw allow 8100/tcp && sudo ufw allow 2221/tcp && sudo ufw allow 2223/tcp && sudo ufw allow 8091:8092/tcp && sudo ufw allow 9021:9022/tcp
  ```
- **Network address:** setup and auto-host use the address of the network card that reaches the internet. On a VPN, pass your Wi-Fi or LAN address with `--ip`.

## Giving STARS to someone else

Use a **private** GitHub repository, because the challenge files and answer sheets contain every flag. Only give access to other organizers.

**What's in git:** all the challenges and their downloads, the Docker setup, the scripts, the logo, and both answer sheets. `.gitattributes` makes git deliver the player downloads byte for byte. Without it, Git for Windows would change some of them, and the two PDFs would break.

**What isn't:** passwords and tokens (`.env`, `.ctf/config`, `LOGINS.txt`) and logs. Setup makes new ones on each PC. Your CTFd's accounts, teams and solves aren't in git either, because they live in Docker on your PC. The other person's setup starts with a fresh, empty CTF.

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
