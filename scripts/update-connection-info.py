"""Copies each challenge's connection_info from its challenge.yml into CTFd.

set-host.ps1 runs this after the IP changes. Unlike `ctf challenge sync`, it
changes nothing else, so it's safe during an event. It reads the admin token
from .ctf/config and never prints it.

    docker compose run --rm --entrypoint python ctfcli scripts/update-connection-info.py

Pass a folder to update a different CTFd from its own .ctf/config and
challenges, as scripts/demo.ps1 does for the demo:

    python ../scripts/update-connection-info.py .
"""
import configparser
import pathlib
import sys

import requests
import yaml

DEFAULT_ROOT = pathlib.Path(__file__).resolve().parent.parent
ROOT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_ROOT
LABEL = "" if ROOT == DEFAULT_ROOT else f" ({ROOT.name})"

config = configparser.ConfigParser()
config.read(ROOT / ".ctf" / "config")
url = config["config"]["url"].rstrip("/")
session = requests.Session()
session.headers.update({"Authorization": f"Token {config['config']['access_token']}",
                        "Content-Type": "application/json"})

wanted = {}
for path in (ROOT / "challenges").glob("*/*/challenge.yml"):
    if path.parent.name != "_template":
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        wanted[data["name"]] = data.get("connection_info")

reply = session.get(f"{url}/api/v1/challenges?view=admin", timeout=20)
reply.raise_for_status()
changed = 0
for row in reply.json()["data"]:
    if row["name"] not in wanted:
        continue
    detail = session.get(f"{url}/api/v1/challenges/{row['id']}?view=admin", timeout=20)
    detail.raise_for_status()
    if detail.json()["data"]["connection_info"] != wanted[row["name"]]:
        session.patch(f"{url}/api/v1/challenges/{row['id']}", timeout=20,
                      json={"connection_info": wanted[row["name"]]}).raise_for_status()
        changed += 1
print(f"Updated the address on {changed} challenge(s) in CTFd{LABEL}.")
