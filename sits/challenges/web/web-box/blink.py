from flask import Flask

from common import page

app = Flask(__name__)
FLAG = "FLAG{r3d1r3ct_t00_f4st}"

# The lost property page holds the flag, but its meta refresh sends the browser
# to /moved at once. view-source:, the Network tab, or curl.exe all read it
# without following the redirect.
LOST = """
<p>Lost property this week: one umbrella, two left gloves, and a note that says:</p>
<p class="key"><code>{{ flag }}</code></p>
"""

MOVED = """
<p>The lost and found page has moved. You've been sent here instead.</p>
<p>The page you asked for was <code>/</code>, but you'll never see it.</p>
"""


@app.route("/")
def lost():
    html = page("Lost and Found", "Town library", LOST, flag=FLAG)
    # Redirect straight away, before anything is visible.
    return html.replace("<head>", '<head>\n  <meta http-equiv="refresh" content="0; url=/moved">', 1)


@app.route("/moved")
def moved():
    return page("Lost and Found", "Town library", MOVED)
