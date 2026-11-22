import sqlite3

FLAG = "STARS{4ln1t4k_un10n_s3l3ct_w1ns}"

db = sqlite3.connect("alnitak.db")
db.execute("CREATE TABLE stars (name TEXT, constellation TEXT, magnitude REAL)")
db.execute("CREATE TABLE dome_vault_7f3a (key_name TEXT, key_value TEXT)")
db.executemany(
    "INSERT INTO stars VALUES (?, ?, ?)",
    [
        ("Rigel", "Orion", 0.13),
        ("Betelgeuse", "Orion", 0.50),
        ("Bellatrix", "Orion", 1.64),
        ("Alnilam", "Orion", 1.69),
        ("Alnitak", "Orion", 1.77),
        ("Mintaka", "Orion", 2.23),
        ("Polaris", "Ursa Minor", 1.98),
        ("Kochab", "Ursa Minor", 2.08),
        ("Pherkad", "Ursa Minor", 3.05),
        ("Castor", "Gemini", 1.58),
        ("Pollux", "Gemini", 1.14),
        ("Alhena", "Gemini", 1.92),
        ("Vega", "Lyra", 0.03),
        ("Sheliak", "Lyra", 3.52),
        ("Sulafat", "Lyra", 3.25),
        ("Antares", "Scorpius", 0.96),
        ("Shaula", "Scorpius", 1.62),
        ("Sargas", "Scorpius", 1.87),
    ],
)
db.execute("INSERT INTO dome_vault_7f3a VALUES ('telescope_key', ?)", (FLAG,))
db.commit()
db.close()
