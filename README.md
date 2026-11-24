# STARS CTF

Capture the flag events hosted from one PC. Players join over the same Wi-Fi, log in to a CTFd website, solve challenges and submit the flags they find. Only the organizers can see the scoreboard.

STARS and the SITS Capture The Flag Competition 2026 were made by Axel Jonas C. Tangalin. This folder is everything needed to run them again, change them, or build the next event.

**This folder contains every flag and every answer sheet. Keep it in a private repository, and share it only with organizers.**

## The CTFs

Each CTF is its own folder with its own website, accounts and scores. They can run at the same time on one PC.

| CTF | Folder | Players open | Flags look like | Start it with |
|---|---|---|---|---|
| **2nd Star**, the main STARS event (56 challenges) | [2nd-star/](2nd-star/) | `http://<host>:8000` | `STARS{...}` | the **Start STARS** button |
| **STARS Classic**, the first orientation (36) | [classic/](classic/) | `http://<host>:8200` | `STARS{...}` | `scripts\classic.ps1 start` |
| **STARS Demo**, safe to show anyone (12) | [demo/](demo/) | `http://<host>:8100` | `STARS{...}` | `scripts\demo.ps1 start` |
| **STARS Demo 2**, ★★ Medium, one per category (6) | [demo2/](demo2/) | `http://<host>:8500` | `STARS{...}` | `scripts\demo2.ps1 start` |
| **SITS Capture The Flag Competition 2026** (83) | [sits/](sits/) | `http://<host>:8300` | `FLAG{...}` | the **Start SITS CTF** button |

`<host>` is the CTF PC's Wi-Fi address, which the Start buttons show. **Stop STARS** stops all of them. Each folder's README lists its ports and commands.

## What's in this folder

| Folder | What it is |
|---|---|
| `2nd-star/`, `classic/`, `demo/`, `demo2/`, `sits/` | The five CTFs: their challenges, answer sheets, and Docker setup |
| `docs/` | The manual, and a blank challenge to copy |
| `scripts/` | Setup, start, stop, sync, making teams, and the challenge checker |
| `ctfd-plugin/` | Features added to CTFd: the mission clock, music, first blood, the help queue |
| `tools/ctfcli/` | The tool that loads challenges into CTFd |
| `branding/` | The STARS logo and icons |
| `logs/`, `backups/` | Made on the CTF PC, never in git |

## Quick start

**New to this?** Read [docs/start-here.md](docs/start-here.md) first. It explains what to install, how to use the terminal, and walks you through making your first challenge.

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and start it (Linux: Docker Engine with the Compose plugin).
2. Connect to the Wi-Fi the players will use, then run this once from this folder:
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\setup.ps1    # Linux: bash scripts/setup.sh
   ```
3. After that, use **Start STARS** and **Stop STARS** on the desktop. Nothing starts by itself when the PC starts.
4. Before each event, make the teams and test from a phone. The [event day checklist](docs/running-an-event.md#event-day-checklist) has every step.

Admin passwords are in each CTF's `LOGINS.txt`, made by setup.

## The manual

| Read this | When you want to |
|---|---|
| [docs/start-here.md](docs/start-here.md) | get started if you're new: installing, the terminal, a practice challenge, saving your changes to GitHub, a glossary, and common errors |
| [docs/running-an-event.md](docs/running-an-event.md) | set up, run an event day, make teams, use the mission clock, reset, or fix a problem |
| [docs/making-challenges.md](docs/making-challenges.md) | add a challenge, edit one, change a flag, or hide one |
| [docs/new-event.md](docs/new-event.md) | start a new event, like next year's competition, by copying one of the CTFs |
| [docs/how-it-works.md](docs/how-it-works.md) | understand or change how STARS itself works: the containers, the plugin, the scripts |

Before loading new or changed challenges into CTFd, run the checker. It only reads files and points out common mistakes:

```powershell
scripts\check.ps1     # Linux: bash scripts/check.sh
```

## Who to ask

Axel Jonas C. Tangalin made STARS and SITS, and is happy to help:

- **Facebook:** Axel Jonas C. Tangalin
- **Discord:** terendex
- **Email:** lol.doge27@gmail.com

When you ask, say which CTF, what you did, and what happened. A screenshot of the error helps.

## Credits

STARS (2nd Star, STARS Classic and both demos) and the SITS Capture The Flag Competition 2026 were made by Axel Jonas C. Tangalin. If you add challenges, put your own name in their `author` and `attribution`.
