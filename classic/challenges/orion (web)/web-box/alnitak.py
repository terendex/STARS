import sqlite3

from flask import Flask, request

from common import page

app = Flask(__name__)
DB_URI = "file:/app/alnitak.db?mode=ro"

BODY = """
<form method="get">
  <label for="q">Search for a star</label>
  <input id="q" name="q" value="{{ q }}" autocomplete="off" autofocus>
  <button type="submit">Search</button>
</form>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
{% if searched and not error %}
<div class="results">
  <table>
    <tr><th>Name</th><th>Constellation</th><th>Magnitude</th></tr>
    {% for row in rows %}
    <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td></tr>
    {% else %}
    <tr><td colspan="3">No stars found.</td></tr>
    {% endfor %}
  </table>
</div>
{% endif %}
"""


@app.route("/")
def home():
    q = request.args.get("q")
    rows, error = [], None
    if q is not None:
        # Intentionally vulnerable to SQL injection: this is the challenge.
        query = f"SELECT name, constellation, magnitude FROM stars WHERE name LIKE '%{q}%'"
        db = sqlite3.connect(DB_URI, uri=True)
        try:
            rows = db.execute(query).fetchmany(200)
        except sqlite3.Error as exc:
            error = f"Database error: {exc}"
        finally:
            db.close()
    return page(
        "Alnitak Star Catalog",
        "Orion's belt, eastern star",
        BODY,
        q=q or "",
        rows=rows,
        error=error,
        searched=q is not None,
    )
