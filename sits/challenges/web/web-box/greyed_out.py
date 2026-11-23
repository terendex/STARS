from flask import Flask, request

from common import page

app = Flask(__name__)
FLAG = "FLAG{gr3y3d_0ut_but_n0t_l0ck3d}"

HOME = """
<p>Every Friday, the first visitor to press the button gets a free cookie. Today
someone already claimed it, so the button has been switched off.</p>
<form method="post" action="/claim">
  <label for="name">Your name</label>
  <input id="name" name="name" autocomplete="off">
  <!-- Switched off: today's cookie is gone. -->
  <button type="submit" disabled>Claim the free cookie</button>
</form>
"""

CLAIMED = """
<p>Claim received. Enjoy your cookie! Show this code at the counter:</p>
<p class="key"><code>{{ flag }}</code></p>
"""

USE_BUTTON = """
<p class="error">Claims are made with the button on the <a href="/">front page</a>.</p>
"""


@app.route("/")
def home():
    return page("Free Cookie Friday", "Sunny Side Bakery", HOME)


@app.route("/claim", methods=["GET", "POST"])
def claim():
    if request.method == "POST":
        # The disabled button in the page is the only thing stopping claims.
        return page("Free Cookie Friday", "Sunny Side Bakery", CLAIMED, flag=FLAG)
    return page("Free Cookie Friday", "Sunny Side Bakery", USE_BUTTON)
