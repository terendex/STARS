# Starting a new event

How to make a new CTF next to the others, for example next year's SITS, by copying one that already works. Copy the CTF closest to what you want: `sits` for a competition with plain names, `2nd-star` for a STARS-style event.

Each CTF runs on its own ports, so several can run on one PC at the same time. Every CTF needs its own block of ports, and its own name for Docker. In the examples below, `sits` is copied to `sits-2027` and given ports in the 8400s.

| Ports already used | 2nd Star | Demo | Demo 2 | Classic | SITS |
|---|---|---|---|---|---|
| CTFd | 8000 | 8100 | 8500 | 8200 | 8300 |
| Projector page (this PC only) | 8001 | none | none | 8002 | 8003 |
| SSH boxes | 2220, 2222 | 2221, 2223 | 2250, 2252 | 2230, 2232 | 2240, 2242 |
| Web | 8081-8090 | 8091-8092 | 8501 | 8201-8206 | 8301-8315 |
| Pwn | 9001-9006 | 9021-9022 | 9051 | 9031-9036 | 9041-9048 |

Avoid port 9012 on the original CTF PC: an ASUS program (Armoury Crate) uses it.

## 1. Copy the folder

Copy `sits` to `sits-2027`. Then delete these from the copy, because they belong to the old event and setup makes new ones:

- `.env`, `.ctf\` and `LOGINS.txt`
- every `host-keys\` folder (in the SSH boxes)
- any `__pycache__\` folders

## 2. Give it its own name and ports

In `sits-2027/docker-compose.yml`:

1. Change the first line, `name: sits`, to `name: sits-2027`. Docker uses this name for the event's containers and saved data, so it must be different from every other CTF's.
2. Change the CTFd ports: `"${CTF_BIND_IP}:8300:8000"` → `8400`, the projector's `"127.0.0.1:8003:8000"` → `8004`, and `STARS_PROJECTOR_URL` to match (`http://localhost:8004/timer`).
3. Change `STARS_SESSION_COOKIE` to a new name, like `sits2027_session`. Otherwise signing in to one CTF signs you out of the other.
4. Change the `edge` service's ports to the new block, for example `2260`, `2262`, `8401-8415` and `9061-9068`.
5. Update the comment at the top that lists the ports.

In `sits-2027/edge/nginx.conf`, change every `listen` port to match. The part after `set $upstream` stays the same.

## 3. Change the challenges

Edit, add and remove challenges as in [making-challenges.md](making-challenges.md). For a new event with returning players, change at least the flags, passwords and files, so old answer sheets don't work.

- Every `connection_info` needs its new port. The IP is fixed by itself later.
- If you remove a challenge that runs on a port, also remove its service from `docker-compose.yml` and its line from `edge/nginx.conf`.
- Rewrite `ANSWERS.md`. Keep the line "The commands use `<ip>`" near the top, because set-host looks for it to keep the IP in the answers up to date.
- Run `scripts\check.ps1 sits-2027`. It finds the new folder by itself.

## 4. Its name, colour and home page

1. In `scripts/setup-ctfd.py`, copy the `"sits"` entry in `PROFILES` and call it `"sits-2027"`. Change `ctf_name`, `ctf_description` and `theme_color` (the navbar colour, so organizers can tell the CTFs apart), and change `"home": PAGES["sits"]` to `PAGES["sits-2027"]`.
2. In `scripts/home_page.py`, copy the `"sits"` page in `PAGES` and call it `"sits-2027"`. Change the heading, the welcome text and the time limit, and update its "Start here" list (`SITS_START_HERE`) if those challenges changed. `CREDIT` at the top is the "Made by" line on the home pages.

Git already ignores `.env`, `.ctf\`, `LOGINS.txt` and `host-keys\` in every folder, so the new event's passwords stay out of the repository.

## 5. Its start, stop and sync commands

1. Copy `scripts/sits.ps1` to `scripts/sits-2027.ps1`, and `scripts/sits.sh` to `scripts/sits-2027.sh`. In each, replace the folder name (`'sits'` → `'sits-2027'`), the port in the "is on" message, and `setup-ctfd.py sits` → `setup-ctfd.py sits-2027`.
2. Add it to the list of CTFs that follow the IP. In `scripts/set-host.ps1`, add a line to `$sides`:
   ```powershell
   @{ Dir = (Join-Path $root 'sits-2027'); Name = 'SITS 2027'; Port = 8400 }
   ```
   In `scripts/set-host.sh`, add `"sits-2027:8400"` to `SIDES`.
3. In `scripts/stop-stars.ps1`, add it to the list, so **Stop STARS** stops it too.
4. Optional: a desktop button. Copy `scripts/start-sits.ps1` to `scripts/start-sits-2027.ps1` and change the script name, ports and wording. Then add it to the list in `scripts/install-shortcuts.ps1` and run that script.

## 6. Set it up and test it

```powershell
scripts\sits-2027.ps1 setup       # makes .env, the admin, and installs the challenges
scripts\sits-2027.ps1 teams 15    # 15 teams of 3, logins in sits-2027\LOGINS.txt
```

Then play an Easy challenge from each category on another laptop, and check the projector page and the help queue. On Linux, open the new ports in the firewall (see [running-an-event.md](running-an-event.md#linux)).

## Retiring an old event

You don't have to delete an old event. A stopped CTF uses only disk space. To remove one for good:

1. In its CTFd, **Admin Panel > Config > Backup** to keep the results.
2. In its folder, run `docker compose down -v`. This deletes its accounts, scores and containers.
3. Remove it from `set-host.ps1`, `set-host.sh`, `stop-stars.ps1` and `install-shortcuts.ps1`, delete its scripts and its entries in `setup-ctfd.py` and `home_page.py`, then delete the folder.

## Next year's main event

To replace 2nd Star with a new main event but keep the old one playable, do what was done for STARS Classic: copy `2nd-star` to a new folder as above, and give the copy its own name and ports. Or edit `2nd-star` in place if you don't need the old challenges anymore. Its name on the CTFd pages is `ctf_name` in the `"main"` entry of `scripts/setup-ctfd.py` (for new installs). On a running CTFd, change it in **Admin Panel > Config > General**.
