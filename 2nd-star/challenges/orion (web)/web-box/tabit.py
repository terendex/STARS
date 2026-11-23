from flask import Flask

from common import page

app = Flask(__name__)
FLAG = "STARS{t4b1t_bl1nk_4nd_y0u_m1ss_1t}"

# The archive page holds the flag, but its meta refresh sends the browser to
# /closed at once. view-source:, the Network tab with Preserve log, or curl.exe
# all read it without following the redirect.
ARCHIVE = """
<p>Tabit night archive, shield of Orion.</p>
<p class="key"><code>{{ flag }}</code></p>
"""

CLOSED = """
<p>The Tabit archive is closed to visitors. You've been sent here instead.</p>
<p>The page you asked for was <code>/</code>, but you'll never see it.</p>
"""


@app.route("/")
def archive():
    html = page("Tabit Archive", "The shield of Orion", ARCHIVE, flag=FLAG)
    # Redirect straight away, before anything is visible.
    return html.replace("<head>", '<head>\n  <meta http-equiv="refresh" content="0; url=/closed">', 1)


@app.route("/closed")
def closed():
    return page("Tabit Archive", "The shield of Orion", CLOSED)
