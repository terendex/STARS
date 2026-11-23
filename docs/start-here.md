# Start here

New to running STARS? Read this page first. It assumes you've never used Docker, a terminal or GitHub before. By the end, you'll have made a practice challenge, tested it and removed it again, and you'll know where to look for everything else.

- [1. Install three programs](#1-install-three-programs)
- [2. Get the STARS folder](#2-get-the-stars-folder)
- [3. Open a terminal](#3-open-a-terminal)
- [4. Allow PowerShell scripts (once)](#4-allow-powershell-scripts-once)
- [5. How to read the commands in these docs](#5-how-to-read-the-commands-in-these-docs)
- [6. Your first challenge](#6-your-first-challenge)
- [7. Saving your changes](#7-saving-your-changes)
- [Words you'll see](#words-youll-see)
- [If you see this error](#if-you-see-this-error)
- [Learning to make challenges](#learning-to-make-challenges)
- [Who to ask](#who-to-ask)

## 1. Install three programs

All three are free:

| Program | What it's for |
|---|---|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Runs the CTFs. Start it, and wait until it says it's running, before you use STARS. |
| [Visual Studio Code](https://code.visualstudio.com/) (VS Code) | Editing files, and a terminal built in. When it offers to install the recommended YAML extension, say yes: it underlines mistakes in `challenge.yml` files. |
| [GitHub Desktop](https://desktop.github.com/) | Downloading the STARS folder, and sending your changes back so the next organizer gets them. |

You also need access to the private STARS repository on GitHub. Ask the previous organizer (or [Axel](#who-to-ask)) to add your GitHub account under the repository's **Settings > Collaborators**.

## 2. Get the STARS folder

1. Open GitHub Desktop and sign in to your GitHub account.
2. **File > Clone repository**, pick the STARS repository on the **GitHub.com** tab, choose where to put it (for example `Documents`), and press **Clone**.
3. If this PC will host the CTFs, run first-time setup now: see [running-an-event.md](running-an-event.md#first-time-setup).

## 3. Open a terminal

A terminal is a window where you type commands. The easiest one to use is inside VS Code:

1. In VS Code, **File > Open Folder**, and choose the STARS folder.
2. **Terminal > New Terminal**. A panel opens at the bottom with a line like:
   ```text
   PS C:\Users\you\Documents\STARS>
   ```
   That's PowerShell, waiting for a command, in the STARS folder. Every command in these docs starts from here unless it says otherwise.

To go into a folder, type `cd` and its name, like `cd sits`. To go back up one level, type `cd ..`. The part before `>` always shows which folder you're in.

## 4. Allow PowerShell scripts (once)

Windows doesn't let PowerShell run scripts until you allow it. Do this once on each PC. In the terminal, type:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

If it asks, type `Y` and press Enter. This only affects your Windows account, and still blocks scripts downloaded from the internet that aren't signed. Without it, commands like `scripts\check.ps1` stop with "running scripts is disabled on this system". The desktop buttons work either way.

## 5. How to read the commands in these docs

```powershell
cd sits                                     # go into the SITS folder
docker compose run --rm ctfcli challenge sync
```

- Type or paste **one line at a time**, then press **Enter**. Wait until the `PS ...>` line comes back before the next one.
- Everything after `#` is a note for you. You can paste it too: PowerShell ignores it.
- `<something>` means "put your own value here", without the `<` and `>`. For example, `scripts\check.ps1 <ctf>` becomes `scripts\check.ps1 sits`.
- After `cd sits`, the next commands run inside `sits` until you `cd ..`.
- Lines marked "Linux" are only for a Linux PC. These docs are written for Windows.
- Paths with spaces need quotes, like `"challenges/orion (web)/bellatrix"`.

## 6. Your first challenge

You'll make a small practice challenge in SITS, load it into CTFd hidden (so no player can ever see it), solve it yourself, then remove it. It takes about 15 minutes, and it's the same routine as making a real one. If something doesn't match what this page says, check [If you see this error](#if-you-see-this-error).

**Before you start:** Docker Desktop is running, and SITS is running (press **Start SITS CTF** on the desktop, or run `scripts\sits.ps1 start`). Its window shows SITS's address, like `http://192.168.1.20:8300`.

### Make the challenge's folder

1. In VS Code's file list on the left, find `docs/challenge-template`. Right-click it, **Copy**.
2. Right-click `sits/challenges/crypto`, **Paste**. Rename the copy (right-click, **Rename**) to `practice`.
3. Inside `practice`, make a new folder called `dist` (right-click `practice`, **New Folder**).

### Make the file players download

1. Open [CyberChef](https://gchq.github.io/CyberChef/) in your browser.
2. In **Operations** on the left, search for `To Base64` and drag it into **Recipe** in the middle.
3. In **Input**, type `FLAG{my_first_challenge}`. **Output** shows the encoded text.
4. In VS Code, right-click your `dist` folder, **New File**, call it `message.txt`, paste the Output into it, and save (Ctrl+S).

### Fill in challenge.yml

Open `sits/challenges/crypto/practice/challenge.yml`. The lines starting with `#` explain each field. Change these lines, keeping the spaces at the start of each line exactly as they are:

```yaml
name: "Practice"
author: "Your name"                   # your real name here
attribution: "Made by Your name"      # and here
category: "Crypto"
description: |-
  My first practice challenge.

  **Your goal:** decode the message (download it below). The decoded text is the flag.

  **Tools you may need to solve this level:** CyberChef
files:
  - dist/message.txt
flags:
  - "FLAG{my_first_challenge}"
hints:
  - content: "Search CyberChef's operations for Base64."
    cost: 5
state: hidden
```

Delete the `connection_info:` line, because this challenge has no port, only a download. Save.

### Check it

In the terminal, in the STARS folder:

```powershell
scripts\check.ps1 sits
```

You should see `0 error(s)` and two warnings. One says the flag isn't in `sits/ANSWERS.md`, which is fine for a practice challenge. The other says the challenge isn't added to CTFd yet, which is the next step. If you see an `ERROR`, it says which line to fix. Fix it, save, and run the check again.

### Load it into CTFd

```powershell
cd sits
docker compose run --rm ctfcli challenge add "challenges/crypto/practice"
docker compose run --rm ctfcli challenge install "challenges/crypto/practice"
cd ..
```

`add` prints nothing when it works. `install` ends with `Success! All challenges installed!`

### Solve it

1. Open SITS's address with `/admin` at the end (like `http://192.168.1.20:8300/admin`) and sign in as admin. The password is in `sits\LOGINS.txt`, under "Admin".
2. **Challenges** in the top menu, then click **Practice**. A red **hidden** badge shows under its name.
3. Below the name is a row of icons. Click the first one, a page (hover over it: **Preview Challenge**). You see the challenge the way players would.
4. Download `message.txt`, decode it in CyberChef with **From Base64**, and type the flag into the box. Press **Submit**. It says **Correct**. Preview never records a solve, so it doesn't count for anyone.

### Change something

1. In `challenge.yml`, change the hint's text, and save.
2. Check it, then sync just this challenge:
   ```powershell
   scripts\check.ps1 sits
   cd sits
   docker compose run --rm ctfcli challenge sync "challenges/crypto/practice"
   cd ..
   ```
3. Refresh Practice's page in the admin panel and open its **Hints** tab. The new text is there. (The Preview window only shows hints as locked buttons, because hints cost points and the admin account has no team to pay with.)

### Remove it

1. In the admin panel, on Practice's page, click the trash can, the last icon in the row, and confirm.
2. In VS Code, delete the `sits/challenges/crypto/practice` folder.
3. Open `sits/.ctf/config` and delete the line that starts with `challenges/crypto/practice`. Save. (`add` wrote that line. If it stays, every sync prints "could not be found" for it.)
4. Run `scripts\check.ps1 sits` once more. It should say `All good`.

That's the whole routine. Every real challenge follows it, with more care over the description and the hints. [making-challenges.md](making-challenges.md) covers each kind of challenge, and how to write them well.

## 7. Saving your changes

Your changes only exist on your PC until you send them to GitHub. Do this whenever you finish something, so the next organizer gets it:

1. **Before you start working,** open GitHub Desktop and press **Fetch origin**, then **Pull origin** if it appears. That gets everyone else's changes first.
2. **When you're done,** GitHub Desktop lists the files you changed on the left. Click one to see exactly what changed.
3. In the **Summary** box at the bottom left, describe what you did, like `Add a new Web challenge: Cookie Monster`, and press **Commit to main**.
4. Press **Push origin** at the top.

Passwords, tokens and logins (`.env`, `.ctf`, `LOGINS.txt`) never appear in GitHub Desktop, because the repository is set to ignore them. If you ever see one of those files in the list, don't commit it: ask for help.

## Words you'll see

| Word | What it means here |
|---|---|
| **CTF** | Capture the flag: a contest where players solve security puzzles to find secret text called flags. Each folder like `sits` is one CTF. |
| **Flag** | The secret answer to a challenge, like `FLAG{...}`. Players paste it into CTFd to get the points. |
| **Challenge** | One puzzle. Each has a folder with a `challenge.yml`. |
| **CTFd** | The website players log in to. It shows the challenges, checks flags and keeps the scores. |
| **Admin panel** | CTFd's organizer pages, at `/admin`. Only the admin account can open them. |
| **`challenge.yml`** | The file that describes a challenge: its name, text, points, flag and hints. Written in YAML. |
| **YAML** | The format of `challenge.yml`: `name: value` lines, where the spaces at the start of a line matter. |
| **Docker** | The program that runs the CTFs on this PC. Docker Desktop is its Windows app. |
| **Container** | One running program inside Docker, like CTFd, or one web challenge. Each CTF is many containers. |
| **Image** | The recipe a container is made from. "Rebuild" means making it again after you change its files. |
| **Box** | Our name for a container players log in to, like the Linux SSH box. Its levels are made when it's built. |
| **Port** | The number after the address, like `:8300` or `-p 2240`. Each challenge that runs on a server has its own. |
| **SSH** | A way to log in to another computer's terminal: `ssh <account>@<address> -p <port>`. Players use it for Linux and Reversing. |
| **`nc`** | Netcat: connects a terminal to a port, for the Pwn challenges. |
| **ctfcli** | The tool that loads `challenge.yml` files into CTFd. You run it with `docker compose run --rm ctfcli ...`. |
| **Sync** | Copying your changed `challenge.yml` into CTFd. |
| **Edge** | The part that connects players to each challenge's port. A new port needs a line in `edge/nginx.conf`. |
| **Repository (repo)** | The STARS folder on GitHub, with its full history. |
| **Commit / Push / Pull** | Save a set of changes / send them to GitHub / get everyone else's. |

## If you see this error

| You see | What it means | What to do |
|---|---|---|
| `running scripts is disabled on this system` | PowerShell isn't allowed to run scripts yet. | Do [step 4](#4-allow-powershell-scripts-once). |
| `docker` `is not recognized` | Docker Desktop isn't installed. | Install it, then open a new terminal. |
| `error during connect` or `The system cannot find the file specified` | Docker Desktop isn't running. | Start Docker Desktop, wait until it says it's running, and try again. |
| `no configuration file provided: not found` | You're in the wrong folder for `docker compose`. | `cd` into the CTF's folder (like `cd sits`) first. Check the `PS ...>` line. |
| `isn't valid YAML` (from the checker) | A mistake in `challenge.yml`'s format. | Look at the line it names. Usually a line has the wrong number of spaces at the start, or a tab instead of spaces. Text containing `: ` must be in quotes. VS Code's YAML extension underlines the spot. |
| `ERROR` from the checker | Something in a challenge is wrong. | The message says what. [making-challenges.md](making-challenges.md) explains each rule. |
| `Could not process the challenge path` | ctfcli can't find the folder you named. | Check the spelling, that you're in the right CTF's folder, and the quotes around paths with spaces. |
| `Found already existing challenge with the same name` | It's already in CTFd. | Use `challenge sync` instead of `install`. |
| `LEVEL FAILED: /build/levels/...` | A level's script failed while its box was built. | Scroll up: the lines above it show which command failed. Fix that script and rebuild. |
| `port is already allocated` or `Ports are not available` | Another challenge or CTF already uses that port. | Pick another port, in both `docker-compose.yml` and `edge/nginx.conf`. The port table is in [new-event.md](new-event.md). |
| A correct-looking flag is rejected | The flag in CTFd doesn't match the one the challenge gives out. | Check for typos and spaces. If you changed the flag, see [If you change a flag](making-challenges.md#if-you-change-a-flag): it lives in two places. |
| `has not started yet` (players) | The mission clock is in standby. | Press Start on the Mission Clock page. |
| GitHub Desktop says the push was rejected | Someone else pushed changes first. | Press **Pull origin**, then **Push origin** again. If it mentions a conflict, ask for help. |

For problems while running an event, see [Troubleshooting](running-an-event.md#troubleshooting).

## Learning to make challenges

This folder makes adding a challenge easy. Inventing a good one needs you to know that skill yourself, and the best way to learn is to play other people's. All of these are free, and STARS's challenges borrow ideas from them:

| Site | Good for |
|---|---|
| [picoCTF](https://picoctf.org/) | Every category, made for high-school beginners. Start with its practice gym. |
| [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/) | Linux. STARS's tools lines copy its style. |
| [PortSwigger Web Security Academy](https://portswigger.net/web-security) | Web, with free labs. |
| [CryptoHack](https://cryptohack.org/) | Crypto. |
| [pwn.college](https://pwn.college/) | Pwn and reversing, from the basics. |

A good way to start making your own: take an Easy challenge in this folder that you understand, and make a new one with the same idea but different details. Then play the existing challenges in each category, and read their walkthroughs in `ANSWERS.md`.

## Who to ask

Axel Jonas C. Tangalin made STARS and SITS:

- **Facebook:** Axel Jonas C. Tangalin
- **Discord:** terendex
- **Email:** lol.doge27@gmail.com

When you ask, say which CTF, what you did, and what happened. A screenshot of the error helps.
