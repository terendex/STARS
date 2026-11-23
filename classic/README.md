# STARS Classic

The first orientation's 36 challenges, kept exactly as they were, as their own CTF, for a group that hasn't played them yet. Flags look like `STARS{...}`. It has the same features as 2nd Star: points that drop with each solve, its own mission clock with music, first blood, the help queue, and teams of 3. Its navbar is green, so you can tell it apart from 2nd Star (dark), the demo (purple) and SITS (blue).

It has its own CTFd, accounts, scores and ports, and runs beside the others on the same IP:

| What | Address |
|---|---|
| Classic CTFd | `http://<host>:8200` |
| Ursa Minor (Linux), and SSH into Scorpius | `ssh <star>@<host> -p 2230` |
| Orion (Web) | `http://<host>:8201` to `8206` |
| Scorpius (Pwn) | `nc <host> 9032` to `9036` (Antares: `9031`) |
| Draco (Reversing) | `ssh <star>@<host> -p 2232`, password `draco` |
| Its mission clock, for the projector | `http://localhost:8002/timer` on the CTF PC, and **Admin Panel > Mission Clock** |

```powershell
scripts\classic.ps1 setup      # first time only    (Linux: bash scripts/classic.sh setup)
scripts\classic.ps1 teams 15   # makes 15 teams of 3; logins go in classic\LOGINS.txt
scripts\classic.ps1 start      # start it
scripts\classic.ps1 stop       # stop it, keeping accounts and scores
scripts\classic.ps1 sync       # after editing a challenge.yml in classic\challenges
```

The admin password and the players' logins are in `classic\LOGINS.txt`, which stays out of git, and the walkthroughs are in `classic\ANSWERS.md`. Signing in to Classic doesn't sign you out of the other CTFs.

Classic doesn't start by itself, and first-time setup doesn't set it up. If your IP changes while it's running, it moves with 2nd Star. The folder layout is the same as [2nd Star's](../2nd-star/README.md).

See [docs/](../docs/) for how to run an event and how to make challenges.
