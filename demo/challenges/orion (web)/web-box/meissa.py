from flask import Flask

from common import page

app = Flask(__name__)
FLAG = "STARS{m31ss4_3ntry_z3r0}"

# Entry 0 is never linked from the home page. Changing the number in the
# address is all it takes to read it.
ENTRIES = {
    0: ("Staff only", f"Not for public release. Archive key: {FLAG}"),
    1: ("Night 1", "Clear skies. Meissa, at Orion's head, was easy to find."),
    2: ("Night 2", "Thin cloud after midnight. Three hours of usable data."),
    3: ("Night 3", "Fully overcast. No observations."),
    4: ("Night 4", "Clear and still. Measured Meissa's brightness every ten minutes."),
    5: ("Night 5", "Clear. Packed up the telescope at dawn."),
}

HOME = """
<p>The log from our week watching Meissa, the star at Orion's head.</p>
<ul>
{% for number in range(1, 6) %}
  <li><a href="/entry/{{ number }}">Entry {{ number }}</a></li>
{% endfor %}
</ul>
"""

ENTRY = """
<p>{{ text }}</p>
<p><a href="/">Back to the log</a></p>
"""


@app.route("/")
def home():
    return page("Meissa Observation Log", "Orion's head", HOME)


@app.route("/entry/<int:number>")
def entry(number):
    if number not in ENTRIES:
        return page("Meissa Observation Log", "No such entry",
                    '<p>There\'s no entry with that number.</p><p><a href="/">Back to the log</a></p>'), 404
    title, text = ENTRIES[number]
    return page("Meissa Observation Log", f"Entry {number}: {title}", ENTRY, text=text)
