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
   Admin Panel > Mission Clock, and the clock counts down on every player page
   and on the projector page /timer, which can also play music. It's built on
   CTFd's own start and end times, so CTFd itself does the locking: before Start,
   players can't open the challenges, and once the clock reaches zero, nobody can
   submit a flag. Admins are never locked out, so they can still test.

   Where the clock lives, in CTFd's config table:
     start, end            CTFd's own CTF start and end (unix seconds)
     stars_timer_duration  the length chosen on the admin page, in seconds
     stars_music           "1" to play the playlist on /timer, "0" for silence
   Standby is a start time far in the future (STANDBY), which CTFd reads as
   "hasn't started yet". The same times show in Admin Panel > Config > Start
   and End Time, and changing them there works too.
"""
import os
import time

from flask import Blueprint, jsonify, render_template, request
from wtforms.validators import Optional

from CTFd.cache import clear_challenges, clear_config, clear_standings
from CTFd.forms import users
from CTFd.plugins import (
    register_admin_plugin_menu_bar,
    register_plugin_assets_directory,
    register_plugin_script,
)
from CTFd.utils import get_config, set_config
from CTFd.utils.decorators import admins_only

# 1 January 2100. Any start time this late means "waiting for the organizer".
STANDBY = 4102444800
DEFAULT_DURATION = 60 * 60
LONGEST = 7 * 24 * 60 * 60

ASSETS = "/plugins/stars/assets/"


def clock():
    """The clock's state, worked out from CTFd's start and end times."""
    now = time.time()
    start = int(get_config("start") or 0)
    end = int(get_config("end") or 0)
    duration = int(get_config("stars_timer_duration") or DEFAULT_DURATION)

    if start >= STANDBY:
        state = "standby"
    elif start and now < start:
        state = "scheduled"
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
        "music": str(get_config("stars_music", "1")) != "0",
    }


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
        save(start=now - 1, end=now + length, stars_timer_duration=length)
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
        if state["state"] in ("standby", "scheduled", "open"):
            save(start=now - 1, end=now)
        else:
            save(end=now)
    elif action == "standby":
        length = seconds(body.get("seconds"))
        values = {"start": STANDBY, "end": None}
        if length and length > 0:
            values["stars_timer_duration"] = length
        save(**values)
    elif action == "open":
        save(start=None, end=None)
    elif action == "music":
        save(stars_music="1" if body.get("on") else "0")
    else:
        return "Unknown action."
    return None


def load(app):
    users.UserBaseForm.email = users.EmailField("Email", validators=[Optional()])

    cookie = os.environ.get("STARS_SESSION_COOKIE", "").strip()
    if cookie:
        app.config["SESSION_COOKIE_NAME"] = cookie

    register_plugin_assets_directory(app, base_path=ASSETS)
    register_plugin_script(ASSETS + "timer-bar.js")
    register_admin_plugin_menu_bar("Mission Clock", "/admin/stars-timer")

    blueprint = Blueprint("stars_timer", __name__, template_folder="templates")

    @blueprint.route("/stars/timer/state")
    def timer_state():
        response = jsonify(clock())
        response.headers["Cache-Control"] = "no-store"
        return response

    @blueprint.route("/timer")
    def timer_screen():
        return render_template("stars_timer_screen.html", assets=ASSETS, ctf_name=get_config("ctf_name"))

    @blueprint.route("/admin/stars-timer")
    @admins_only
    def timer_admin():
        return render_template("stars_timer_admin.html", assets=ASSETS)

    @blueprint.route("/admin/stars-timer/action", methods=["POST"])
    @admins_only
    def timer_action():
        body = request.get_json(silent=True) or {}
        error = act(body.get("action"), body)
        if error:
            return jsonify({"success": False, "error": error, "clock": clock()}), 400
        return jsonify({"success": True, "clock": clock()})

    app.register_blueprint(blueprint)
