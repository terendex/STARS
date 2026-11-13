"""Makes CTFd teams named with NATO call signs (Alpha, Bravo, Charlie, ...), each
with 3 player accounts under random names, since players can't register
themselves. No account belongs to anyone in particular, so on the day you can
hand any team's logins to any group. Give it how many teams to add:

    docker compose run --rm --entrypoint python ctfcli scripts/make-teams.py 15

New teams take the next call signs not in CTFd yet, so running it again adds
more teams after the last one. Players' names are an animal and a number, like
otter42, and the first player is the team's captain. Nobody needs an email.
Passwords are added to LOGINS.txt and never printed. Run it from the folder
whose .ctf/config points at the CTFd, because it reads the admin token there.
"""
import configparser
import datetime
import pathlib
import secrets
import sys

import requests

CALL_SIGNS = """
    Alpha Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliet Kilo Lima Mike
    November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey X-ray Yankee Zulu
""".split()

# Players' names: one of these and a number from 10 to 99.
ANIMALS = """
    beaver camel cobra condor coyote dingo dolphin ferret gecko gopher hawk hippo
    husky ibis impala jackal jaguar lemur leopard llama lynx magpie mantis marmot
    moose narwhal ocelot octopus orca osprey otter owl panda panther parrot
    pelican penguin puma quail rhino seal shark sloth sparrow squid swan tiger
    toucan turtle viper walrus weasel whale wolf wombat yak zebra
""".split()

# Passwords: two of these and a number from 100 to 999. They're common words
# that are easy to spell, with no animals or call signs, so a password never
# looks like a name. That allows 9 million passwords, too many to guess at
# CTFd's login page, which allows about 2 tries a second.
WORDS = """
    amber anchor anvil apple arrow aspen autumn bamboo basil beacon berry birch
    blossom breeze bright brook button cactus candle canoe canyon cedar cherry
    cider clover cobalt compass cookie coral cotton crystal daisy dune ember
    feather fern flint forest fossil frost garden ginger glacier granite harbor
    harvest hazel honey island ivory jasmine juniper kettle lagoon lantern lemon
    lily lotus magnet maple marble meadow melon mint moss nectar ocean olive
    orchid pebble pencil pepper pillow pine plum prairie quartz reef ribbon
    river rocket saddle sage spruce summit sunny thunder timber topaz tulip
    valley velvet violet walnut willow winter acorn cloud mango copper
""".split()


def new_password():
    return f"{secrets.choice(WORDS)}-{secrets.choice(WORDS)}-{100 + secrets.randbelow(900)}"


class Refused(Exception):
    pass


if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) < 1:
    sys.exit("Usage: make-teams.py <how many teams to add>")
count = int(sys.argv[1])

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
taken_teams = {team["name"].lower() for team in every("/teams")}
taken_names = {user["name"].lower() for user in every("/users")}
free = [sign for sign in CALL_SIGNS if sign.lower() not in taken_teams]
if count > len(free):
    sys.exit(f"Only {len(free)} call signs are free, so nothing was changed.")


def new_name():
    while True:
        name = f"{secrets.choice(ANIMALS)}{10 + secrets.randbelow(90)}"
        if name not in taken_names:
            taken_names.add(name)
            return name


LOGINS = pathlib.Path.cwd() / "LOGINS.txt"
with LOGINS.open("a", encoding="utf-8") as logins:
    if logins.tell() == 0:
        logins.write("CTFd logins. Keep this file to yourself.\n")
    logins.write(f"\nMade by scripts/make-teams.py on {datetime.date.today()}. Each player logs in with their "
                 "name and password.\nThey're already on their team, so they don't need its password.\n")
    for sign in free[:count]:
        made = []
        try:
            team_password = new_password()
            team_id = call("POST", "/teams", {"name": sign, "password": team_password})["id"]
            made.append(f"/teams/{team_id}")
            lines = ["", f"{sign} (team password {team_password})"]
            players = []
            for number in range(1, size + 1):
                name, password = new_name(), new_password()
                user = call("POST", "/users", {"name": name, "password": password})
                made.append(f"/users/{user['id']}")
                call("POST", f"/teams/{team_id}/members", {"user_id": user["id"]})
                if number == 1:
                    call("PATCH", f"/teams/{team_id}", {"captain_id": user["id"]})
                lines.append(f"  {name} / {password}" + ("   (captain)" if number == 1 else ""))
                players.append(name)
        except Refused as error:
            # Undo this team, so running the script again is safe.
            for path in reversed(made):
                api.delete(API + path, timeout=30)
            sys.exit(f"{error}\nUndid team {sign}. Any teams listed above it were made.")
        logins.write("\n".join(lines) + "\n")
        logins.flush()
        print(f"Made team {sign}: {', '.join(players)}")

print("Their passwords are in LOGINS.txt.")
