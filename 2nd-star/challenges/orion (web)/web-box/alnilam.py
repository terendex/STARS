import base64
import json

from flask import Flask, make_response, request

from common import page

app = Flask(__name__)
FLAG = "STARS{4ln1l4m_r4nk3d_up_v14_c00k13}"
COOKIE = "badge"
NEEDED = "commander"
UNREADABLE = "Your badge cookie couldn't be read. It has to be Base64 of the same kind of text as before."

BODY = """
{% if problem %}
<p class="error">{{ problem }}</p>
{% else %}
<p>Signed in as: <strong>{{ name }}</strong>, rank <strong>{{ rank }}</strong></p>
{% endif %}
{% if rank == needed %}
<p>The dome is open.</p>
<p class="key"><code>{{ flag }}</code></p>
{% else %}
<p>The dome only opens for the rank <strong>{{ needed }}</strong>.</p>
{% endif %}
"""


def make_badge():
    return base64.b64encode(json.dumps({"name": "guest", "rank": "cadet"}).encode()).decode()


def read_badge(value):
    """Returns (name, rank, problem)."""
    try:
        badge = json.loads(base64.b64decode(value, validate=True).decode())
    except (ValueError, UnicodeDecodeError):
        return None, None, UNREADABLE
    if not isinstance(badge, dict):
        return None, None, UNREADABLE
    return str(badge.get("name", "?")), str(badge.get("rank", "?")).strip(), None


@app.route("/")
def home():
    value = request.cookies.get(COOKIE)
    if value:
        name, rank, problem = read_badge(value)
    else:
        name, rank, problem = "guest", "cadet", None
    response = make_response(page(
        "Alnilam Dome", "Orion's belt, central star", BODY,
        name=name, rank=rank, problem=problem, needed=NEEDED, flag=FLAG,
    ))
    if value is None:
        response.set_cookie(COOKIE, make_badge())
    return response
