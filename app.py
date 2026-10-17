import os
import sqlite3
from flask import Flask

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)


def init_db(filename, create_sql, insert_sql, rows):
    path = os.path.join(BASE_DIR, filename)
    print("Database:", filename, "/path:", path, "/exists:", os.path.exists(path))
    if os.path.exists(path):
        return
    conn = sqlite3.connect(path)
    conn.execute(create_sql)
    conn.executemany(insert_sql, rows)
    conn.commit()
    conn.close()

def init_all():
    init_db(
        "jazz.db",
        "CREATE TABLE jazz (id INTEGER PRIMARY KEY AUTOINCREMENT, album TEXT NOT NULL, artist TEXT NOT NULL, year INTEGER)",
        "INSERT INTO jazz (album, artist, year) VALUES (?, ?, ?)",
        [("Kind of Blue", "Miles Davis", 1959),
         ("A Love Supreme", "John Coltrane", 1965),
         ("Time Out", "Dave Brubeck Quartet", 1959),
         ("Mingus Ah Um", "Charles Mingus", 1959),
         ("Head Hunters", "Herbie Hancock", 1973)],
    )
    init_db(
        "ambient.db",
        "CREATE TABLE ambient (id INTEGER PRIMARY KEY AUTOINCREMENT, album TEXT NOT NULL, artist TEXT NOT NULL, year INTEGER)",
        "INSERT INTO ambient (album, artist, year) VALUES (?, ?, ?)",
        [("Music for Airports", "Brian Eno", 1978),
         ("Selected Ambient Works 85-92", "Aphex Twin", 1992),
         ("Substrata", "Biosphere", 1997),
         ("The Disintegration Loops", "William Basinski", 2002),
         ("Discreet Music", "Brian Eno", 1975)],
    )
    init_db(
        "mountains.db",
        "CREATE TABLE mountains (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, country TEXT NOT NULL, height_m INTEGER)",
        "INSERT INTO mountains (name, country, height_m) VALUES (?, ?, ?)",
        [("Mount Everest", "Nepal/China", 8849),
         ("K2", "Pakistan/China", 8611),
         ("Mont Blanc", "France/Italy", 4806),
         ("Kebnekaise", "Sweden", 2096),
         ("Halti", "Finland", 1324)],
    )

init_all()

@app.route("/")
def home():
    return "Hello, databases!"

if __name__ == "__main__":
    app.run(debug=True)