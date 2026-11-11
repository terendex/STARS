import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)
DB_URI = "file:/app/observatory.db?mode=ro"
TOP_CLEARANCE = "9"


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
        query = (
            "SELECT username, role, clearance FROM staff "
            f"WHERE username = '{username}' AND password = '{password}'"
        )
        try:
            row = run_query(query)
        except sqlite3.Error as exc:
            error = f"Database error: {exc}"
        else:
            if row is not None:
                return dashboard(*row)
            error = "Invalid username or password."
    return render_template("login.html", error=error)


def dashboard(username, role, clearance):
    key = None
    if str(clearance) == TOP_CLEARANCE:
        key = run_query("SELECT value FROM secrets WHERE name = ?", ("telescope_key",))[0]
    return render_template(
        "dashboard.html",
        username=username,
        role=role,
        clearance=clearance,
        top_clearance=TOP_CLEARANCE,
        key=key,
    )
