import sqlite3

from flask import Flask, request

from common import page

app = Flask(__name__)
DB_URI = "file:/app/cinema.db?mode=ro"

LOGIN = """
<form method="post">
  <label for="username">Username</label>
  <input id="username" name="username" autocomplete="off" autofocus>
  <label for="password">Password</label>
  <input id="password" name="password" type="password">
  <button type="submit">Sign in</button>
</form>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
"""

DASHBOARD = """
<p>Signed in as <strong>{{ username }}</strong> ({{ job }}).</p>
{% if key %}
<p>The safe code for tonight:</p>
<p class="key"><code>{{ key }}</code></p>
{% else %}
<p>Only the <strong>manager</strong> account can see the safe code.</p>
{% endif %}
<p><a href="/">Sign out</a></p>
"""


def run_query(query, params=()):
    db = sqlite3.connect(DB_URI, uri=True)
    try:
        return db.execute(query, params).fetchone()
    finally:
        db.close()


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # Intentionally vulnerable to SQL injection: this is the challenge.
        query = f"SELECT username, job FROM staff WHERE username = '{username}' AND password = '{password}'"
        try:
            row = run_query(query)
        except sqlite3.Error as exc:
            error = f"Database error: {exc}"
        else:
            if row is not None:
                key = None
                if row[0] == "manager":
                    key = run_query("SELECT value FROM secrets WHERE name = ?", ("safe_code",))[0]
                return page("Starlight Cinema", "Staff portal", DASHBOARD, username=row[0], job=row[1], key=key)
            error = "Wrong username or password."
    return page("Starlight Cinema", "Staff portal", LOGIN, error=error)
