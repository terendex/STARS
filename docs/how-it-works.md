# How it works

A short tour of what's under the hood, for when you want to change how STARS behaves rather than add a challenge.

## The big picture

Each CTF (`2nd-star`, `classic`, `demo`, `demo2`, `sits`) is one **Docker Compose project**: a `docker-compose.yml` that starts a set of containers together. They all look like this:

```text
                 players' laptops (same Wi-Fi)
                   |                       |
        http://<ip>:8000              ports 2220, 8081..., 9001...
                   |                       |
   +---------------v----------+   +--------v--------+
   | ctfd   (the website)     |   | edge  (nginx)   |  the only door into
   |   + ctfd-plugin/         |   +--------+--------+  the challenges
   +----+-----------+---------+            |
        |           |             internal network, no internet
   +----v---+  +----v----+        +--------v---------------------------+
   | db     |  | cache   |        | ssh-box, draco-box, web apps,       |
   |MariaDB |  | Redis   |        | pwn programs ... (one per service)  |
   +--------+  +---------+        +-------------------------------------+

   ctfcli (only runs when you call it): reads challenge.yml files and
   pushes them into ctfd. Also runs the Python scripts in scripts/.
```

- **ctfd** is [CTFd](https://ctfd.io), the website players log in to, version 3.8.9. It stores everything (accounts, solves, challenges) in **db** (MariaDB), and **cache** (Redis) speeds it up.
- **edge** is an nginx proxy. Challenge containers sit on an internal network with no route out, so edge is what publishes their ports. `edge/nginx.conf` maps each port to a container.
- **Challenge containers** are built from the folders in `challenges/`. They're read-only, with limits on CPU, memory and processes (the `x-challenge` block at the top of each `docker-compose.yml`).
- **ctfcli** is CTFd's command-line tool, version 0.1.8, in `tools/ctfcli/`. `docker compose run --rm ctfcli ...` starts it, does the job and removes it. It mounts the whole STARS folder, so it can run the scripts in `scripts/`.

Every container only publishes on the address in the CTF's `.env` (`CTF_BIND_IP`), which set-host keeps equal to this PC's Wi-Fi address. `2nd-star/.env` is the one the other CTFs copy their address from.

## Where the data lives

Everything players do (accounts, teams, solves, hints bought, the help queue, the clock) is in Docker **volumes**, named after the CTF: `stars_db_data` for 2nd Star, `stars-classic_db_data`, `stars-demo_db_data`, `stars-demo2_db_data` and `sits_db_data`. They survive stopping, restarting and rebuilding. Only `docker compose down -v` deletes them.

To keep a copy, use **Admin Panel > Config > Backup** in each CTFd. It downloads a zip you can restore with **Import**. Old backups of the whole folder can go in `backups\`, which git ignores.

## The CTFd plugin (`ctfd-plugin/`)

The features CTFd doesn't have come from a plugin. 2nd Star, Classic and SITS mount this folder into their CTFd. The two demos share their own, smaller one in `demo/ctfd-plugin/`.

| File | What it does |
|---|---|
| `__init__.py` | Loads everything. Makes the email optional in the admin's Create User form, sets a separate login cookie per CTF (`STARS_SESSION_COOKIE`), and runs the mission clock: the admin page, its buttons, and the projector page `/timer`. |
| `extras.py` | First blood (the public list, and the admin table on Statistics) and the help queue (the `stars_help` table, and the player and admin pages). |
| `assets/clock-watch.js` | On players' challenges page: reloads it when the clock starts or ends. Players never see a countdown. |
| `assets/clock.js`, `clock.css` | The projector page: the countdown, first blood banners, music. |
| `assets/music.js`, `playlist.json` | The Spotify player and its track list. `scripts/set-playlist.py` rewrites the list. |
| `assets/help.js` | The **Ask for help** button on the challenges page. |
| `assets/admin-extras.js` | The First Bloods table on Statistics and the waiting count next to **Help Queue** in the admin menu. |
| `templates/` | The HTML for the Mission Clock page, the projector page and the Help Queue page. |

The demos' `demo/ctfd-plugin/__init__.py` signs every visitor in as `demo1` (`STARS_DEMO_AUTOLOGIN` in each demo's `docker-compose.yml`), so nobody needs an account to try them. `STARS_SESSION_COOKIE` gives each demo its own login cookie.

**To change the plugin:** edit the file, then restart CTFd in every CTF that uses it. From each CTF's folder: `docker compose restart ctfd`. Don't do it during an event: CTFd is down for a few seconds. For JavaScript, refresh the browser too.

**Keep pages plain.** The admin pages use CTFd's own look (Bootstrap 4): standard buttons, short plain labels, no decorative styling.

## The scripts (`scripts/`)

Each Windows script (`.ps1`) has a Linux version (`.sh`) with the same name, except the desktop buttons. The `.py` scripts run inside the ctfcli container.

| Script | What it does |
|---|---|
| `setup.ps1` | First-time setup of 2nd Star and the demo, auto-host and the desktop buttons. |
| `start-stars.ps1`, `stop-stars.ps1` | The **Start STARS** and **Stop STARS** buttons. Stop stops every CTF. |
| `start-sits.ps1` | The **Start SITS CTF** button. |
| `install-shortcuts.ps1` | Puts those buttons on the desktop. |
| `classic.ps1`, `demo.ps1`, `demo2.ps1`, `sits.ps1` | `setup`, `start`, `stop`, `sync` and `teams` for each side CTF. |
| `set-host.ps1` | Moves every CTF to a new IP: `.env` files, `connection_info`, answer sheets, CTFd. |
| `auto-host.ps1`, `install-auto-host.ps1` | The scheduled task that runs set-host when the network changes. Its log is `logs\auto-host.log`. |
| `check.ps1`, `check-challenges.py` | The challenge checker (see [making-challenges.md](making-challenges.md)). |
| `setup-ctfd.py` | Finishes CTFd's setup wizard for a new CTF: name, rules, logo, admin, API token. Has one profile per CTF. |
| `home_page.py` | The CTFd home pages with the "How to play" guide. Running it pushes a page to a running CTFd. |
| `make-teams.py` | Makes teams named Alpha, Bravo, ... with 3 random accounts each. |
| `update-connection-info.py` | Copies just the addresses from `challenge.yml` into CTFd. Safe during an event, unlike sync. |
| `set-playlist.py` | Points the music at another Spotify album or playlist. |

To push a changed home page to a running CTFd, from the STARS folder:

```powershell
docker compose -f 2nd-star/docker-compose.yml run --rm --entrypoint python ctfcli ../scripts/home_page.py main
docker compose -f sits/docker-compose.yml run --rm --entrypoint python ctfcli ../scripts/home_page.py sits
```

## Versions and their quirks

Upgrading CTFd or ctfcli may break things. Test an upgrade on a copy first, not on the day.

- **CTFd 3.8.9** (`image: ctfd/ctfd:3.8.9` in each `docker-compose.yml`). In this version, points that drop with each solve are built into `type: standard`, and `type: dynamic` breaks with sync. `setup-ctfd.py` reads CTFd's setup page, so a new version may need changes there.
- **ctfcli 0.1.8** (`tools/ctfcli/Dockerfile`). It never sends `author`, so the credit players see comes from `attribution`. `challenge verify` reports a difference in `extra` for every challenge, which is harmless.
- **The login limit.** On Docker Desktop, CTFd sees every player as the same address, so its limit of about 10 logins in a few seconds applies to the whole room.
- **Wrong flags.** CTFd accepts about 10 wrong flags a minute per account, and then refuses for a while.

## Line endings

The scripts and configs run inside Linux containers, where Windows line endings break them. `.gitattributes` makes git keep LF line endings on every PC, and leaves player downloads (`dist/`, pictures, PDFs, captures) exactly as they are. If you add a file type that must not change, add it there. `.vscode/settings.json` makes VS Code save new files with LF line endings too, and `.vscode/extensions.json` recommends the YAML extension.

## The tick or X next to commits on GitHub

Each commit pushed to GitHub is checked by SonarQube Cloud (SonarCloud), a code-quality service, which marks it with a green tick or a red X. It only checks STARS's own code, the scripts and the CTFd plugin. `.sonarcloud.properties` tells it to skip every `challenges` folder, because the challenges are insecure on purpose. A red X never stops anything from working, and the CTFs don't depend on it. Click it on GitHub to see what SonarCloud found. Ask the repository's owner if you need access to its full report.
