import sqlite3
from flask import Flask, render_template, request, flash
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = "linkkiwi2026"

def get_db():
    conn = sqlite3.connect('myproject.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll INTEGER NOT NULL,
            marks INTEGER NOT NULL,
            subject TEXT NOT NULL,
            attendance INTEGER DEFAULT 0
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    try:
        conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
    except Exception:
        pass

    admin = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if admin is None:
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", generate_password_hash("admin123"), "admin")
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    