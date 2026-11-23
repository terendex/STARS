from flask import Flask, request

from common import page

app = Flask(__name__)
FLAG = "STARS{h0rs3h34d_us3r_4g3nt_sp00f3d}"
BROWSER = "StarScope/2.0"

BODY = """
<p>Your browser introduced itself as:</p>
<p><code>{{ agent or "(nothing)" }}</code></p>
{% if allowed %}
<p>Welcome back, StarScope. The Horsehead archive is open.</p>
<p class="key"><code>{{ flag }}</code></p>
{% else %}
<p class="error">The Horsehead archive only opens for the observatory's own browser,
<code>{{ browser }}</code>.</p>
{% endif %}
"""


@app.route("/")
def home():
    agent = request.headers.get("User-Agent", "")
    allowed = BROWSER.lower() in agent.lower()
    return page("Horsehead Archive", "A dark nebula in Orion's belt", BODY,
                agent=agent, allowed=allowed, browser=BROWSER, flag=FLAG)
