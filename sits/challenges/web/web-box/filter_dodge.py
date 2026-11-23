import os

from flask import Flask, request

from common import page

app = Flask(__name__)
FLAG = "FLAG{f1lt3r_d0dg3d_w1th_d0ts}"

# The travel diary's pages, and the flag one folder above them. Written at
# start-up into /tmp (the only writable place in the container).
BASE = "/tmp/travel-diary"
PAGES = os.path.join(BASE, "pages")
FILES = {
    "day1.txt": "Day 1: Arrived at the beach. The hotel has a pool shaped like a guitar.",
    "day2.txt": "Day 2: Went snorkelling and saw a turtle. Got sunburnt anyway.",
    "day3.txt": "Day 3: Rained all day. Played cards and ate too much ice cream.",
}
os.makedirs(PAGES, exist_ok=True)
for name, text in FILES.items():
    with open(os.path.join(PAGES, name), "w") as f:
        f.write(text + "\n")
with open(os.path.join(BASE, "flag.txt"), "w") as f:
    f.write(f"Souvenir code: {FLAG}\n")

BODY = """
<p><a href="?page=day1.txt">Day 1</a> &middot; <a href="?page=day2.txt">Day 2</a>
&middot; <a href="?page=day3.txt">Day 3</a></p>
<p><small>You asked for: <code>{{ asked }}</code><br>
After the safety filter: <code>{{ filtered }}</code></small></p>
{% if error %}<p class="error">{{ error }}</p>{% else %}<p>{{ text }}</p>{% endif %}
"""


@app.route("/")
def home():
    asked = request.args.get("page", "day1.txt")
    # The "safety filter" removes ../ once. It doesn't look again afterwards,
    # so ....// turns back into ../ : this is the challenge.
    filtered = asked.replace("../", "")
    path = os.path.join(PAGES, filtered)
    try:
        with open(path) as f:
            text, error = f.read(), None
    except OSError:
        text, error = None, f"Couldn't open the file {path}"
    return page("Travel Diary", "Summer holiday", BODY, asked=asked, filtered=filtered, text=text, error=error)
