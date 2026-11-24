# STARS Demo 2

A second small demo CTF, a step up from the first: one ★★ Medium challenge per category, six in all, worth 60 points each. None of them are in a real event, so it's safe to demo in front of players. Its navbar is dark red. Flags look like `STARS{...}`. Keep it that way: never put a real event's challenge, flag or trick here.

It works like the [first demo](../demo/README.md):

- **No login needed.** Anyone who opens it is signed in automatically as `demo1` on the **Demo Team**, so everyone shares that one team, its solves and its 3 tries per challenge. To require logins again, empty `STARS_DEMO_AUTOLOGIN` in `demo2\docker-compose.yml` and run `scripts\demo2.ps1 start`.
- **No mission clock**, and points don't drop. No first blood or help queue.
- **Every hint is free.** In the first demo hints cost points, but CTFd won't sell a hint to a team on 0 points, so a Demo Team that's stuck on its first challenge here could never buy one.

| What | Address |
|---|---|
| CTFd | `http://<host>:8500` |
| Calvera (Ursa Minor, Linux) | `ssh calvera@<host> -p 2250`, password `neutronstar` |
| Flame Nebula (Orion, Web) | `http://<host>:8501` |
| Jellyfish (Gemini, Crypto), Lyrids (Lyra, Forensics) | downloads from CTFd |
| Fafnir (Draco, Reversing) | `ssh fafnir@<host> -p 2252`, password `draco` |
| Jabbah (Scorpius, Pwn) | `nc <host> 9051`, or `nc jabbah 9001` from the Calvera account |

```powershell
scripts\demo2.ps1 setup   # first time only (Linux: bash scripts/demo2.sh setup)
scripts\demo2.ps1 start   # start it
scripts\demo2.ps1 stop    # stop it, keeping accounts and scores (Stop STARS does this too)
scripts\demo2.ps1 sync    # after editing a challenge.yml in demo2\challenges
```

To manage it, open `http://<host>:8500/login` and sign in as admin. The admin password is in `demo2\LOGINS.txt`, which stays out of git, and the walkthroughs are in `demo2\ANSWERS.md`. Signing in here doesn't sign you out of the first demo or the real CTFs.

- **Clear it between showings:** **Admin Panel > Config > Reset**, and reset submissions only.
- **Unlock a challenge after 3 wrong flags:** delete one of the Demo Team's wrong submissions in **Admin Panel > Submissions**.
- **Start over completely:** `docker compose -f demo2\docker-compose.yml down -v`, delete `demo2\.env`, `demo2\.ctf\` and `demo2\LOGINS.txt`, then run `scripts\demo2.ps1 setup`.

## What's in this folder

| Path | What it is |
|---|---|
| `challenges/ursa-minor (linux)/ssh-box/levels/calvera.sh` | Calvera's account, its fake commands, and the checks that run when the box is built |
| `challenges/orion (web)/web-box/flame_nebula.py` | Flame Nebula's site. Its comments explain how the template injection is kept safe. |
| `challenges/gemini (crypto)/make_files.py` | Makes Jellyfish's two files, and checks they can be solved |
| `challenges/lyra (forensics)/make_files.py` | Makes Lyrids' recording, and checks every key can be heard back |
| `challenges/draco (reversing)/draco-box/levels/fafnir/` | Fafnir's program and `setup.sh` |
| `challenges/scorpius (pwn)/jabbah/` | Jabbah: the C source players download, and the flag in `src/flag.txt`. It reuses 2nd Star's Antares (a ret2win overflow), so its trick matches Antares in the real events. |
| `docker-compose.yml`, `edge/nginx.conf` | The containers and their ports |

Like the first demo, it builds its SSH boxes and its pwn program with 2nd Star's Dockerfiles, using its own levels, and it uses the first demo's plugin, from `demo\ctfd-plugin\`.

See [docs/](../docs/) for how to run an event and how to make challenges.
