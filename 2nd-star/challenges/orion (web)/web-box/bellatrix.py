from flask import Flask, Response, abort

from common import page

app = Flask(__name__)
FLAG = "STARS{b3ll4tr1x_d1s4ll0w3d_n0_m0r3}"

HOME = """
<p>Our public pages are all listed in search engines. Some pages aren't, because
we've asked the search engine robots to stay away from them.</p>
<p>Bellatrix, the "female warrior", marks Orion's other shoulder.</p>
"""

EMPTY = """
<p>This page was emptied when the station moved to its new site. Nothing here now.</p>
"""

LOG = """
<p>Night watch log. Robots are not supposed to find this page, and neither are you.</p>
<p class="key"><code>{{ flag }}</code></p>
"""

# Every path robots.txt lists. Only one still has anything on it.
HIDDEN = {
    "old-site": ("Old Site", EMPTY),
    "staff-rota": ("Staff Rota", EMPTY),
    "night-watch": ("Night Watch", LOG),
    "drafts": ("Drafts", EMPTY),
}


@app.route("/")
def home():
    return page("Bellatrix Station", "Public information page", HOME)


@app.route("/robots.txt")
def robots():
    lines = ["User-agent: *"] + [f"Disallow: /{path}/" for path in HIDDEN]
    return Response("\n".join(lines) + "\n", mimetype="text/plain")


@app.route("/<path>/")
def hidden(path):
    if path not in HIDDEN:
        abort(404)
    title, body = HIDDEN[path]
    return page(title, "Bellatrix Station", body, flag=FLAG)
