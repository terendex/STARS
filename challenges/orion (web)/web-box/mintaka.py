from flask import Flask, request

from common import page

app = Flask(__name__)
FLAG = "STARS{m1nt4k4_s3rv3r_n3v3r_ch3ck3d}"

HOME = """
<p>Mintaka's vault is closed for the season, so the request button has been
switched off.</p>
<form method="post" action="/request">
  <label for="name">Your name</label>
  <input id="name" name="name" autocomplete="off">
  <!-- Switched off for the season. -->
  <button type="submit" disabled>Request vault access</button>
</form>
"""

OPEN = """
<p>Request received. The vault is open.</p>
<p class="key"><code>{{ flag }}</code></p>
"""

USE_BUTTON = """
<p class="error">Requests are made with the button on the <a href="/">front page</a>.</p>
"""


@app.route("/")
def home():
    return page("Mintaka Vault", "Orion's belt, western star", HOME)


@app.route("/request", methods=["GET", "POST"])
def request_access():
    if request.method == "POST":
        # The disabled button in the page is the only thing stopping requests.
        return page("Mintaka Vault", "Orion's belt, western star", OPEN, flag=FLAG)
    return page("Mintaka Vault", "Orion's belt, western star", USE_BUTTON)
