"""One-time setup for a fresh CTFd: the real CTF ("main"), STARS Classic
("classic"), the demos ("demo" and "demo2") or the SITS competition ("sits").

scripts/setup.ps1 and setup.sh run this for the real CTF, and demo.ps1 and
demo.sh run it for the demo. Each starts CTFd on this PC only first, because the
first visitor to /setup becomes admin. It runs inside the ctfcli container, from
the CTF's folder, where it writes .ctf/config (2nd-star/, classic/, demo/ or
sits/):

    python ../scripts/setup-ctfd.py main
    python ../scripts/setup-ctfd.py classic
    python ../scripts/setup-ctfd.py demo
    python ../scripts/setup-ctfd.py sits

The admin is called "admin" with a new random password, unless the environment
variables STARS_ADMIN_NAME and STARS_ADMIN_PASSWORD say otherwise (sits.ps1
passes the real CTF's admin, so all the CTFs share one admin login).

It finishes CTFd's setup wizard with the event's rules, uploads the STARS logo,
makes an API token for ctfcli, and writes .ctf/config listing every challenge.
Every password goes into LOGINS.txt next to it, and none are printed.
"""
import datetime
import os
import pathlib
import re
import secrets
import sys

import requests

# The home pages, with their "How to play" guide. Python puts this script's
# folder on the import path, so scripts/home_page.py is found.
from home_page import PAGES

REPO = pathlib.Path(__file__).resolve().parent.parent
ROOT = pathlib.Path.cwd()
URL = "http://ctfd:8000"
CONFIG = ROOT / ".ctf" / "config"
LOGINS = ROOT / "LOGINS.txt"


PROFILES = {
    "main": {
        "ctf_name": "2nd Star",
        "ctf_description": "56 challenges in six categories",
        "theme_color": None,
        "home": PAGES["main"],
        "configs": {"team_creation": "false", "team_disbanding": "disabled"},
        "demo_team": False,
    },
    "classic": {
        "ctf_name": "STARS Classic",
        "ctf_description": "The original STARS challenges, 6 per category",
        # Green, so Classic is never mistaken for the real CTF (dark) or the demo (purple).
        "theme_color": "#0b7a5a",
        "home": PAGES["classic"],
        "configs": {"team_creation": "false", "team_disbanding": "disabled"},
        "demo_team": False,
    },
    "sits": {
        "ctf_name": "SITS Capture The Flag Competition 2026",
        "ctf_description": "A 4-hour capture the flag competition. Made by Axel Jonas C. Tangalin.",
        # Blue, so SITS is never mistaken for 2nd Star (dark), Classic (green)
        # or the demo (purple).
        "theme_color": "#1f5fa8",
        "home": PAGES["sits"],
        "configs": {"team_creation": "false", "team_disbanding": "disabled"},
        "demo_team": False,
        # Not STARS-branded, so CTFd shows the name instead of the STARS logo.
        "logo": False,
        "email_domain": "sits.invalid",
    },
    "demo": {
        "ctf_name": "STARS Demo",
        "ctf_description": "A demo of the STARS CTF.",
        # Purple, so the demo is never mistaken for the real CTF.
        "theme_color": "#6f42c1",
        "home": PAGES["demo"],
        # Name changes are off because everyone shares the demo1 account
        # (see demo/ctfd-plugin).
        "configs": {"team_creation": "false", "team_disbanding": "disabled", "name_changes": "false"},
        "demo_team": True,
    },
    "demo2": {
        "ctf_name": "STARS Demo 2",
        "ctf_description": "A demo of ★★ Medium STARS challenges, one per category.",
        # Dark red, so the 2nd demo is never mistaken for the first (purple) or a real CTF.
        "theme_color": "#9b2c2c",
        "home": PAGES["demo2"],
        # Name changes are off because everyone shares the demo1 account.
        "configs": {"team_creation": "false", "team_disbanding": "disabled", "name_changes": "false"},
        "demo_team": True,
    },
}


def find(pattern, html, what):
    match = re.search(pattern, html)
    if not match:
        sys.exit(f"Couldn't find the {what} on CTFd's page. Has the CTFd version changed?")
    return match.group(1)


if len(sys.argv) != 2 or sys.argv[1] not in PROFILES:
    sys.exit("Usage: setup-ctfd.py main|classic|demo|demo2|sits")
profile = PROFILES[sys.argv[1]]

browser = requests.Session()
page = browser.get(f"{URL}/setup", timeout=30)
if not page.url.endswith("/setup"):
    if CONFIG.exists():
        print("CTFd is already set up.")
        sys.exit(0)
    sys.exit(f"CTFd is already set up, but {CONFIG} is missing. Make a token in CTFd "
             "(Settings > Access Tokens) and run ctfcli init, or wipe CTFd and set it up again.")

# The setup wizard: teams of 3, accounts made by the admin, and scores and
# other teams visible to the admin only.
admin_name = os.environ.get("STARS_ADMIN_NAME", "").strip() or "admin"
admin_password = os.environ.get("STARS_ADMIN_PASSWORD", "").strip() or secrets.token_urlsafe(12)
form = {
    "nonce": find(r'name="nonce"[^>]*value="([^"]+)"', page.text, "setup form's nonce"),
    "ctf_name": profile["ctf_name"],
    "ctf_description": profile["ctf_description"],
    "user_mode": "teams",
    "team_size": "3",
    "name": admin_name,
    "email": f"admin@{profile.get('email_domain', 'stars.invalid')}",
    "password": admin_password,
    "challenge_visibility": "private",
    "account_visibility": "admins",
    "score_visibility": "admins",
    "registration_visibility": "private",
    "verify_emails": "false",
    "social_shares": "false",
}
if profile["theme_color"]:
    form["theme_color"] = profile["theme_color"]
branding = REPO / "branding"
files = {}
if profile.get("logo", True):
    files = {
        "ctf_logo": ("logo.png", (branding / "logo.png").read_bytes(), "image/png"),
        "ctf_small_icon": ("favicon.png", (branding / "favicon.png").read_bytes(), "image/png"),
    }
browser.post(f"{URL}/setup", data=form, files=files or None, timeout=60).raise_for_status()
if browser.get(f"{URL}/admin/statistics", timeout=30, allow_redirects=False).status_code != 200:
    sys.exit("CTFd's setup wizard didn't finish.")

# An API token for ctfcli, valid for a year.
csrf = find(r"csrfNonce['\"]?\s*:\s*['\"]([^'\"]+)", browser.get(f"{URL}/settings", timeout=30).text, "CSRF token")
expires = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()
reply = browser.post(f"{URL}/api/v1/tokens", timeout=30, headers={"CSRF-Token": csrf},
                     json={"expiration": expires, "description": "ctfcli"})
reply.raise_for_status()
token = reply.json()["data"]["value"]

challenges = sorted(
    path.parent.relative_to(ROOT).as_posix()
    for path in (ROOT / "challenges").glob("*/*/challenge.yml")
    if path.parent.name != "_template"
)
CONFIG.parent.mkdir(exist_ok=True)
CONFIG.write_text(
    f"[config]\nurl = {URL}\naccess_token = {token}\n\n[challenges]\n"
    + "".join(f"{path} = {path}\n" for path in challenges),
    encoding="utf-8",
)

api = requests.Session()
api.headers.update({"Authorization": f"Token {token}", "Content-Type": "application/json"})


def call(method, path, body=None):
    reply = api.request(method, f"{URL}/api/v1{path}", json=body, timeout=30)
    reply.raise_for_status()
    return reply.json().get("data")


# Settings the wizard doesn't cover, and the home page.
call("PATCH", "/configs", profile["configs"])
index = next(page for page in call("GET", "/pages") if page["route"] == "index")
# "html", not CTFd's default "markdown": the home pages are hand-written HTML,
# and markdown turns an indented line after a blank one into a literal code block.
call("PATCH", f"/pages/{index['id']}", {"content": profile["home"], "format": "html"})

lines = [
    f"{profile['ctf_name']} CTFd logins. Keep this file to yourself.",
    f"Made by scripts/setup-ctfd.py on {datetime.date.today()}. You can change any of these in CTFd.",
    "",
    "Admin",
    f"  {admin_name} / {admin_password}",
]

# The demo's one team, which every visitor plays as.
if profile["demo_team"]:
    team_password = secrets.token_urlsafe(9)
    team = call("POST", "/teams", {"name": "Demo Team", "password": team_password})
    lines += ["", f"Demo Team (team password {team_password})"]
    for number in range(1, 4):
        password = secrets.token_urlsafe(9)
        user = call("POST", "/users", {"name": f"demo{number}", "email": f"demo{number}@stars.invalid",
                                       "password": password})
        call("POST", f"/teams/{team['id']}/members", {"user_id": user["id"]})
        if number == 1:
            call("PATCH", f"/teams/{team['id']}", {"captain_id": user["id"]})
        lines.append(f"  demo{number} / {password}")

LOGINS.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Set up {profile['ctf_name']} with {len(challenges)} challenges to install. "
      f"Logins are in {LOGINS.relative_to(REPO).as_posix()}.")
