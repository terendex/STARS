"""First bloods and the help queue, for the real CTF and STARS Classic.

First blood: the first solve of each challenge by a team that isn't hidden or
banned (or a user, in users mode), so admins and test teams never count. The
projector page announces new ones, and Admin Panel > Statistics lists them all
with the player who solved it.

Help queue: players press Ask for help on the challenges page, and admins see
the requests on Admin Panel > Help Queue, oldest first. Each team has at most
one open request; asking again updates it. Requests live in the stars_help
table, which this creates the first time CTFd starts with it. CTFd's own Reset
doesn't clear it; the Help Queue page's Clear finished button does.
"""
import calendar
import time

from flask import Blueprint, jsonify, render_template, request

from CTFd.models import Challenges, Solves, Teams, Users, db
from CTFd.utils import get_config
from CTFd.utils.decorators import admins_only, authed_only
from CTFd.utils.user import get_current_team, get_current_user

OPEN = ("open", "coming")
LONGEST_MESSAGE = 300


class StarsHelp(db.Model):
    __tablename__ = "stars_help"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    challenge_id = db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text, default="")
    # open: waiting. coming: an organizer is on the way. done, cancelled: over.
    status = db.Column(db.String(16), default="open")
    created = db.Column(db.Integer)
    updated = db.Column(db.Integer)


def teams_mode():
    return get_config("user_mode") == "teams"


def unix(moment):
    return calendar.timegm(moment.utctimetuple()) if moment else None


def first_bloods():
    """Each challenge's first solve by a visible account, oldest first."""
    Account = Teams if teams_mode() else Users
    owner = Solves.team_id if teams_mode() else Solves.user_id
    rows = (
        db.session.query(Solves, Account, Challenges)
        .join(Account, owner == Account.id)
        .join(Challenges, Solves.challenge_id == Challenges.id)
        .filter(Account.hidden.is_(False), Account.banned.is_(False))
        .order_by(Solves.date.asc(), Solves.id.asc())
        .all()
    )
    seen, found = set(), []
    for solve, account, challenge in rows:
        if challenge.id in seen:
            continue
        seen.add(challenge.id)
        found.append({
            "id": solve.id,
            "at": unix(solve.date),
            "challenge": challenge.name,
            "category": challenge.category,
            "team": account.name,
            "player": solve.user.name if solve.user else account.name,
        })
    return found


def describe(row):
    challenge = Challenges.query.filter_by(id=row.challenge_id).first() if row.challenge_id else None
    team = Teams.query.filter_by(id=row.team_id).first() if row.team_id else None
    user = Users.query.filter_by(id=row.user_id).first() if row.user_id else None
    return {
        "id": row.id,
        "status": row.status,
        "created": row.created,
        "updated": row.updated,
        "message": row.message or "",
        "challenge": f"{challenge.name} · {challenge.category}" if challenge else "",
        "challenge_id": row.challenge_id,
        "team": team.name if team else "",
        "player": user.name if user else "",
    }


def my_request():
    """The current team's (or user's) open request, if any."""
    query = StarsHelp.query.filter(StarsHelp.status.in_(OPEN))
    if teams_mode():
        team = get_current_team()
        if not team:
            return None
        query = query.filter_by(team_id=team.id)
    else:
        query = query.filter_by(user_id=get_current_user().id)
    return query.first()


def queue_position(row):
    waiting = StarsHelp.query.filter_by(status="open").order_by(StarsHelp.created.asc(), StarsHelp.id.asc()).all()
    for number, other in enumerate(waiting, 1):
        if other.id == row.id:
            return number
    return None


def register(app, assets):
    StarsHelp.__table__.create(bind=db.engine, checkfirst=True)
    blueprint = Blueprint("stars_extras", __name__, template_folder="templates")

    # --- First blood ---------------------------------------------------------
    @blueprint.route("/stars/first-bloods")
    def public_first_bloods():
        # For the projector page: team and challenge only, never players' names.
        found = [{key: blood[key] for key in ("id", "at", "challenge", "category", "team")} for blood in first_bloods()]
        response = jsonify({"first_bloods": found})
        response.headers["Cache-Control"] = "no-store"
        return response

    @blueprint.route("/admin/stars/first-bloods")
    @admins_only
    def admin_first_bloods():
        start = int(get_config("start") or 0)
        found = first_bloods()
        for blood in found:
            blood["after_start"] = blood["at"] - start if start and blood["at"] and blood["at"] >= start else None
        return jsonify({"first_bloods": found, "challenges": Challenges.query.filter_by(state="visible").count()})

    # --- Help queue: players --------------------------------------------------
    @blueprint.route("/stars/help", methods=["GET"])
    @authed_only
    def help_mine():
        row = my_request()
        if not row:
            return jsonify({"request": None})
        found = describe(row)
        found["position"] = queue_position(row) if row.status == "open" else None
        return jsonify({"request": found})

    @blueprint.route("/stars/help", methods=["POST"])
    @authed_only
    def help_ask():
        user = get_current_user()
        team = get_current_team() if teams_mode() else None
        if teams_mode() and not team:
            return jsonify({"success": False, "error": "Join a team first."}), 403
        body = request.get_json(silent=True) or {}
        try:
            challenge_id = int(body.get("challenge_id")) if body.get("challenge_id") not in (None, "") else None
        except (TypeError, ValueError):
            challenge_id = None
        if challenge_id is not None and not Challenges.query.filter_by(id=challenge_id, state="visible").first():
            challenge_id = None
        message = str(body.get("message") or "").strip()[:LONGEST_MESSAGE]
        now = int(time.time())

        row = my_request()
        if row:
            # Asking again updates the team's request instead of adding another.
            row.challenge_id, row.message, row.user_id, row.updated = challenge_id, message, user.id, now
        else:
            row = StarsHelp(team_id=team.id if team else None, user_id=user.id, challenge_id=challenge_id,
                            message=message, status="open", created=now, updated=now)
            db.session.add(row)
        db.session.commit()
        found = describe(row)
        found["position"] = queue_position(row) if row.status == "open" else None
        return jsonify({"success": True, "request": found})

    @blueprint.route("/stars/help/cancel", methods=["POST"])
    @authed_only
    def help_cancel():
        row = my_request()
        if row:
            row.status, row.updated = "cancelled", int(time.time())
            db.session.commit()
        return jsonify({"success": True})

    # --- Help queue: admins -------------------------------------------------
    @blueprint.route("/admin/stars-help")
    @admins_only
    def help_queue():
        return render_template("stars_help_admin.html", assets=assets)

    @blueprint.route("/admin/stars-help/list")
    @admins_only
    def help_list():
        active = (StarsHelp.query.filter(StarsHelp.status.in_(OPEN))
                  .order_by(StarsHelp.created.asc(), StarsHelp.id.asc()).all())
        recent = (StarsHelp.query.filter(StarsHelp.status.in_(("done", "cancelled")))
                  .order_by(StarsHelp.updated.desc()).limit(15).all())
        return jsonify({
            "now": time.time(),
            "waiting": sum(1 for row in active if row.status == "open"),
            "active": [describe(row) for row in active],
            "recent": [describe(row) for row in recent],
        })

    @blueprint.route("/admin/stars-help/<int:request_id>", methods=["POST"])
    @admins_only
    def help_update(request_id):
        status = (request.get_json(silent=True) or {}).get("status")
        if status not in ("open", "coming", "done"):
            return jsonify({"success": False, "error": "Status has to be open, coming or done."}), 400
        row = StarsHelp.query.filter_by(id=request_id).first_or_404()
        row.status, row.updated = status, int(time.time())
        db.session.commit()
        return jsonify({"success": True, "request": describe(row)})

    @blueprint.route("/admin/stars-help/clear", methods=["POST"])
    @admins_only
    def help_clear():
        removed = StarsHelp.query.filter(StarsHelp.status.in_(("done", "cancelled"))).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({"success": True, "removed": removed})

    app.register_blueprint(blueprint)
