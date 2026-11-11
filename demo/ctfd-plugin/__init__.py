"""Demo-only changes to CTFd.

1. Its own login cookie name. Browsers share cookies between ports on the same
   address, so without this, signing in to the demo on :8100 would sign you out
   of the real CTF on :8000.

2. No login needed. Anyone who opens the demo is signed in automatically as the
   account named in STARS_DEMO_AUTOLOGIN (demo1, on the Demo Team), so everyone
   shares that team's solves and attempts. Set it to an empty value in
   demo/docker-compose.yml to turn this off.

   The login page, the admin panel and API-token requests are left alone, so
   you can still sign in as admin at /login. Signing out goes back to demo1.
"""
import os

from flask import request

from CTFd.models import Users
from CTFd.utils.security.auth import login_user
from CTFd.utils.user import authed

AUTO_LOGIN = os.environ.get("STARS_DEMO_AUTOLOGIN", "").strip()
LEAVE_ALONE = {"auth.login", "views.setup", "views.themes", "views.themes_beta", "views.healthcheck"}


def load(app):
    app.config["SESSION_COOKIE_NAME"] = "stars_demo_session"

    if not AUTO_LOGIN:
        return

    @app.before_request
    def sign_in_automatically():
        if (
            authed()
            or request.endpoint in LEAVE_ALONE
            or request.path.startswith("/admin")
            or request.headers.get("Authorization")
        ):
            return
        user = Users.query.filter_by(name=AUTO_LOGIN, banned=False).first()
        if user is not None:
            login_user(user)
