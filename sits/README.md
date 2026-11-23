# SITS Capture The Flag Competition 2026

A separate, casual-themed 4-hour competition made by Axel Jonas C. Tangalin, with **83 challenges**. Flags look like `FLAG{...}`. Its challenges remix STARS's with new passwords, keys, files and flags, so players who did the orientations still have something to solve. It's aimed at beginners: every challenge was played by following only its description and hints. Its navbar is blue.

| Category | Challenges | Where |
|---|---|---|
| Linux | 15 (6 Easy, 6 Medium, 3 Hard) | `ssh <account>@<host> -p 2240` |
| Web | 15 | `http://<host>:8301` to `8315` |
| Crypto | 15 | downloads |
| Forensics | 15 | downloads |
| Reversing | 15 | `ssh <account>@<host> -p 2242`, password `reverse` |
| Pwn | 8 (5 Easy, 2 Medium, 1 Hard) | `nc <host> 9041` to `9048`, or SSH gate accounts on 2240 (password `pwnit`) |

CTFd is on `http://<host>:8300`, and the projector page is `http://localhost:8003/timer` on the CTF PC. It has the same features as 2nd Star: points that drop with each solve, the mission clock with music, first blood, the help queue, hidden scores and teams of 3. Its admin is the same as 2nd Star's.

```powershell
scripts\sits.ps1 setup      # first time only: the admin and the challenges
scripts\sits.ps1 teams 15   # makes 15 teams of 3; logins go in sits\LOGINS.txt
scripts\sits.ps1 start      # or the Start SITS CTF button
scripts\sits.ps1 stop       # or Stop STARS; keeps accounts and scores
scripts\sits.ps1 sync       # after editing a challenge.yml in sits\challenges
```

On Linux, use `bash scripts/sits.sh` with the same words, and open ports 8300, 8301-8315, 9041-9048, 2240 and 2242 in the firewall.

## What's in this folder

| Path | What it is |
|---|---|
| `challenges/<category>/<name>/` | One folder per challenge, with its `challenge.yml` |
| `challenges/linux/linux-box/` | The Linux SSH box. Its levels are in `levels/`, numbered in order. `16-pwn-gates.sh` makes the pwn gate accounts. |
| `challenges/linux/doorbell/` | Knock Knock's hidden server, only reachable from the SSH box |
| `challenges/reversing/rev-box/` | The reversing SSH box. Its levels are in `levels/`. |
| `challenges/web/web-box/` | The web challenges' apps |
| `challenges/crypto/make_files.py`, `challenges/forensics/make_files.py` | Make the downloads, and check each one can be solved |
| `challenges/pwn/` | The pwn programs: C source in each `<name>/dist/`, the flag in `<name>/src/flag.txt` |
| `ANSWERS.md` | A step-by-step walkthrough of all 83 challenges, with the outputs a player sees. Organizers only. |

The Pwn programs are the 8 from Scorpius, unchanged except for their flags, so their menus still mention stars. Return to Sender needs raw bytes, so it has no SSH gate: players use `nc` from a Linux challenge account, where `printf` builds the bytes.

See [docs/](../docs/) for how to run an event and how to make challenges.
