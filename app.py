import os
import sqlite3
from flask import Flask

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)


def init_db(filename, create_sql, insert_sql, rows):
    path = os.path.join(BASE_DIR, filename)
    print("Tarkistetaan:", path, os.path.exists(path))
    if os.path.exists(path):
        return
    conn = sqlite3.connect(path)
    conn.execute(create_sql)
    conn.executemany(insert_sql, rows)
    conn.commit()
    conn.close()

def init_all():
    init_db(
        "books.db",
        "CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, author TEXT NOT NULL, year INTEGER)",
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        [("Dune", "Frank Herbert", 1965),
         ("1984", "George Orwell", 1949),
         ("The Hobbit", "J.R.R. Tolkien", 1937),
         ("Neuromancer", "William Gibson", 1984)],
    )
    init_db(
        "movies.db",
        "CREATE TABLE movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, director TEXT NOT NULL, year INTEGER)",
        "INSERT INTO movies (title, director, year) VALUES (?, ?, ?)",
        [("Blade Runner", "Ridley Scott", 1982),
         ("Inception", "Christopher Nolan", 2010),
         ("The Matrix", "The Wachowskis", 1999),
         ("Alien", "Ridley Scott", 1979)],
    )
    init_db(
        "students.db",
        "CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, course TEXT NOT NULL, grade INTEGER)",
        "INSERT INTO students (name, course, grade) VALUES (?, ?, ?)",
        [("Matti", "Databases", 4),
         ("Liisa", "Databases", 5),
         ("Pekka", "Statistics", 3),
         ("Aino", "Statistics", 5)],
    )

init_all()

@app.route("/")
def home():
    return "Hello, databases!"

if __name__ == "__main__":
    app.run(debug=True)