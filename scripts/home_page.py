"""The CTFd home pages for the real CTF ("main") and the demo ("demo"), with a
short "How to play" guide for beginners.

setup-ctfd.py uses these when it sets up a fresh CTFd. After editing them,
push the new page to a running CTFd. Run it from the folder whose .ctf/config
points at that CTFd (it reads the admin token from there and never prints it):

    docker compose run --rm --entrypoint python ctfcli scripts/home_page.py main
    docker compose -f demo/docker-compose.yml run --rm --entrypoint python ctfcli ../scripts/home_page.py demo
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
    </div>
</div>"""


def steps(scoring, sharing):
    return [
        f"Open <b>Challenges</b>. Each category is a constellation, and each challenge is one of its stars. {scoring}",
        "Click a challenge and read it. It tells you your goal. The address, login or file you need is in the same "
        "window, below the description.",
        "Find the flag. Every flag looks like <code>STARS{...}</code>.",
        "Paste the flag into the box at the bottom of the challenge and press <b>Submit</b>. Copy it exactly: each "
        "challenge allows 3 wrong tries, and typos count.",
        f"Stuck? Each challenge has hints, but they cost points, so try first. {sharing}",
    ]


START_LIST = "\n".join(
    f"            <li><b>{star}</b> in {constellation} ({skill})</li>" for star, constellation, skill in START_HERE
)

PAGES = {
    "main": page(
        "STARS CTF",
        "Log in with the account your organizer gave you, then open Challenges.",
        [("Log in", "/login", "btn-primary"), ("Challenges", "/challenges", "btn-outline-secondary")],
        steps(
            "★ Easy challenges are worth 30 points, ★★ Medium 60, and ★★★ Hard 100.",
            "Your team shares its solves, hints and wrong tries.",
        ),
        f"""        <h3>New here? Start with these</h3>
        <p>Each category has one challenge that walks you through every step:</p>
        <ul>
{START_LIST}
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
}


if __name__ == "__main__":
    import requests

    if len(sys.argv) != 2 or sys.argv[1] not in PAGES:
        sys.exit("Usage: home_page.py main|demo")
    config = configparser.ConfigParser()
    config.read(pathlib.Path.cwd() / ".ctf" / "config")
    url = config["config"]["url"].rstrip("/")
    api = requests.Session()
    api.headers.update({"Authorization": f"Token {config['config']['access_token']}",
                        "Content-Type": "application/json"})
    reply = api.get(f"{url}/api/v1/pages", timeout=20)
    reply.raise_for_status()
    index = next(row for row in reply.json()["data"] if row["route"] == "index")
    api.patch(f"{url}/api/v1/pages/{index['id']}", json={"content": PAGES[sys.argv[1]]},
              timeout=20).raise_for_status()
    print(f"Updated the home page of the {sys.argv[1]} CTFd.")
