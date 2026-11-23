from flask import Flask, make_response

from common import page

app = Flask(__name__)
FLAG = "FLAG{h34d3rs_c4rry_s3cr3ts}"

BODY = """
<p><strong>Today:</strong> sunny, 31&deg;C, light breeze from the sea.</p>
<p><strong>Tomorrow:</strong> cloudy in the morning, rain after 3 pm. Bring an umbrella.</p>
<p>The secret forecast is only for our staff, and it isn't on this page.</p>
"""


@app.route("/")
def home():
    response = make_response(page("Weather Today", "Your local forecast", BODY))
    # The flag never appears on the page, only in the response's headers.
    response.headers["X-Secret-Forecast"] = FLAG
    return response
