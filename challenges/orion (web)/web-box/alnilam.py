import base64

from flask import Flask, make_response, request

from common import page

app = Flask(__name__)
FLAG = "STARS{4ln1l4m_c00k13s_c4n_l13}"
COOKIE = "pass"

BODY = """
<p>Signed in as: <strong>{{ role }}</strong></p>
{% if role == "astronomer" %}
<p>The dome is open.</p>
<p class="key"><code>{{ flag }}</code></p>
{% else %}
<p>The dome only opens for the role <strong>astronomer</strong>.</p>
{% endif %}
"""


def encode_pass(role):
    return base64.b64encode(f"role={role}".encode()).decode()


def read_role(value):
    try:
        text = base64.b64decode(value, validate=True).decode()
    except ValueError:
        return "visitor"
    return text[len("role="):] if text.startswith("role=") else "visitor"


@app.route("/")
def home():
    value = request.cookies.get(COOKIE)
    role = read_role(value) if value else "visitor"
    response = make_response(
        page("Alnilam Dome", "Orion's belt, central star", BODY, role=role, flag=FLAG)
    )
    if value is None:
        response.set_cookie(COOKIE, encode_pass("visitor"))
    return response
