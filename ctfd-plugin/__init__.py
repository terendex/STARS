"""Changes to the real CTF's CTFd (and STARS Classic's, which mounts this folder too).

1. Accounts don't need an email. Players sign in with their name, they can't
   register themselves, and CTFd here sends no mail, so an email would never be
   used. CTFd itself accepts accounts without one, but its admin panel's Create
   User and Edit User forms insist on it. This makes the email box in those
   forms optional: leave it empty, or fill it in if you like.

2. Its own login cookie name, when STARS_SESSION_COOKIE is set. Browsers share
   cookies between ports on the same address, so STARS Classic on :8200 sets it,
   or signing in there would sign you out of the real CTF on :8000.

3. The mission clock. The admin sets a length and presses Start on
   Admin Panel > Mission Clock, and the countdown shows there and on the
   projector page /timer. The music plays on one of them, chosen on the admin
   page, so it never plays twice. Players don't see a
   countdown: assets/clock-watch.js only reloads their challenges page when the
   clock starts or ends. It's built on CTFd's own start and end times, so CTFd
   itself does the locking: before Start, players can't open the challenges, and
   once the clock reaches zero, nobody can submit a flag. Admins are never locked
   out, so they can still test.

   STARS_PROJECTOR_URL is the projector page's address on the CTF PC, which the
   admin page links to (see docker-compose.yml).

   Where the clock lives, in CTFd's config table:
     start, end            CTFd's own CTF start and end (unix seconds)
     stars_timer_duration  the length chosen on the admin page, in seconds
     stars_music           where the playlist plays: "admin" (the Mission Clock
                           page), "projector" (/timer) or "0" for silence
     paused                CTFd's own pause, on during a scoreboard break. It
                           stops players submitting; the projector shows scores.
     stars_timer_left      seconds banked on the clock while paused, put back on
                           the end time when the break is resumed, so it's free
     stars_marks_done      how many hourly breaks have started, so each hour
                           mark only triggers one
   Standby is a start time far in the future (STANDBY), which CTFd reads as
   "hasn't started yet". The same times show in Admin Panel > Config > Start
   and End Time, and changing them there works too.

4. Scoreboard breaks. Every hour of play the clock pauses itself (advance()),
   players can't submit (CTFd's own pause), and the projector shows the team and
   player standings side by side until an admin presses Resume. See /stars/
   standings and the "pause"/"resume" actions.

5. First bloods and the help queue: see extras.py.
"""
import os
import time

from flask import Blueprint, jsonify, render_template, request
from wtforms.validators import Optional

from CTFd.cache import clear_challenges, clear_config, clear_standings
from CTFd.forms import users
from CTFd.plugins import (
    register_admin_plugin_menu_bar,
    register_admin_plugin_script,
    register_plugin_assets_directory,
    register_plugin_script,
)
from CTFd.utils import get_config, set_config
from CTFd.utils.decorators import admins_only
from CTFd.utils.scores import get_team_standings, get_user_standings

# 1 January 2100. Any start time this late means "waiting for the organizer".
STANDBY = 4102444800
DEFAULT_DURATION = 60 * 60
LONGEST = 7 * 24 * 60 * 60
# A scoreboard break pauses the clock automatically at each hour of play.
INTERMISSION_EVERY = 60 * 60
STANDINGS_SHOWN = 15

ASSETS = "/plugins/stars/assets/"


def clock():
    """The clock's state, worked out from CTFd's start and end times."""
    now = time.time()
    start = int(get_config("start") or 0)
    end = int(get_config("end") or 0)
    duration = int(get_config("stars_timer_duration") or DEFAULT_DURATION)
    paused = bool(get_config("paused"))
    left = int(get_config("stars_timer_left") or 0)

    if start >= STANDBY:
        state = "standby"
    elif start and now < start:
        state = "scheduled"
    elif paused:
        # A scoreboard break: the countdown is frozen and players can't submit.
        state = "intermission"
    elif end and now >= end:
        state = "ended"
    elif end:
        state = "running"
    else:
        state = "open"

    return {
        "now": now,
        "state": state,
        "start": start if start and start < STANDBY else None,
        "end": end or None,
        "duration": duration,
        # Seconds banked on the clock while it's paused, so the break is free.
        "left": left if state == "intermission" else None,
        "music": music_mode(),
    }


def advance():
    """Start a scoreboard break at each hour of play. Called on every clock
    poll; it only writes when a new hour mark is first reached, so the projector
    (or any page) polling the state is what trips it. Pausing banks the time
    left and turns on CTFd's own pause, which stops players submitting."""
    now = int(time.time())
    start = int(get_config("start") or 0)
    end = int(get_config("end") or 0)
    duration = int(get_config("stars_timer_duration") or DEFAULT_DURATION)
    if get_config("paused") or not end or start >= STANDBY or now < start or now >= end:
        return
    elapsed = duration - (end - now)
    mark = int(get_config("stars_marks_done") or 0) + 1
    # Never break on the mark that would land on the finish itself.
    if INTERMISSION_EVERY * mark < duration and elapsed >= INTERMISSION_EVERY * mark:
        save(paused=True, stars_timer_left=end - now, stars_marks_done=mark)


def music_mode():
    """Where the music plays: "admin", "projector", or "0" for nowhere. Older
    installs stored "1" for on, which meant the projector page."""
    mode = str(get_config("stars_music", "admin"))
    return {"1": "projector"}.get(mode, mode if mode in ("admin", "projector") else "0")


def save(**values):
    for key, value in values.items():
        set_config(key, "" if value is None else str(value))
    # The same clean-up CTFd's own config API does after a change.
    clear_config()
    clear_standings()
    clear_challenges()


def seconds(value):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if 0 < abs(number) <= LONGEST else None


def act(action, body):
    """Carries out one button from the admin page. Returns an error, or None."""
    now = int(time.time())
    state = clock()

    if action in ("start", "restart"):
        length = seconds(body.get("seconds"))
        if not length or length < 0:
            return "Choose a length between 1 second and 7 days."
        # A second in the past, because CTFd counts the CTF as started only
        # once the current time is after the start time.
        save(start=now - 1, end=now + length, stars_timer_duration=length,
             paused=False, stars_timer_left=None, stars_marks_done=0)
    elif action == "pause":
        # Begin a scoreboard break: freeze the clock and stop submissions.
        if state["state"] == "running":
            save(paused=True, stars_timer_left=state["end"] - now)
        elif state["state"] == "open":
            save(paused=True, stars_timer_left=None)
        elif state["state"] != "intermission":
            return "Start the clock before showing scores."
    elif action == "resume":
        if state["state"] != "intermission":
            return "The clock isn't paused."
        left = int(get_config("stars_timer_left") or 0)
        # Push the end out by however long the break ran, so no time is lost.
        values = {"paused": False, "stars_timer_left": None}
        if left > 0:
            values["end"] = now + left
        save(**values)
    elif action == "add":
        change = seconds(body.get("seconds"))
        if not change:
            return "Choose how much time to add or take away."
        if state["state"] == "running":
            save(end=max(now, state["end"] + change))
        elif state["state"] == "ended" and change > 0:
            # Reopens a finished clock for that much longer.
            save(end=now + change)
        else:
            return "The clock isn't running."
    elif action == "end":
        clear = {"paused": False, "stars_timer_left": None}
        if state["state"] in ("standby", "scheduled", "open"):
            save(start=now - 1, end=now, **clear)
        else:
            save(end=now, **clear)
    elif action == "standby":
        length = seconds(body.get("seconds"))
        values = {"start": STANDBY, "end": None, "paused": False,
                  "stars_timer_left": None, "stars_marks_done": 0}
        if length and length > 0:
            values["stars_timer_duration"] = length
        save(**values)
    elif action == "open":
        save(start=None, end=None, paused=False, stars_timer_left=None, stars_marks_done=0)
    elif action == "music":
        mode = body.get("mode")
        if mode not in ("admin", "projector", "0"):
            return "Music has to be admin, projector or 0."
        save(stars_music=mode)
    else:
        return "Unknown action."
    return None


def load(app):
    users.UserBaseForm.email = users.EmailField("Email", validators=[Optional()])

    cookie = os.environ.get("STARS_SESSION_COOKIE", "").strip()
    if cookie:
        app.config["SESSION_COOKIE_NAME"] = cookie

    register_plugin_assets_directory(app, base_path=ASSETS)
    register_plugin_script(ASSETS + "clock-watch.js")
    register_plugin_script(ASSETS + "help.js")
    register_admin_plugin_script(ASSETS + "admin-extras.js")
    register_admin_plugin_menu_bar("Mission Clock", "/admin/stars-timer")
    register_admin_plugin_menu_bar("Help Queue", "/admin/stars-help")
    register_admin_plugin_menu_bar("Score Matrix", "/admin/stars-matrix")

    blueprint = Blueprint("stars_timer", __name__, template_folder="templates")

    @blueprint.route("/stars/timer/state")
    def timer_state():
        advance()  # start a scoreboard break if an hour mark has arrived
        response = jsonify(clock())
        response.headers["Cache-Control"] = "no-store"
        return response

    @blueprint.route("/stars/standings")
    def standings():
        # Served only while a break is on, so the scoreboard (hidden from
        # players the rest of the time) is shown on the projector just for the
        # intermission. Hidden and banned teams are left out by get_*_standings.
        if clock()["state"] != "intermission":
            response = jsonify({"intermission": False})
            response.headers["Cache-Control"] = "no-store"
            return response

        def rows(standing):
            return [{"name": row.name, "score": int(row.score or 0)} for row in standing]

        teams = rows(get_team_standings(count=STANDINGS_SHOWN)) if get_config("user_mode") == "teams" else []
        users = rows(get_user_standings(count=STANDINGS_SHOWN))
        response = jsonify({"intermission": True, "teams": teams, "users": users})
        response.headers["Cache-Control"] = "no-store"
        return response

    @blueprint.route("/timer")
    def timer_screen():
        return render_template("stars_timer_screen.html", assets=ASSETS, ctf_name=get_config("ctf_name"))

    @blueprint.route("/admin/stars-timer")
    @admins_only
    def timer_admin():
        projector = os.environ.get("STARS_PROJECTOR_URL", "").strip()
        # The same admin page on this PC's localhost address, where Spotify can
        # play whole songs (see docker-compose.yml).
        local_admin = projector[: -len("/timer")] + "/admin/stars-timer" if projector.endswith("/timer") else ""
        return render_template("stars_timer_admin.html", assets=ASSETS, projector=projector, local_admin=local_admin)

    @blueprint.route("/admin/stars-timer/action", methods=["POST"])
    @admins_only
    def timer_action():
        body = request.get_json(silent=True) or {}
        error = act(body.get("action"), body)
        if error:
            return jsonify({"success": False, "error": error, "clock": clock()}), 400
        return jsonify({"success": True, "clock": clock()})

    app.register_blueprint(blueprint)

    # First bloods and the help queue (extras.py).
    from .extras import register
    register(app, ASSETS)
