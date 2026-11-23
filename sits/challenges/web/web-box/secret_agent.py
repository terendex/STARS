from flask import Flask, request

from common import page

app = Flask(__name__)
FLAG = "FLAG{y0u_4r3_wh0_y0u_s4y_y0u_4r3}"
BROWSER = "SecretAgent/007"

BODY = """
<p>Your browser introduced itself as:</p>
<p><code>{{ agent or "(nothing)" }}</code></p>
{% if allowed %}
<p>Welcome back, agent. The gadget catalogue is open.</p>
<p class="key"><code>{{ flag }}</code></p>
{% else %}
<p class="error">The gadget catalogue only opens for the agency's own browser,
<code>{{ browser }}</code>.</p>
{% endif %}
"""


@app.route("/")
def home():
    agent = request.headers.get("User-Agent", "")
    allowed = BROWSER.lower() in agent.lower()
    return page("Spy Gadget Shop", "Agents only", BODY, agent=agent, allowed=allowed, browser=BROWSER, flag=FLAG)
