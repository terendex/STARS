from flask import Flask, jsonify

from common import page

app = Flask(__name__)
FLAG = "STARS{h4ty54_r3m3mb3rs_y0u}"

# The pass is fetched and saved to the browser's Local Storage by the script,
# so it never appears in the page or its source.
HOME = """
<p>Welcome to Hatysa, the brightest star in Orion's sword.</p>
<p id="status">Issuing your visitor pass...</p>
<script>
  fetch("/api/visitor-pass")
    .then((reply) => reply.json())
    .then((data) => {
      localStorage.setItem("hatysa_visitor_pass", data.pass);
      localStorage.setItem("hatysa_visits", String(Number(localStorage.getItem("hatysa_visits") || 0) + 1));
      document.getElementById("status").textContent =
        "Your visitor pass has been saved in this browser. For your security, it isn't shown on screen.";
    });
</script>
"""


@app.route("/")
def home():
    return page("Hatysa Observatory", "The sword of Orion", HOME)


@app.route("/api/visitor-pass")
def visitor_pass():
    return jsonify({"pass": FLAG, "valid": "tonight only"})
