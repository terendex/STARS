"""Makes CTFd teams and their players' accounts, since players can't register
themselves. Give it the team names:

    docker compose run --rm --entrypoint python ctfcli scripts/make-teams.py Nebula Comet Quasar Pulsar Nova

Each team gets as many players as CTFd's team size allows (3 for STARS), named
after the team: Nebula gets nebula1, nebula2 and nebula3, and nebula1 is its
captain. Run it from the folder whose .ctf/config points at the CTFd, because it
reads the admin token from there. Passwords are added to LOGINS.txt in that
folder and never printed. If any name is already taken, it changes nothing.
"""
import configparser
import datetime
import pathlib
import re
import secrets
import sys

import requests

# Common words that are easy to spell, so passwords are easy to read and type.
# Two of these and a 3-digit number allow 9 million passwords, too many to guess
# at CTFd's login page, which allows about 2 tries a second.
WORDS = """
    amber anchor apple arrow aspen autumn bamboo basil beacon berry birch bison
    breeze bright brook cactus canyon cedar cherry cider clover cobalt coral
    cotton crane daisy delta dune eagle ember falcon fern flint forest fossil
    frost garden ginger glacier granite harbor hazel heron honey island ivory
    jasmine juniper kettle koala lagoon lantern lemon lily lotus maple meadow
    melon mint moss nectar ocean olive orchid otter panda pebble pepper pine
    plum prairie quartz rabbit raven reef river robin sage salmon sierra spruce
    summit sunny thunder tiger timber topaz tulip valley velvet violet walnut
    willow winter zebra acorn badger cloud mango copper
""".split()


def new_password():
    return f"{secrets.choice(WORDS)}-{secrets.choice(WORDS)}-{100 + secrets.randbelow(900)}"


class Refused(Exception):
    pass


if len(sys.argv) < 2:
    sys.exit("Usage: make-teams.py <team name> [<team name> ...]")
names = sys.argv[1:]

config = configparser.ConfigParser()
config.read(pathlib.Path.cwd() / ".ctf" / "config")
API = config["config"]["url"].rstrip("/") + "/api/v1"
api = requests.Session()
# CTFd only accepts the token on JSON requests.
api.headers.update({"Authorization": f"Token {config['config']['access_token']}",
                    "Content-Type": "application/json"})


def call(method, path, body=None):
    reply = api.request(method, API + path, json=body, timeout=30)
    if not reply.ok:
        raise Refused(f"CTFd refused {method} {path} ({reply.status_code}): {reply.text[:300]}")
    return reply.json().get("data")


def every(path):
    """Every row of a CTFd list, including hidden and banned ones."""
    rows, page = [], 1
    while page:
        reply = api.get(API + path, params={"page": page, "view": "admin"}, timeout=30)
        reply.raise_for_status()
        rows += reply.json()["data"]
        page = reply.json()["meta"]["pagination"]["next"]
    return rows


size = int(call("GET", "/configs/team_size")["value"] or 3)
players = {}
for name in names:
    handle = re.sub(r"[^a-z0-9]", "", name.lower())
    if not handle:
        sys.exit(f"Can't make player names from {name!r}. Use letters or digits in team names.")
    players[name] = [f"{handle}{number}" for number in range(1, size + 1)]

wanted_users = [player for team in players.values() for player in team]
taken_teams = {team["name"].lower() for team in every("/teams")}
taken_users = {user["name"].lower() for user in every("/users")}
clashes = [name for name in names if name.lower() in taken_teams] + \
          [player for player in wanted_users if player in taken_users]
if len(set(wanted_users)) < len(wanted_users) or len({name.lower() for name in names}) < len(names):
    sys.exit("Two of those team names are too alike. Nothing was changed.")
if clashes:
    sys.exit(f"Already taken, so nothing was changed: {', '.join(clashes)}")

LOGINS = pathlib.Path.cwd() / "LOGINS.txt"
with LOGINS.open("a", encoding="utf-8") as logins:
    if logins.tell() == 0:
        logins.write("CTFd logins. Keep this file to yourself.\n")
    logins.write(f"\nTeams made by scripts/make-teams.py on {datetime.date.today()}. Each player logs in "
                 "with their name and password.\nThey're already on their team, so they don't need its password.\n")
    for name in names:
        made = []
        try:
            team_password = new_password()
            team = call("POST", "/teams", {"name": name, "password": team_password})
            made.append(f"/teams/{team['id']}")
            lines = ["", f"{name} (team password {team_password})"]
            for number, player in enumerate(players[name], 1):
                password = new_password()
                user = call("POST", "/users", {"name": player, "email": f"{player}@stars.invalid",
                                               "password": password})
                made.append(f"/users/{user['id']}")
                call("POST", f"/teams/{team['id']}/members", {"user_id": user["id"]})
                if number == 1:
                    call("PATCH", f"/teams/{team['id']}", {"captain_id": user["id"]})
                lines.append(f"  {player} / {password}" + ("   (captain)" if number == 1 else ""))
        except Refused as error:
            # Undo this team, so running the script again with the rest is safe.
            for path in reversed(made):
                api.delete(API + path, timeout=30)
            sys.exit(f"{error}\nUndid team {name}. Any teams listed above it were made.")
        logins.write("\n".join(lines) + "\n")
        logins.flush()
        print(f"Made team {name}: {', '.join(players[name])}")

print("Their passwords are in LOGINS.txt.")
