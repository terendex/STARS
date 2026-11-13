"""Makes CTFd teams and their players' accounts from a roster file, since
players can't register themselves:

    docker compose run --rm --entrypoint python ctfcli scripts/make-teams.py TEAMS.txt

The roster has one block per team: the team's name, then one player per line,
written "Surname, First names" or just the surname, with a blank line between
teams. Lines starting with # are ignored. The first player is the captain.

Each player logs in with their surname in lowercase, without spaces or
punctuation, so "Dela Cruz, Juan" logs in as delacruz. If two players share a
surname, give one of them a login name in brackets: "Santos, Juan [jsantos]".
Nobody needs an email.

Running it again only adds what isn't in CTFd yet: new teams, and new players
in existing teams. It checks everything first, and changes nothing if a team
would be too big or a login name is already someone else's. Passwords are
added to LOGINS.txt and never printed. Run it from the folder whose .ctf/config
points at the CTFd, because it reads the admin token from there.
"""
import configparser
import datetime
import pathlib
import re
import secrets
import sys
import unicodedata

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


def read_roster(path):
    """{team name: [player, ...]}, in the file's order."""
    teams, team = {}, None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        if not line:
            team = None
        elif team is None:
            team = line
            if team.lower() in (name.lower() for name in teams):
                sys.exit(f"{team} is in {path.name} twice. Nothing was changed.")
            teams[team] = []
        else:
            teams[team].append(line)
    return teams


def login_name(player):
    """The surname, or the name in brackets, as plain lowercase letters and digits."""
    bracket = re.search(r"\[([^\]]*)\]\s*$", player)
    name = bracket.group(1) if bracket else player.split(",")[0]
    plain = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", plain.lower())


def full_name(player):
    return re.sub(r"\s*\[[^\]]*\]\s*$", "", player)


class Refused(Exception):
    pass


if len(sys.argv) != 2:
    sys.exit("Usage: make-teams.py TEAMS.txt")
ROSTER = pathlib.Path(sys.argv[1])
if not ROSTER.is_file():
    sys.exit(f"Can't find {ROSTER}.")
roster = read_roster(ROSTER)

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


# Check everything before changing anything.
size = int(call("GET", "/configs/team_size")["value"] or 3)
teams = {team["name"].lower(): team for team in every("/teams")}
users = {user["name"].lower(): user for user in every("/users")}
problems, owners, plan = [], {}, []
for team, players in roster.items():
    found = teams.get(team.lower())
    members = set(call("GET", f"/teams/{found['id']}")["members"]) if found else set()
    new = []
    for player in players:
        login = login_name(player)
        user = users.get(login)
        if not login:
            problems.append(f"Can't make a login name from {player!r}. Add one in brackets: {player} [name]")
        elif login in owners:
            problems.append(f"{owners[login]!r} and {player!r} would both log in as {login}. "
                            f"Give one a login name in brackets, like: {player} [{login}2]")
        elif user and user["id"] not in members:
            problems.append(f"{login} is already someone else's login, so give {player!r} a login name "
                            f"in brackets, like: {player} [{login}2]")
        elif not user:
            new.append((player, login))
        owners[login] = player
    if not players and not found:
        problems.append(f"{team} has no players. Add them, or put # in front of its name.")
    if len(members) + len(new) > size:
        problems.append(f"{team} would have {len(members) + len(new)} players, but a team can have "
                        f"{size}. Split it into two teams.")
    if new:
        plan.append((team, found, new, len(members)))
if problems:
    sys.exit("Nothing was changed, because:\n- " + "\n- ".join(problems))
if not plan:
    sys.exit(f"Everyone in {ROSTER.name} is already in CTFd. Nothing was changed.")

LOGINS = pathlib.Path.cwd() / "LOGINS.txt"
with LOGINS.open("a", encoding="utf-8") as logins:
    if logins.tell() == 0:
        logins.write("CTFd logins. Keep this file to yourself.\n")
    logins.write(f"\nMade by scripts/make-teams.py on {datetime.date.today()}. Each player logs in with "
                 "their login name and password.\nThey're already on their team, so they don't need its password.\n")
    for team, found, new, already in plan:
        made = []
        try:
            if found:
                team_id = found["id"]
                lines = ["", f"Added to {team}:"]
            else:
                team_password = new_password()
                team_id = call("POST", "/teams", {"name": team, "password": team_password})["id"]
                made.append(f"/teams/{team_id}")
                lines = ["", f"{team} (team password {team_password})"]
            for number, (player, login) in enumerate(new, already + 1):
                password = new_password()
                user = call("POST", "/users", {"name": login, "password": password})
                made.append(f"/users/{user['id']}")
                call("POST", f"/teams/{team_id}/members", {"user_id": user["id"]})
                if number == 1:
                    call("PATCH", f"/teams/{team_id}", {"captain_id": user["id"]})
                lines.append(f"  {login} / {password}   {full_name(player)}" + (" (captain)" if number == 1 else ""))
        except Refused as error:
            # Undo this team's changes, so running the script again is safe.
            for path in reversed(made):
                api.delete(API + path, timeout=30)
            sys.exit(f"{error}\nUndid the changes to {team}. Any teams listed above it were done.")
        logins.write("\n".join(lines) + "\n")
        logins.flush()
        print(f"{'Added to' if found else 'Made'} {team}: {', '.join(login for _, login in new)}")

print("Their passwords are in LOGINS.txt.")
