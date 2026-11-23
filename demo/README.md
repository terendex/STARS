# STARS Demo

A small separate CTF for showing people how STARS works: 2 Easy challenges per category, 12 in all. None of them are in the real events, so it's safe to demo in front of players. Its navbar is purple. Flags look like `STARS{...}`. Keep it that way: never put a real event's challenge, flag or trick here.

**No login needed.** Anyone who opens the demo is signed in automatically as `demo1` on the **Demo Team**, so everyone shares that one team. A challenge solved by one person shows as solved for everyone, and wrong flags count against everyone's 3 tries. To require logins again, empty `STARS_DEMO_AUTOLOGIN` in `demo\docker-compose.yml` and run `scripts\demo.ps1 start`.

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

To manage it, open `http://<host>:8100/login` and sign in as admin. Signing out puts you back on the Demo Team. The admin password is in `demo\LOGINS.txt`, which stays out of git, and the walkthroughs are in `demo\ANSWERS.md`.

- **Clear it between showings:** **Admin Panel > Config > Reset** in the demo's CTFd, and reset submissions only.
- **Unlock a challenge after 3 wrong flags:** delete one of the Demo Team's wrong submissions in **Admin Panel > Submissions**.
- **Start over completely:** `docker compose -f demo\docker-compose.yml down -v`, delete `demo\.env`, `demo\.ctf\` and `demo\LOGINS.txt`, then run `scripts\demo.ps1 setup`.

The demo has no mission clock, its points don't drop, and it has no first blood or help queue. It builds its SSH boxes and pwn programs with 2nd Star's Dockerfiles, using its own levels in `demo\challenges\`. It has its own small plugin in `demo\ctfd-plugin\` for the automatic login.

See [docs/](../docs/) for how to run an event and how to make challenges.
