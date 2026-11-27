# Running an event

How to set STARS up, run an event day, and fix things when they go wrong. Most commands are for Windows PowerShell, with the Linux version next to them. Run them from the STARS folder unless a step says to `cd` into a CTF's folder.

- [Event day checklist](#event-day-checklist)
- [First-time setup](#first-time-setup)
- [Starting and stopping](#starting-and-stopping)
- [Registering players](#registering-players)
- [Mission clock](#mission-clock)
- [First blood and help requests](#first-blood-and-help-requests)
- [If your IP changes](#if-your-ip-changes)
- [Resetting](#resetting)
- [Replacing the admin token](#replacing-the-admin-token)
- [Troubleshooting](#troubleshooting)
- [Linux](#linux)
- [Giving STARS to someone else](#giving-stars-to-someone-else)
- [How it's isolated](#how-its-isolated)

## Event day checklist

**A few days before**

1. If you changed any challenges, run `scripts\check.ps1`, then sync (see [making-challenges.md](making-challenges.md)).
2. Make the teams: `scripts\sits.ps1 teams 15` or `scripts\classic.ps1 teams 15`. For 2nd Star, see [Registering players](#registering-players). Print or copy the logins from that CTF's `LOGINS.txt`.
3. Start the CTF and play one Easy challenge per category yourself, from another laptop or a phone on the same Wi-Fi. Connections from the CTF PC to itself don't prove that other devices can reach it.

**On the day**

1. Connect the CTF PC to the Wi-Fi the players will use, plug it in, and turn off sleep.
2. Press **Start STARS** (or **Start SITS CTF**) on the desktop. Its window shows the players' address. Write it on the board.
3. Put the [mission clock](#mission-clock) in **Standby**, and choose its length.
4. Show the clock on the projector: press **Full screen** on the Mission Clock page, or open the projector address on the CTF PC (`http://localhost:8001/timer` for 2nd Star).
5. Have teams log in a few at a time (see [Registering players](#registering-players) for why).
6. Press **Start**. Keep **Admin Panel > Help Queue** open on a second screen or phone.

**After**

1. **Admin Panel > Config > Backup** saves the results.
2. Press **Stop STARS**. Accounts and scores are kept.
3. To run it again with the same accounts, see [Resetting](#resetting).

## First-time setup

On **Windows**, install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and start it. On **Linux**, install Docker Engine with the Compose plugin, and make sure your account can run `docker` without `sudo` (see [Linux](#linux)). Then connect to the network the players will use, and run one command from the STARS folder:

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

```bash
# Linux
bash scripts/setup.sh
```

The first run downloads and builds everything, so it takes a few minutes. It:

1. Makes `2nd-star\.env` with new random passwords.
2. Starts CTFd on this PC only and claims the admin account, because the first person to open CTFd's setup page becomes admin.
3. Sets CTFd up for the event: teams of 3, private registration, and the scoreboard and team lists hidden from players. It also uploads the STARS logo from `branding\`.
4. Installs all 56 challenges of 2nd Star.
5. Opens the CTF on this PC's network address.
6. Sets up the demo CTF.
7. Turns on [auto-host](#if-your-ip-changes), so the CTF follows your network, and puts **Start STARS** and **Stop STARS** buttons on the desktop (Windows). After that, nothing starts STARS by itself.

The admin password goes into `2nd-star\LOGINS.txt`. Running setup again is safe, because anything already set up is skipped. Options: `-Ip <address>` / `--ip <address>` to choose the address yourself, `-NoDemo` / `--no-demo`, and `-NoAutoHost` / `--no-auto-host`.

STARS Classic and SITS aren't set up by this, so a fresh install stays small. Set them up with `scripts\classic.ps1 setup` and `scripts\sits.ps1 setup` (Linux: `bash scripts/classic.sh setup`, `bash scripts/sits.sh setup`). SITS uses the same admin name and password as 2nd Star.

## Starting and stopping

STARS never starts by itself when the PC starts, and Docker doesn't restart its containers. Use the buttons on the desktop:

- **Start STARS** starts Docker Desktop if it's closed, then 2nd Star on this PC's current network. When it's done, its window shows the players' address and the Mission Clock's.
- **Start SITS CTF** does the same for SITS.
- **Stop STARS** stops every CTF: 2nd Star, Classic, both demos and SITS. Accounts, scores and the clock are kept.

First-time setup puts the buttons there. To add them again, for example after moving the STARS folder, run `scripts\install-shortcuts.ps1`.

The same from a terminal:

```powershell
scripts\start-stars.ps1        # start 2nd Star
scripts\sits.ps1 start         # start SITS (also: classic.ps1, demo.ps1, demo2.ps1)
scripts\stop-stars.ps1         # stop everything, keeping scores and accounts
cd 2nd-star; docker compose logs -f    # watch a CTF's logs
```

If something stops during the event, **Start STARS** (or `docker compose up -d` in that CTF's folder) brings it back. To have the CTF start whenever you sign in, run `scripts\install-auto-host.ps1 -StartAtSignIn` (Linux: `bash scripts/install-auto-host.sh --start-at-boot`). The buttons are Windows only. On Linux, use `docker compose up -d` and `docker compose stop` in the CTF's folder.

## Registering players

Players can't register themselves, so make their teams and accounts before the event. Say how many teams you want:

```powershell
scripts\sits.ps1 teams 15          # SITS
scripts\classic.ps1 teams 15       # STARS Classic

# 2nd Star
cd 2nd-star
docker compose run --rm --entrypoint python ctfcli ../scripts/make-teams.py 15
```

Teams are named with NATO call signs (Alpha, Bravo, Charlie, and so on), and each gets 3 accounts with random names, like `otter42`. The first player is the captain, and nobody needs an email. No account belongs to anyone in particular, so on the day you can give any team's logins to any group. Running it again adds more teams after the last call sign.

The passwords go into that CTF's `LOGINS.txt`, which stays out of git, and aren't printed. Each is two words and a number, like `maple-anvil-318`, so it's easy to type. Players log in with the name, in any capitals. They're already on their team, so they don't need the team's password. Solves, hints and wrong flags belong to the team: once one member solves a challenge, it's solved for all three.

On Windows, Docker Desktop makes every player reach CTFd from the same address, so CTFd's login limit covers the whole room. Once 10 people have logged in within a few seconds of each other, it answers "Too many requests" until 5 seconds pass with no new login. Have teams log in one at a time, or tell players to wait a few seconds and try again.

To add a team or player by hand, sign in as admin:

1. **Admin Panel > Teams**, then **+** (Create Team). Give the team a name and a password.
2. **Admin Panel > Users**, then **+** (Create User) for each player. Give them a name and a password. You can leave the email empty.
3. Open each team and use the **Add Team Members** icon to add its 3 players.
4. Hand each player their name and password.

Put every player on a team. A player without one gets stuck on CTFd's "join a team" page after logging in, because team creation is off. To see the scores yourself, open **Admin Panel > Scoreboard**.

## Mission clock

The mission clock decides when players can play. While it's running, players see the challenges and can submit flags. Before it starts, CTFd says the CTF hasn't started yet, and when it reaches zero, flag submissions close. Players never see a countdown, so they aren't put under pressure: their challenges page just opens when you press Start and closes at the end. Admins can always open every challenge and check its flag with **Preview Challenge** (see [Testing it](making-challenges.md#testing-it)), so you can test while it's stopped.

Sign in as admin and open **Admin Panel > Mission Clock**. It has:

- **Length:** type hours, minutes and seconds, or pick a preset (30 minutes to 3 hours).
- **Start:** opens the challenges and starts the countdown from the length.
- **Restart:** starts the countdown again from the full length. It doesn't touch scores. To clear those, see [Resetting](#resetting).
- **+5 min / −5 min:** moves the end time while it's running. Adding time after it has ended reopens it.
- **End now:** closes submissions straight away.
- **Standby:** stops the clock and hides the challenges until you press Start. Put the clock in standby before players arrive.
- **No time limit:** turns the clock off, so the CTF is open for as long as you like.
- **Music:** where the music plays: **This page** (the Mission Clock page), **Projector page**, or **Off**. Only the chosen page plays, so it never plays twice.
- **Full screen** (or press F): fills your screen with the countdown, for the projector.

**On the projector,** either press **Full screen** on the Mission Clock page, or open the projector page on the CTF PC, which shows the same countdown with no controls. It's `http://localhost:8001/timer` for 2nd Star, `8002` for Classic and `8003` for SITS. These `localhost` addresses only work on the CTF PC itself. The demos have no clock.

**Music:** while the clock runs, the chosen page plays the tracks of a Spotify album in a random order, with a new order on every Start or Restart. N or **Skip** skips a track. It pauses when the clock ends or goes back to standby. Browsers only allow sound after a click on the page:

- With **This page**, pressing Start is that click, so the music starts with the clock. Only the browser where you pressed Start plays. If you reload the page while the clock runs, press **Turn on sound**.
- With **Projector page**, click the projector page once when it says so, before or after Start.

It also needs:

- **Internet on the CTF PC.** Without it, the page says so, and the clock still works.
- **`localhost`, for whole songs.** Spotify only plays whole songs on a secure page, and browsers count `http://localhost` as secure but not `http://<host>`. So for whole songs, open the Mission Clock as `http://localhost:8001/admin/stars-timer` (sign in there once) or the projector page as `http://localhost:8001/timer`. On `http://<host>:8000`, the music only plays previews, and the Mission Clock page says so.
- **Spotify signed in, in that browser,** for whole songs. Otherwise Spotify only plays short previews.

The tracks are listed in `ctfd-plugin/assets/playlist.json`. To use another album or playlist, run `python scripts/set-playlist.py <Spotify link>`, then refresh the page. It only needs Python, no extra packages.

## First blood and help requests

**First blood** is the first team to solve *anything* in the whole event — whoever lands the first correct answer. Exactly one team takes it. Hidden teams and admins never count, so testing can't take it.

- **On the projector page,** first blood shows at the top for 8 seconds when it happens: the team, and the challenge it solved. If you put a sound file at `ctfd-plugin/assets/first-blood.mp3`, it plays with the banner (once someone has clicked the page to turn on sound). With no file there, the banner just shows in silence.
- **Admin Panel > Statistics** has a **First Blood** entry above Player Progression: which team took it, the player who did, the challenge, the time, and how long after the start.

**Help requests:** players press **Ask for help** in the corner of the challenges page. The challenge they have open is chosen for them, and they can say what they've tried. Each team has one request at a time. Asking again changes it.

- **Admin Panel > Help Queue** lists the requests, oldest first, with how long each team has waited. **On my way** tells the team someone is coming, and **Done** clears it from their screen. The page checks every 5 seconds, and plays a short sound for each new request once you've clicked anywhere on it.
- The **Help Queue** link in the admin menu shows how many teams are waiting, on every admin page.
- The player sees their place in the queue, then "An organizer is on the way". They can also cancel.
- Finished requests stay listed until you press **Clear finished**. CTFd's own Reset doesn't clear them.

2nd Star, Classic and SITS have both. The demos don't.

## If your IP changes

Your IP comes from the router, so it changes when you join another network, and sometimes on the same one. The ports stay the same, and every CTF moves together.

**Automatically:** run `scripts\install-auto-host.ps1` once (first-time setup does it for you). It sets up a task that runs as you, hidden, with no admin rights. When Windows connects to a network, and every 5 minutes, it moves the CTFs to your new IP and updates the addresses in CTFd and in the `ANSWERS.md` files.

It never starts a CTF. A CTF that isn't running stays off, and only its files are updated, so it starts on the right address next time. If Docker Desktop is closed, the task does nothing. Everything it does is logged to `logs\auto-host.log`. To turn it off, run `scripts\install-auto-host.ps1 -Remove`.

The task follows **any** network this PC joins, so a running CTF opens to everyone on it, including public Wi-Fi. Stop the CTF before you join an untrusted network.

**By hand:** run `scripts\set-host.ps1 -Ip <new IP>`.

**On Linux:** `bash scripts/install-auto-host.sh` adds a cron job that moves the CTF to your new IP within 5 minutes of a network change. `--start-at-boot` adds a second one that starts the CTF at boot. Remove them with `bash scripts/install-auto-host.sh --remove`. By hand, run `bash scripts/set-host.sh <new IP>`.

All of these only change the addresses in CTFd, so they're safe during an event. Players still need the new address, so tell them. To keep the same address at a venue, reserve it for this PC in the router's DHCP settings.

## Resetting

- **Clear scores between runs:** in that CTF's CTFd, **Admin Panel > Config > Backup** first, to keep a copy of the results. Then **Admin Panel > Config > Reset**, and tick **Submissions** only, which keeps the accounts and teams. Then sync (`cd 2nd-star; docker compose run --rm ctfcli challenge sync`, or `scripts\sits.ps1 sync`), so every challenge goes back to its starting points, and put the [mission clock](#mission-clock) in standby.
- **Delete everything in 2nd Star, including accounts and challenges:** remove auto-host first (`scripts\install-auto-host.ps1 -Remove`), or it can open CTFd to the network before setup has claimed it. Then, in `2nd-star`, run `docker compose down -v`, delete `.env`, `.ctf\` and `LOGINS.txt`, and run [first-time setup](#first-time-setup) again. Setup turns auto-host back on.
- **Delete everything in Classic, a demo or SITS:** in its folder, run `docker compose down -v`, delete its `.env`, `.ctf\` and `LOGINS.txt`, then run its `setup` again (for example `scripts\sits.ps1 setup`).

## Replacing the admin token

Each CTF has its own token in its `.ctf\config`. To replace one, for example if it was shared by mistake:

1. In that CTF's CTFd, go to **Settings > Access Tokens** and generate a new token.
2. Replace the `access_token` value in that CTF's `.ctf\config` (for example `2nd-star\.ctf\config`).
3. Delete the old token on the same page.
4. Check it works with a sync.

## Troubleshooting

Run `docker compose` commands from the CTF's own folder (`2nd-star`, `classic`, `demo`, `demo2` or `sits`). For error messages from commands, see [If you see this error](start-here.md#if-you-see-this-error).

- **Other devices can't connect:** check they're on the same network. Guest networks and some routers block devices from reaching each other. Then check the IP with `ipconfig` (Linux: `ip -4 addr`). On Linux, also check the firewall (see [Linux](#linux)).
- **An SSH box is stuck, for example after a fork bomb:** `docker compose restart ssh-box` (or `draco-box`; in SITS, `linux-box` or `rev-box`).
- **`REMOTE HOST IDENTIFICATION HAS CHANGED` when connecting:** the SSH box got new keys, so anyone who connected before sees this. They can clear it with `ssh-keygen -R "[<host>]:2220"`, using that box's port. To stop it happening, see [Keeping the SSH keys](#keeping-the-ssh-keys).
- **A challenge port doesn't respond:** check `docker compose ps`, then `docker compose logs <service>`. Containers don't restart by themselves, so `docker compose up -d` starts anything that stopped.
- **Players see "2nd Star has not started yet" or "has ended":** that's the [mission clock](#mission-clock). Press Start, or **No time limit** to turn it off.
- **A team is locked out of a challenge:** each team gets 3 wrong flags per challenge. To unlock it, delete one of the team's wrong submissions for it in **Admin Panel > Submissions**, then have them wait a minute.
- **"Too many requests" at login:** see [Registering players](#registering-players).

### Keeping the SSH keys

Each SSH box has its own keys, which players' computers remember. Rebuilding a box would normally make new ones. To avoid that, each box installs the keys in its `host-keys` folder when it's built, if there are any. These folders stay out of git, because they're this server's private keys. A copy of STARS on another PC makes its own.

To save a running box's keys into its folder, for example after a fresh install, run this from the `2nd-star` folder (or from `classic`, which has the same boxes):

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

For SITS, run it from `sits` with `linux-box` → `challenges/linux/linux-box/host-keys/` and `rev-box` → `challenges/reversing/rev-box/host-keys/`. Copy the key files one by one, as here. Copying the whole `/etc/ssh` folder fails on Windows, because it holds a link Windows won't create.

## Linux

Everything runs the same on Linux. Every Windows script except the desktop buttons has a bash version in `scripts/`. Run them with `bash scripts/<name>.sh`.

- **Docker without sudo:** the scripts and the cron jobs run as you, so add yourself to the `docker` group with `sudo usermod -aG docker "$USER"`, then log out and back in.
- **Docker at boot:** `sudo systemctl enable --now docker`, if you use `--start-at-boot`.
- **Firewall:** if players can't connect and you use `ufw`, open the ports:
  ```bash
  # 2nd Star
  sudo ufw allow 8000/tcp && sudo ufw allow 2220/tcp && sudo ufw allow 2222/tcp && sudo ufw allow 8081:8090/tcp && sudo ufw allow 9001:9006/tcp
  # The demo
  sudo ufw allow 8100/tcp && sudo ufw allow 2221/tcp && sudo ufw allow 2223/tcp && sudo ufw allow 8091:8092/tcp && sudo ufw allow 9021:9022/tcp
  # The 2nd demo
  sudo ufw allow 8500/tcp && sudo ufw allow 2250/tcp && sudo ufw allow 2252/tcp && sudo ufw allow 8501/tcp && sudo ufw allow 9051/tcp
  # STARS Classic
  sudo ufw allow 8200/tcp && sudo ufw allow 2230/tcp && sudo ufw allow 2232/tcp && sudo ufw allow 8201:8206/tcp && sudo ufw allow 9031:9036/tcp
  # SITS
  sudo ufw allow 8300/tcp && sudo ufw allow 2240/tcp && sudo ufw allow 2242/tcp && sudo ufw allow 8301:8315/tcp && sudo ufw allow 9041:9048/tcp
  ```
- **Network address:** setup and auto-host use the address of the network card that reaches the internet. On a VPN, pass your Wi-Fi or LAN address with `--ip`.

## Giving STARS to someone else

Use a **private** GitHub repository, because the challenge files and answer sheets contain every flag. Only give access to other organizers.

**What's in git:** all the challenges and their downloads, the Docker setup, the scripts, the logo, the docs and the answer sheets. `.gitattributes` makes git deliver the player downloads byte for byte. Without it, Git for Windows would change some of them, and the PDFs would break.

**What isn't:** passwords and tokens (each CTF's `.env`, `.ctf\` and `LOGINS.txt`), the SSH boxes' keys (`host-keys\`), logs and backups. Setup makes new ones on each PC. Accounts, teams and solves aren't in git either, because they live in Docker on the PC that ran the event. The other person's setup starts with a fresh, empty CTF.

To add another organizer, open the repository on github.com, go to **Settings > Collaborators**, and add them. They download it with `git clone <the repository's address>`, start Docker, and run [first-time setup](#first-time-setup).

## How it's isolated

- Challenge containers sit on an internal Docker network with no route to your PC, your LAN, or the internet. The `edge` proxy is the only thing publishing their ports.
- CTFd, MariaDB and Redis are on a separate network that challenges can't reach.
- Ports are published on the address in `CTF_BIND_IP` only, so they aren't exposed on other adapters such as Radmin VPN or Tailscale.
- Challenge containers have read-only filesystems, limited capabilities, and CPU, memory and process limits.
- As on OverTheWire, players on an SSH box can see each other's processes and anything left world-readable in `/tmp`.
