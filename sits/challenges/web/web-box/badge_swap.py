import base64
import json

from flask import Flask, make_response, request

from common import page

app = Flask(__name__)
FLAG = "FLAG{tw0_f13lds_sw4pp3d}"
COOKIE = "ticket"
UNREADABLE = "Your ticket cookie couldn't be read. It has to be Base64 of the same kind of text as before."

BODY = """
{% if problem %}
<p class="error">{{ problem }}</p>
{% else %}
<p>Ticket holder: <strong>{{ name }}</strong></p>
<p>Seat: <strong>{{ seat }}</strong> &middot; Backstage: <strong>{{ backstage }}</strong></p>
{% endif %}
{% if allowed %}
<p>Welcome backstage! The band left you a note:</p>
<p class="key"><code>{{ flag }}</code></p>
{% else %}
<p>Backstage is only for tickets with seat <strong>vip</strong> <em>and</em> backstage <strong>true</strong>.</p>
{% endif %}
"""


def make_ticket():
    return base64.b64encode(json.dumps({"name": "guest", "seat": "standing", "backstage": False}).encode()).decode()


def read_ticket(value):
    """Returns (name, seat, backstage, problem)."""
    try:
        ticket = json.loads(base64.b64decode(value, validate=True).decode())
    except (ValueError, UnicodeDecodeError):
        return None, None, None, UNREADABLE
    if not isinstance(ticket, dict):
        return None, None, None, UNREADABLE
    backstage = ticket.get("backstage", False)
    # true and "true" both count, so a beginner's quotes don't matter.
    backstage = "true" if str(backstage).strip().lower() == "true" else "false"
    return str(ticket.get("name", "?")), str(ticket.get("seat", "?")).strip(), backstage, None


@app.route("/")
def home():
    value = request.cookies.get(COOKIE)
    if value:
        name, seat, backstage, problem = read_ticket(value)
    else:
        name, seat, backstage, problem = "guest", "standing", "false", None
    allowed = problem is None and seat.lower() == "vip" and backstage == "true"
    response = make_response(page(
        "Summer Beats Festival", "Your ticket", BODY,
        name=name, seat=seat, backstage=backstage, problem=problem, allowed=allowed, flag=FLAG,
    ))
    if value is None:
        response.set_cookie(COOKIE, make_ticket())
    return response
