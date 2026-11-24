# 2nd Star

The main STARS CTF: the second orientation's 56 challenges in six categories. Each category is a constellation and each challenge is one of its stars. Flags look like `STARS{...}`.

## What players use

| What | Address |
|---|---|
| Login, challenges, flags, downloads | `http://<host>:8000` |
| Ursa Minor (Linux), shared SSH box | `ssh <star>@<host> -p 2220` |
| Orion (Web) | `http://<host>:8081` to `8090` |
| Gemini (Crypto), Lyra (Forensics) | files downloaded from CTFd |
| Scorpius (Pwn) | `ssh <star>@<host> -p 2220`, or `nc <host> 9002` to `9006` |
| Antares (Pwn, Hard) | `nc <host> 9001` |
| Draco (Reversing), its own SSH box | `ssh <star>@<host> -p 2222`, password `draco` |
| Mission clock, for the projector | `http://localhost:8001/timer`, on the CTF PC only |

Every category has 5 Easy, 4 Medium and 1 Hard challenge, except Scorpius, which has 3 Easy, 2 Medium and 1 Hard. Each category has a "Start here" challenge that walks through every step: Pherkad, Betelgeuse, Pollux, Sheliak, Shaula and Thuban.

## Commands

```powershell
scripts\start-stars.ps1     # or the Start STARS button
scripts\stop-stars.ps1      # or Stop STARS; keeps accounts and scores

cd 2nd-star
docker compose run --rm ctfcli challenge sync                                   # after editing a challenge.yml
docker compose run --rm --entrypoint python ctfcli ../scripts/make-teams.py 15  # 15 teams of 3
```

## What's in this folder

| Path | What it is |
|---|---|
| `challenges/<constellation> (<skill>)/<star>/` | One folder per challenge, with its `challenge.yml` |
| `challenges/ursa-minor (linux)/ssh-box/` | The Linux SSH box. Its levels are in `levels/`. |
| `challenges/draco (reversing)/draco-box/` | The reversing SSH box. Its levels are in `levels/`. |
| `challenges/orion (web)/web-box/` | The web challenges' apps |
| `challenges/scorpius (pwn)/` | The pwn programs and the `Dockerfile` that builds them |
| `docker-compose.yml`, `edge/nginx.conf` | The containers and their ports |
| `ANSWERS.md` | Walkthroughs of every challenge. Organizers only. |
| `.env`, `.ctf/config`, `LOGINS.txt` | Passwords, the CTFd token and the logins. Made by setup, never in git. |

Both demos build their SSH boxes from this folder's Dockerfiles, and the first demo its pwn programs too, so changes to those Dockerfiles affect the demos as well.

See [docs/](../docs/) for how to run an event and how to make challenges.
