from flask import Flask, Response

from common import page

app = Flask(__name__)
FLAG = "STARS{b3ll4tr1x_r0b0ts_kn0w}"

HOME = """
<p>Our public pages are all listed in search engines. Some pages aren't, because
we've asked the search engine robots to stay away from them.</p>
<p>Bellatrix, the "female warrior", marks Orion's other shoulder.</p>
"""

LOG = """
<p>Private log. Robots are not supposed to find this page, and neither are you.</p>
<p class="key"><code>{{ flag }}</code></p>
"""


@app.route("/")
def home():
    return page("Bellatrix Station", "Public information page", HOME)


@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nDisallow: /captains-log/\n", mimetype="text/plain")


@app.route("/captains-log/")
def captains_log():
    return page("Captain's Log", "Bellatrix Station", LOG, flag=FLAG)
