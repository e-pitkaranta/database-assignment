import os
import sqlite3
from flask import Flask, request, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where this file is
app = Flask(__name__)

# Creates one database file with a table and dummy data (skips if file exists)
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

# Creates all three databases
def init_all():
    init_database(
        "employees.db",
        "CREATE TABLE employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, department TEXT NOT NULL, salary INTEGER, hired_year INTEGER)",
        "INSERT INTO employees (name, department, salary, hired_year) VALUES (?, ?, ?, ?)",
        [("Matti Virtanen", "Production", 3200, 2015),
         ("Laura Korhonen", "Finance", 3800, 2018),
         ("Jussi Nieminen", "IT", 4100, 2020),
         ("Sanna Mäkinen", "HR", 3500, 2017),
         ("Pekka Laine", "Production", 3000, 2022)],
    )
    init_database(
        "projects.db",
        "CREATE TABLE projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, owner TEXT NOT NULL, status TEXT NOT NULL, budget INTEGER)",
        "INSERT INTO projects (name, owner, status, budget) VALUES (?, ?, ?, ?)",
        [("New ERP system", "Jussi Nieminen", "In progress", 120000),
         ("Safety training", "Sanna Mäkinen", "Done", 8000),
         ("Line 3 upgrade", "Matti Virtanen", "Planned", 250000),
         ("Budget 2027", "Laura Korhonen", "In progress", 5000),
         ("Website renewal", "Jussi Nieminen", "Planned", 15000)],
    )
    init_database(
        "customers.db",
        "CREATE TABLE customers (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT NOT NULL, contact TEXT NOT NULL, city TEXT, country TEXT)",
        "INSERT INTO customers (company, contact, city, country) VALUES (?, ?, ?, ?)",
        [("Nordic Metals Oy", "Aino Salo", "Pori", "Finland"),
         ("Baltic Steel AB", "Erik Lund", "Gothenburg", "Sweden"),
         ("Rhein Kupfer GmbH", "Hans Weber", "Hamburg", "Germany"),
         ("Kupari Trading", "Mikko Heino", "Helsinki", "Finland"),
         ("Oslo Cable AS", "Ingrid Berg", "Oslo", "Norway")],
    )

init_all()  # runs at startup




# Database name -> file name
DATABASES = {
    "employees": "employees.db",
    "projects": "projects.db",
    "customers": "customers.db",
}

# Columns of each table (without id)
COLUMNS = {
    "employees": ["name", "department", "salary", "hired_year"],
    "projects": ["name", "owner", "status", "budget"],
    "customers": ["company", "contact", "city", "country"],
}

# Reads all rows of a table and returns them as a list of dicts
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

# READ: returns columns and rows of the chosen database
@app.route("/api/<db_name>")
def api_read(db_name):
    if db_name not in DATABASES:
        return {"error": "Unknown database"}, 404
    return {"columns": COLUMNS[db_name], "rows": get_rows(db_name)}



# ADD: inserts a new row
@app.route("/api/<db_name>", methods=["POST"])
def api_add(db_name):
    if db_name not in DATABASES:
        return {"error": "Unknown database"}, 404

    data = request.get_json()  # values sent by the page
    print(data)

    names = COLUMNS[db_name]

    # build the values and the ? marks from the column list
    values = []
    marks = []
    for name in names:
        values.append(data[name])
        marks.append("?")

    sql = "INSERT INTO " + db_name + " (" + ", ".join(names) + ") VALUES (" + ", ".join(marks) + ")"

    path = os.path.join(BASE_DIR, DATABASES[db_name])
    conn = sqlite3.connect(path)
    conn.execute(sql, values)
    conn.commit()
    conn.close()

    return {"done": True}

# DELETE: removes the row with the given id
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

# UPDATE: changes the row with the given id
@app.route("/api/<db_name>/<int:row_id>", methods=["PUT"])
def api_update(db_name, row_id):
    if db_name not in DATABASES:
        return {"error": "Unknown database"}, 404

    data = request.get_json()
    print(data)

    names = COLUMNS[db_name]

    # parts = "name = ?" pieces, values = new values (id goes last for WHERE)
    parts = []
    values = []
    for name in names:
        parts.append(name + " = ?")
        values.append(data[name])
    values.append(row_id)

    sql = "UPDATE " + db_name + " SET " + ", ".join(parts) + " WHERE id = ?"

    path = os.path.join(BASE_DIR, DATABASES[db_name])
    conn = sqlite3.connect(path)
    conn.execute(sql, values)
    conn.commit()
    conn.close()

    return {"done": True}

# Front page: sends the HTML page to the browser
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)  # starts the server