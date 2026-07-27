import os
import sqlite3

# Absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "myproject.db")


# Database connection
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Create tables
def init_db():

    conn = get_db()

    # Students Table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            marks INTEGER,
            subject TEXT NOT NULL,
            attendance INTEGER DEFAULT 0
        )
    """)

    # Users Table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Subjects Table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Add role column
    try:
        conn.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
    except Exception:
        pass

    # Add photo column
    try:
        conn.execute("ALTER TABLE students ADD COLUMN photo TEXT DEFAULT 'default.png'")
    except Exception:
        pass

    # Default Subjects
    default_subjects = [
        "Java",
        "C++",
        "Python",
        "Operating Systems",
        "Data Structures",
        "Database Management Systems",
        "Computer Networks"
    ]

    for subject in default_subjects:
        try:
            conn.execute(
                "INSERT INTO subjects (name) VALUES (?)",
                (subject,)
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()


# Create Default Admin
def create_admin():

    conn = get_db()

    admin = conn.execute(
        "SELECT * FROM users WHERE username=?",
        ("admin",)
    ).fetchone()

    if admin is None:

        conn.execute(
            """
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
            """,
            ("admin", "admin123", "admin")
        )

        conn.commit()

    conn.close()


# Initialize Database
init_db()
create_admin()


if __name__ == "__main__":
    print("Database initialized successfully!")