from flask import Flask

from common import page

app = Flask(__name__)
FLAG = "FLAG{v13w_s0urc3_r3v34ls_4ll}"

BODY = """
<p>Welcome to Sunny Side Bakery! Fresh bread every morning from 6 am.</p>
<!-- TODO: the croissant price below is out of date. -->
<p>Today's special: chocolate croissants, two for the price of one.</p>
<!-- Staff note: delete this before the site goes live. Oven password: {{ flag }} -->
<p>Ask at the counter about birthday cakes.</p>
<!-- Photo of the shop goes here once we take one. -->
"""


@app.route("/")
def home():
    return page("Sunny Side Bakery", "Fresh every morning", BODY, flag=FLAG)
