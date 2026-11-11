from flask import Flask, make_response

from common import page

app = Flask(__name__)
FLAG = "STARS{s41ph_s3nds_h34d3rs}"

BODY = """
<p>Saiph marks the hunter's right knee in Orion. It's a blue supergiant, and much
hotter than our Sun.</p>
<p><strong>Status:</strong> all telescopes tracking. Nothing to report.</p>
"""


@app.route("/")
def home():
    response = make_response(page("Saiph Status Board", "Orion's right knee", BODY))
    # The flag never appears on the page, only in the response headers.
    response.headers["X-Archive-Key"] = FLAG
    return response
