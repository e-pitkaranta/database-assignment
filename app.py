import os
import sqlite3
from flask import Flask, request, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

def init_database(filename, create_sql, insert_sql, rows):
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
    init_database(
        "jazz.db",
        "CREATE TABLE jazz (id INTEGER PRIMARY KEY AUTOINCREMENT, album TEXT NOT NULL, artist TEXT NOT NULL, year INTEGER)",
        "INSERT INTO jazz (album, artist, year) VALUES (?, ?, ?)",
        [("Kind of Blue", "Miles Davis", 1959),
         ("A Love Supreme", "John Coltrane", 1965),
         ("Time Out", "Dave Brubeck Quartet", 1959),
         ("Mingus Ah Um", "Charles Mingus", 1959),
         ("Head Hunters", "Herbie Hancock", 1973)],
    )
    init_database(
        "ambient.db",
        "CREATE TABLE ambient (id INTEGER PRIMARY KEY AUTOINCREMENT, album TEXT NOT NULL, artist TEXT NOT NULL, year INTEGER)",
        "INSERT INTO ambient (album, artist, year) VALUES (?, ?, ?)",
        [("Music for Airports", "Brian Eno", 1978),
         ("Selected Ambient Works 85-92", "Aphex Twin", 1992),
         ("Substrata", "Biosphere", 1997),
         ("The Disintegration Loops", "William Basinski", 2002),
         ("Discreet Music", "Brian Eno", 1975)],
    )
    init_database(
        "fusion.db",
        "CREATE TABLE fusion (id INTEGER PRIMARY KEY AUTOINCREMENT, album TEXT NOT NULL, artist TEXT NOT NULL, year INTEGER)",
        "INSERT INTO fusion (album, artist, year) VALUES (?, ?, ?)",
        [("Cross Point", "Casiopea", 1981),
         ("Mint Jams", "T-Square", 1982),
         ("Paradise", "Hiroshi Sato", 1980),
         ("Fuse", "Hiroshima", 1984),
         ("Bluesy", "Masayoshi Takanaka", 1980)],
    )

init_all()




DATABASES = {
    "jazz": "jazz.db",
    "ambient": "ambient.db",
    "fusion": "fusion.db",
}

def get_rows(db_name):
    path = os.path.join(BASE_DIR, DATABASES[db_name])
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM " + db_name).fetchall()
    conn.close()

    tulos = []
    for row in rows:
        tulos.append(dict(row))
    return tulos

@app.route("/api/<db_name>")
def api_read(db_name):
    if db_name not in DATABASES:
        return {"error": "Unknown database"}, 404
    return {"rows": get_rows(db_name)}



@app.route("/api/<db_name>", methods=["POST"])
def api_add(db_name):
    if db_name not in DATABASES:
        return {"error": "Unknown database"}, 404

    data = request.get_json()
    print(data)
    values = (data["album"], data["artist"], data["year"])

    path = os.path.join(BASE_DIR, DATABASES[db_name])
    conn = sqlite3.connect(path)
    conn.execute("INSERT INTO " + db_name + " (album, artist, year) VALUES (?,?,?)", values)
    conn.commit()
    conn.close()

    return {"done": True}

@app.route("/api/<db_name>/<int:row_id>", methods=["DELETE"])
def api_delete(db_name, row_id):
    if db_name not in DATABASES:
        return {"error": "Unknown database"}, 404

    path = os.path.join(BASE_DIR, DATABASES[db_name])
    conn = sqlite3.connect(path)
    conn.execute("DELETE FROM " + db_name + " WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()

    return {"done": True}

@app.route("/api/<db_name>/<int:row_id>", methods=["PUT"])
def api_update(db_name, row_id):
    if db_name not in DATABASES:
        return {"error": "Unknown database"}, 404

    data = request.get_json()
    print(data)
    values = (data["album"], data["artist"], data ["year"], row_id)

    path = os.path.join(BASE_DIR, DATABASES[db_name])
    conn = sqlite3.connect(path)
    conn.execute("UPDATE " + db_name + " SET album = ?, artist = ?, year = ? WHERE id = ?", values)
    conn.commit()
    conn.close()

    return {"done": True}

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
