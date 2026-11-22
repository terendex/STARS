import sqlite3

FLAG = "STARS{4ln1t4k_un10n_s3l3ct_d33p3r}"

db = sqlite3.connect("alnitak.db")
db.execute("CREATE TABLE stars (name TEXT, constellation TEXT, magnitude REAL, distance_ly INTEGER)")
db.execute("CREATE TABLE archive_b71d (label TEXT, secret TEXT)")
db.executemany(
    "INSERT INTO stars VALUES (?, ?, ?, ?)",
    [
        ("Rigel", "Orion", 0.13, 860),
        ("Betelgeuse", "Orion", 0.50, 550),
        ("Bellatrix", "Orion", 1.64, 250),
        ("Alnilam", "Orion", 1.69, 2000),
        ("Alnitak", "Orion", 1.77, 1260),
        ("Mintaka", "Orion", 2.23, 1200),
        ("Polaris", "Ursa Minor", 1.98, 430),
        ("Kochab", "Ursa Minor", 2.08, 130),
        ("Pherkad", "Ursa Minor", 3.05, 490),
        ("Castor", "Gemini", 1.58, 51),
        ("Pollux", "Gemini", 1.14, 34),
        ("Alhena", "Gemini", 1.92, 110),
        ("Vega", "Lyra", 0.03, 25),
        ("Sheliak", "Lyra", 3.52, 960),
        ("Sulafat", "Lyra", 3.25, 620),
        ("Antares", "Scorpius", 0.96, 550),
        ("Shaula", "Scorpius", 1.62, 570),
        ("Sargas", "Scorpius", 1.87, 300),
    ],
)
db.executemany(
    "INSERT INTO archive_b71d VALUES (?, ?)",
    [
        ("dome_schedule", "Opens at dusk, closes at dawn"),
        ("telescope_key", FLAG),
        ("wifi_password", "ask at the front desk"),
    ],
)
db.commit()
db.close()
