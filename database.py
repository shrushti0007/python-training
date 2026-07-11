import sqlite3
import os


# ---------------- DATABASE PATH ----------------

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "myproject.db"
)



# ---------------- DATABASE CONNECTION ----------------

def get_db():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn



# ---------------- CREATE TABLES ----------------

def init_db():

    conn = get_db()

    cursor = conn.cursor()


    # Students Table

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            subject TEXT NOT NULL,
            marks INTEGER,
            attendance INTEGER
        )
        """
    )


    # Users Table

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'student'
        )
        """
    )


    conn.commit()

    conn.close()



# ---------------- CREATE DEFAULT ADMIN ----------------

def create_admin():

    conn = get_db()


    admin = conn.execute(
        """
        SELECT * FROM users
        WHERE username=?
        """,
        ("admin",)
    ).fetchone()



    if admin is None:

        conn.execute(
            """
            INSERT INTO users
            (username,password,role)
            VALUES (?,?,?)
            """,
            (
                "admin",
                "admin123",
                "admin"
            )
        )


        conn.commit()


    conn.close()



# ---------------- DATABASE SETUP ----------------

if __name__ == "__main__":

    init_db()

    create_admin()

    print("Database initialized successfully!")