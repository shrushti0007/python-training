# ---------------- IMPORT DATABASE FUNCTIONS ----------------

from database import init_db, create_admin



# ---------------- INITIALIZE DATABASE ----------------

init_db()

# ---------------- CREATE ADMIN USER ----------------

create_admin()



# ---------------- SUCCESS MESSAGE ----------------

print(
    "Database created successfully!"
)