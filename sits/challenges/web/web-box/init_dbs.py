"""Builds the two databases at image build time: cinema.db (Sign In Anyway) and
music.db (The Union)."""
import secrets
import sqlite3

# Sign In Anyway: the staff passwords are random, so nobody can guess them.
# Only the manager's dashboard shows the flag.
FLAG = "FLAG{s1gn3d_1n_w1th0ut_4_p4ssw0rd}"
db = sqlite3.connect("cinema.db")
db.execute("CREATE TABLE staff (username TEXT, password TEXT, job TEXT)")
db.execute("CREATE TABLE secrets (name TEXT, value TEXT)")
db.executemany(
    "INSERT INTO staff VALUES (?, ?, ?)",
    [
        ("guest", secrets.token_hex(16), "Visitor"),
        ("usher", secrets.token_hex(16), "Usher"),
        ("projectionist", secrets.token_hex(16), "Projectionist"),
        ("manager", secrets.token_hex(16), "Cinema Manager"),
    ],
)
db.execute("INSERT INTO secrets VALUES ('safe_code', ?)", (FLAG,))
db.commit()
db.close()

# The Union: a song search with three columns, and the flag in another table
# whose name players have to find.
FLAG = "FLAG{un10n_s3l3ct_f0und_th3_st4sh}"
db = sqlite3.connect("music.db")
db.execute("CREATE TABLE songs (title TEXT, artist TEXT, year INTEGER)")
db.execute("CREATE TABLE secret_stash_4d2b (item TEXT, value TEXT)")
db.executemany(
    "INSERT INTO songs VALUES (?, ?, ?)",
    [
        ("Morning Coffee", "The Early Birds", 2019),
        ("Rainy Day Blues", "Grey Skies", 2015),
        ("Pizza Party", "Extra Cheese", 2021),
        ("Last Bus Home", "Night Owls", 2018),
        ("Sunday Pancakes", "The Early Birds", 2022),
        ("Lost My Keys", "Forgetful Five", 2017),
        ("Dancing in the Kitchen", "Extra Cheese", 2023),
        ("Homework Can Wait", "The Procrastinators", 2020),
        ("Karaoke Night", "Night Owls", 2024),
        ("Window Seat", "Grey Skies", 2016),
    ],
)
db.executemany(
    "INSERT INTO secret_stash_4d2b VALUES (?, ?)",
    [
        ("wifi_password", "ask at the counter"),
        ("vault_code", FLAG),
        ("lunch_order", "two noodles, one rice"),
    ],
)
db.commit()
db.close()
