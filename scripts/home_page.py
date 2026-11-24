"""The CTFd home pages for the real CTF ("main"), STARS Classic ("classic"), the
demos ("demo" and "demo2") and the SITS competition ("sits"), with a short "How to play"
guide for beginners and the credit line.

setup-ctfd.py uses these when it sets up a fresh CTFd. After editing them,
push the new page to a running CTFd. Run it from the folder whose .ctf/config
points at that CTFd (it reads the admin token from there and never prints it):

    docker compose -f 2nd-star/docker-compose.yml run --rm --entrypoint python ctfcli ../scripts/home_page.py main
    docker compose -f classic/docker-compose.yml run --rm --entrypoint python ctfcli ../scripts/home_page.py classic
    docker compose -f demo/docker-compose.yml run --rm --entrypoint python ctfcli ../scripts/home_page.py demo
    docker compose -f demo2/docker-compose.yml run --rm --entrypoint python ctfcli ../scripts/home_page.py demo2
    docker compose -f sits/docker-compose.yml run --rm --entrypoint python ctfcli ../scripts/home_page.py sits
"""
import configparser
import pathlib
import sys

# Each category's walkthrough level, which talks a beginner through every step.
START_HERE = [
    ("Pherkad", "Ursa Minor", "Linux"),
    ("Betelgeuse", "Orion", "Web"),
    ("Pollux", "Gemini", "Crypto"),
    ("Sheliak", "Lyra", "Forensics"),
    ("Shaula", "Scorpius", "Pwn"),
    ("Thuban", "Draco", "Reversing"),
]

# SITS's walkthrough levels: (challenge, category).
SITS_START_HERE = [
    ("Welcome Mat", "Linux"),
    ("View Source", "Web"),
    ("Not So Secret", "Crypto"),
    ("Photo Notes", "Forensics"),
    ("Secret Menu", "Pwn"),
    ("Strings Attached", "Reversing"),
]

CREDIT = "Made by Axel Jonas C. Tangalin"


def page(heading, text, buttons, steps, extra):
    links = "\n".join(
        f'        <a class="btn {style} btn-lg m-1" href="{href}">{label}</a>' for label, href, style in buttons
    )
    items = "\n".join(f"            <li>{step}</li>" for step in steps)
    return f"""<div class="row">
    <div class="col-md-6 offset-md-3 text-center" style="padding-top: 10vh;">
        <h1 class="mb-3">{heading}</h1>
        <p class="lead">{text}</p>
{links}
    </div>
</div>
<div class="row">
    <div class="col-md-8 offset-md-2 text-start text-left" style="padding-top: 5vh; padding-bottom: 5vh;">
        <h3>How to play</h3>
        <ol>
{items}
        </ol>
{extra}
        <h3>Using the terminal</h3>
        <ul>
            <li>Some challenges need a terminal. On Windows, that's PowerShell: press the Windows key, type <code>powershell</code>, and press Enter. On a Mac, open Terminal.</li>
            <li>The first time you connect to a server, <code>ssh</code> asks whether you want to continue connecting. Type <code>yes</code>.</li>
            <li>Passwords don't appear as you type them. That's normal, so keep typing and press Enter.</li>
            <li>To copy a flag out of PowerShell, highlight it with the mouse, then right-click.</li>
            <li>If a program seems stuck, press Ctrl+C to stop it. Type <code>exit</code> to leave a server.</li>
        </ul>
        <p class="text-muted small mt-5 mb-0">{CREDIT}</p>
    </div>
</div>"""


def steps(scoring, sharing, clock=False, flag="STARS{...}",
          hints="Stuck? Each challenge has hints, but they cost points, so try first."):
    found = [
        f"Open <b>Challenges</b>. Each category is a constellation, and each challenge is one of its stars. {scoring}",
        "Click a challenge and read it. It tells you your goal. The address, login or file you need is in the same "
        "window, below the description.",
        f"Find the flag. Every flag looks like <code>{flag}</code>.",
        "Paste the flag into the box at the bottom of the challenge and press <b>Submit</b>. Copy it exactly: each "
        "challenge allows 3 wrong tries, and typos count.",
        f"{hints} {sharing}",
    ]
    if clock:
        found.insert(0, "The challenges open when your organizer starts the clock, and flag submissions "
                     "close when time is up.")
    return found


START_LIST = "\n".join(
    f"            <li><b>{star}</b> in {constellation} ({skill})</li>" for star, constellation, skill in START_HERE
)

SITS_START_LIST = "\n".join(
    f"            <li><b>{name}</b> in {category}</li>" for name, category in SITS_START_HERE
)

PAGES = {
    "main": page(
        "2nd Star",
        "Log in with the account your organizer gave you, then open Challenges.",
        [("Log in", "/login", "btn-primary"), ("Challenges", "/challenges", "btn-outline-secondary")],
        steps(
            "★ Easy challenges start at 30 points, ★★ Medium at 60, and ★★★ Hard at 100. Every time another "
            "team solves one, it loses 1, 3 or 5 points for every team that has it, so the rarer the solve, "
            "the more it's worth.",
            "Your team shares its solves, hints and wrong tries.",
            clock=True,
        ),
        f"""        <h3>New here? Start with these</h3>
        <p>Each category has one challenge that walks you through every step:</p>
        <ul>
{START_LIST}
        </ul>""",
    ),
    "classic": page(
        "STARS Classic",
        "The original STARS challenges. Log in with the account your organizer gave you, then open Challenges.",
        [("Log in", "/login", "btn-primary"), ("Challenges", "/challenges", "btn-outline-secondary")],
        steps(
            "★ Easy challenges start at 30 points, ★★ Medium at 60, and ★★★ Hard at 100. Every time another "
            "team solves one, it loses 1, 3 or 5 points for every team that has it, so the rarer the solve, "
            "the more it's worth.",
            "Your team shares its solves, hints and wrong tries.",
            clock=True,
        ),
        f"""        <h3>New here? Start with these</h3>
        <p>Each category has one challenge that walks you through every step:</p>
        <ul>
{START_LIST}
        </ul>""",
    ),
    "sits": page(
        "SITS Capture The Flag Competition 2026",
        "Log in with the account your organizer gave you, then open Challenges. You have 4 hours.",
        [("Log in", "/login", "btn-primary"), ("Challenges", "/challenges", "btn-outline-secondary")],
        steps(
            "★ Easy challenges start at 30 points, ★★ Medium at 60, and ★★★ Hard at 100. Every time another "
            "team solves one, it loses 1, 3 or 5 points for every team that has it, so the rarer the solve, "
            "the more it's worth.",
            "Your team shares its solves, hints and wrong tries. Stuck for a while? Press <b>Ask for help</b> "
            "in the corner of the challenges page and an organizer will come to you.",
            clock=True,
            flag="FLAG{...}",
        ),
        f"""        <h3>New here? Start with these</h3>
        <p>Each category has one challenge that walks you through every step:</p>
        <ul>
{SITS_START_LIST}
        </ul>""",
    ),
    "demo": page(
        "STARS CTF Demo",
        "No login needed. You're already playing as the Demo Team.",
        [("Open the challenges", "/challenges", "btn-primary")],
        steps(
            "Every challenge here is ★ Easy and worth 30 points.",
            "Everyone here plays as the same Demo Team, so solves, hints and wrong tries are shared by all.",
        ),
        "",
    ),
    "demo2": page(
        "STARS CTF Demo 2",
        "No login needed. You're already playing as the Demo Team.",
        [("Open the challenges", "/challenges", "btn-primary")],
        steps(
            "Every challenge here is ★★★ Hard, the hardest kind in STARS, and worth 100 points.",
            "Everyone here plays as the same Demo Team, so solves, hints and wrong tries are shared by all.",
            hints="Stuck? Each challenge has hints, and here they're free.",
        ),
        "",
    ),
}


if __name__ == "__main__":
    import requests

    if len(sys.argv) != 2 or sys.argv[1] not in PAGES:
        sys.exit("Usage: home_page.py main|classic|demo|demo2|sits")
    config = configparser.ConfigParser()
    config.read(pathlib.Path.cwd() / ".ctf" / "config")
    url = config["config"]["url"].rstrip("/")
    api = requests.Session()
    api.headers.update({"Authorization": f"Token {config['config']['access_token']}",
                        "Content-Type": "application/json"})
    reply = api.get(f"{url}/api/v1/pages", timeout=20)
    reply.raise_for_status()
    index = next(row for row in reply.json()["data"] if row["route"] == "index")
    # The page's title is the browser tab's name, so it follows the CTF's name.
    name = api.get(f"{url}/api/v1/configs/ctf_name", timeout=20).json()["data"]["value"]
    # "html": the pages are hand-written HTML, not markdown (which turns an
    # indented line after a blank one into a literal code block).
    api.patch(f"{url}/api/v1/pages/{index['id']}", json={"content": PAGES[sys.argv[1]], "title": name, "format": "html"},
              timeout=20).raise_for_status()
    print(f"Updated the home page of the {sys.argv[1]} CTFd.")
