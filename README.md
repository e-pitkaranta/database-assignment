# Multi-Database Manager

A small web application for the Data-Intensive Systems course. It uses three separate SQLite databases (`employees`, `projects`, `customers`), each with its own columns and dummy data. In the browser you can select a database and read, add, edit and delete rows.

## Requirements

- Python 3
- Flask (SQLite is included in Python)

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Then open http://localhost:5000 in a browser.

The three database files are created automatically with dummy data on the first start.

## How to use

1. Select a database from the dropdown.
2. The rows are shown in a table.
3. Add a row with the form below the table.
4. Press Edit to change a row, then Save.
5. Press Delete to remove a row.

## Files

- `app.py` - Flask backend, creates the databases and provides the API
- `templates/index.html` - the user interface
- `requirements.txt` - Python packages needed

## Demo video

(link here)