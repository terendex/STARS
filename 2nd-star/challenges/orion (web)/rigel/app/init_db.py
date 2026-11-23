import secrets
import sqlite3

FLAG = "STARS{r1g3l_c0mm3nt3d_0ut_th3_p4ssw0rd}"

db = sqlite3.connect("observatory.db")
db.execute("CREATE TABLE staff (username TEXT, password TEXT, role TEXT, clearance INTEGER)")
db.execute("CREATE TABLE secrets (name TEXT, value TEXT)")
db.executemany(
    "INSERT INTO staff VALUES (?, ?, ?, ?)",
    [
        ("guest", secrets.token_hex(16), "Visiting Observer", 1),
        ("technician", secrets.token_hex(16), "Dome Technician", 3),
        ("archivist", secrets.token_hex(16), "Plate Archivist", 5),
        ("curator", secrets.token_hex(16), "Head Curator", 7),
    ],
)
db.execute("INSERT INTO secrets VALUES ('telescope_key', ?)", (FLAG,))
db.commit()
db.close()
