from flask import Flask

from common import page

app = Flask(__name__)
FLAG = "STARS{b3t3lg3us3_v13w_s0urc3}"

BODY = """
<p>Welcome! Betelgeuse is the red supergiant at Orion's shoulder, and one of the
largest stars you can see without a telescope.</p>
<!-- Staff note: remove this before opening to the public. Archive key: {{ flag }} -->
<p>The visitor centre is open every clear night.</p>
"""


@app.route("/")
def home():
    return page("Betelgeuse Visitor Centre", "Orion's red shoulder", BODY, flag=FLAG)
