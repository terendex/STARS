import secrets
import sqlite3

FLAG = "STARS{r1g3l_bl1nds_th3_0bs3rv4t0ry}"

db = sqlite3.connect("observatory.db")
db.execute("CREATE TABLE staff (username TEXT, password TEXT, role TEXT, clearance INTEGER)")
db.execute("CREATE TABLE secrets (name TEXT, value TEXT)")
db.executemany(
    "INSERT INTO staff VALUES (?, ?, ?, ?)",
    [
        ("observer", secrets.token_hex(16), "Night Observer", 1),
        ("technician", secrets.token_hex(16), "Dome Technician", 3),
        ("director", secrets.token_hex(16), "Observatory Director", 9),
    ],
)
db.execute("INSERT INTO secrets VALUES ('telescope_key', ?)", (FLAG,))
db.commit()
db.close()
