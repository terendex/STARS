"""Changes to the real CTF's CTFd.

Accounts don't need an email. Players sign in with their name, they can't
register themselves, and CTFd here sends no mail, so an email would never be
used. CTFd itself accepts accounts without one, but its admin panel's Create User
and Edit User forms insist on it. This makes the email box in those forms
optional: leave it empty, or fill it in if you like.
"""
from wtforms.validators import Optional

from CTFd.forms import users


def load(app):
    users.UserBaseForm.email = users.EmailField("Email", validators=[Optional()])
