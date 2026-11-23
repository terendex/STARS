import base64

from flask import Flask, make_response, request

from common import page

app = Flask(__name__)
FLAG = "FLAG{c00k13s_c4n_b3_3d1t3d}"
COOKIE = "membership"
NEEDED = "gold"

BODY = """
<p>Signed in with a <strong>{{ level }}</strong> membership.</p>
{% if level == needed %}
<p>Welcome to the sauna! Here's your locker code:</p>
<p class="key"><code>{{ flag }}</code></p>
{% else %}
<p>The sauna is only for <strong>{{ needed }}</strong> members.</p>
{% endif %}
"""


def encode(level):
    return base64.b64encode(f"level={level}".encode()).decode()


def read_level(value):
    try:
        text = base64.b64decode(value, validate=True).decode()
    except (ValueError, UnicodeDecodeError):
        return "unknown"
    return text[len("level="):].strip() if text.startswith("level=") else "unknown"


@app.route("/")
def home():
    value = request.cookies.get(COOKIE)
    level = read_level(value) if value else "basic"
    response = make_response(page("FitLife Gym", "Members' area", BODY, level=level, needed=NEEDED, flag=FLAG))
    if value is None:
        response.set_cookie(COOKIE, encode("basic"))
    return response
