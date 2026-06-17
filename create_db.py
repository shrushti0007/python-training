import sqlite3

conn = sqlite3.connect('sample.db')

conn.execute('''CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll INTEGER NOT NULL,
            marks INTEGER NOT NULL,
            subject TEXT NOT NULL,
            attendance INTEGER DEFAULT 0)''')

conn.commit()
conn.close()
print("Database and table created successfully.")
