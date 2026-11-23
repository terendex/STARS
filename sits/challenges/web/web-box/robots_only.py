from flask import Flask, Response, abort

from common import page

app = Flask(__name__)
FLAG = "FLAG{r0b0ts_txt_p01nts_th3_w4y}"

HOME = """
<p>Bean There is the coffee shop on the corner. Our public pages are all listed in
search engines. Some pages aren't, because we've asked the search engine robots
to stay away from them.</p>
"""

EMPTY = """
<p>This page was emptied when we moved the website. Nothing here now.</p>
"""

BACKUP = """
<p>Backup of the shop's secret recipe card. Robots aren't supposed to find this
page, and neither are you.</p>
<p class="key"><code>{{ flag }}</code></p>
"""

# Every path robots.txt lists. Only one still has anything on it.
HIDDEN = {
    "old-menu": ("Old Menu", EMPTY),
    "staff-only": ("Staff Only", EMPTY),
    "backup": ("Backup", BACKUP),
    "test-page": ("Test Page", EMPTY),
}


@app.route("/")
def home():
    return page("Bean There Coffee", "Open daily", HOME)


@app.route("/robots.txt")
def robots():
    lines = ["User-agent: *"] + [f"Disallow: /{path}/" for path in HIDDEN]
    return Response("\n".join(lines) + "\n", mimetype="text/plain")


@app.route("/<path>/")
def hidden(path):
    if path not in HIDDEN:
        abort(404)
    title, body = HIDDEN[path]
    return page(title, "Bean There Coffee", body, flag=FLAG)
