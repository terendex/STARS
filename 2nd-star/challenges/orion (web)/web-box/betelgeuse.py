from flask import Flask

from common import page

app = Flask(__name__)
FLAG = "STARS{b3t3lg3us3_r34d_th3_c0mm3nts}"

BODY = """
<p>Welcome! Betelgeuse is the red supergiant at Orion's shoulder. It's so big
that if it sat where our Sun is, it would swallow Mars.</p>
<!-- TODO: the opening hours below are out of date. -->
<p>The visitor centre is open every clear night.</p>
<!-- Staff note: delete this before the site goes public. Archive key: {{ flag }} -->
<p>Ask at the front desk about our telescope tours.</p>
"""


@app.route("/")
def home():
    return page("Betelgeuse Visitor Centre", "Orion's red shoulder", BODY, flag=FLAG)
