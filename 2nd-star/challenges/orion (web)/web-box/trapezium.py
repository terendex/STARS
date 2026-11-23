import os

from flask import Flask, request

from common import page

app = Flask(__name__)
FLAG = "STARS{tr4p3z1um_cl1mb3d_0ut_0f_th3_f0ld3r}"

# The site's text files, and the flag one folder above them. Written at start-up
# into /tmp (the only writable place in the container).
BASE = "/tmp/trapezium"
PAGES = os.path.join(BASE, "pages")
FILES = {
    "welcome.txt": "Welcome to the Trapezium, four young stars at the heart of the Orion Nebula. "
                   "Use the links above to read about them.",
    "stars.txt": "The four brightest Trapezium stars are named A, B, C and D. Theta-1 Orionis C is the "
                 "brightest and lights up most of the nebula.",
    "history.txt": "Galileo drew three of the stars in 1617. The fourth was spotted in 1673.",
}
os.makedirs(PAGES, exist_ok=True)
for name, text in FILES.items():
    with open(os.path.join(PAGES, name), "w") as f:
        f.write(text + "\n")
with open(os.path.join(BASE, "flag.txt"), "w") as f:
    f.write(f"Trapezium staff key: {FLAG}\n")

BODY = """
<p><a href="?page=welcome.txt">Welcome</a> &middot; <a href="?page=stars.txt">The stars</a>
&middot; <a href="?page=history.txt">History</a></p>
{% if error %}<p class="error">{{ error }}</p>{% else %}<p>{{ text }}</p>{% endif %}
"""


@app.route("/")
def home():
    name = request.args.get("page", "welcome.txt")
    # Intentionally vulnerable to path traversal: this is the challenge.
    path = os.path.join(PAGES, name)
    try:
        with open(path) as f:
            text, error = f.read(), None
    except OSError:
        text, error = None, f"Couldn't open the file {path}"
    return page("Trapezium Cluster", "The heart of the Orion Nebula", BODY, text=text, error=error)
