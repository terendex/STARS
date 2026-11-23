from flask import Flask, jsonify

from common import page

app = Flask(__name__)
FLAG = "FLAG{l0c4l_st0r4g3_r3m3mb3rs}"

# The script fetches the secret track and saves it in the browser's Local
# Storage, so it never appears in the page or its source.
HOME = """
<p>Welcome to Playlist Maker. We've picked a secret bonus track just for you.</p>
<p id="status">Picking your bonus track...</p>
<script>
  fetch("/api/bonus-track")
    .then((reply) => reply.json())
    .then((data) => {
      localStorage.setItem("bonus_track", data.track);
      localStorage.setItem("volume", "70");
      localStorage.setItem("theme", "light");
      document.getElementById("status").textContent =
        "Your bonus track has been saved in this browser for later. It's a surprise, so it isn't shown on screen.";
    });
</script>
"""


@app.route("/")
def home():
    return page("Playlist Maker", "Your music, your way", HOME)


@app.route("/api/bonus-track")
def bonus_track():
    return jsonify({"track": FLAG, "saved": "for later"})
