from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_db, init_db


app = Flask(__name__)

app.secret_key = "polytechnic_hingoli_secret_key"



# ---------------- HOME PAGE ----------------

@app.route("/")
def home():

    return render_template(
        "home.html"
    )



# ---------------- ABOUT PAGE ----------------

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )

# ---------------- SUBJECTS PAGE ----------------

@app.route("/subjects")
def subjects():

    return render_template(
        "subjects.html"
    )


# ---------------- STUDENTS PAGE ----------------

@app.route("/students")
def students():

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()


    return render_template(
        "students.html",
        students=students
    )



# ---------------- STUDENT DETAIL PAGE ----------------

@app.route("/detail/<int:id>")
def detail(id):

    conn = get_db()


    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()


    conn.close()


    return render_template(
        "detail.html",
        student=student
    )



# ---------------- ADD STUDENT PAGE ----------------

@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]
        subject = request.form["subject"]
        marks = request.form["marks"]
        attendance = request.form["attendance"]


        conn = get_db()


        conn.execute(
            """
            INSERT INTO students
            (name, roll, subject, marks, attendance)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                roll,
                subject,
                marks,
                attendance
            )
        )


        conn.commit()
        conn.close()


        flash(
            "Student added successfully!",
            "success"
        )


        return redirect(
            "/students"
        )


    return render_template(
        "add_student.html"
    )

# ---------------- EDIT STUDENT ----------------

@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    conn = get_db()


    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]
        subject = request.form["subject"]
        marks = request.form["marks"]
        attendance = request.form["attendance"]


        conn.execute(
            """
            UPDATE students
            SET name=?,
                roll=?,
                subject=?,
                marks=?,
                attendance=?
            WHERE id=?
            """,
            (
                name,
                roll,
                subject,
                marks,
                attendance,
                id
            )
        )


        conn.commit()
        conn.close()


        flash(
            "Student updated successfully!",
            "success"
        )


        return redirect("/students")



    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()


    conn.close()


    return render_template(
        "edit_student.html",
        student=student
    )




# ---------------- DELETE STUDENT ----------------

@app.route("/delete_student/<int:id>")
def delete_student(id):

    conn = get_db()


    conn.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )


    conn.commit()
    conn.close()


    flash(
        "Student deleted successfully!",
        "danger"
    )


    return redirect("/students")




# ---------------- FILTER STUDENTS ----------------

@app.route("/filter", methods=["GET", "POST"])
def filter_students():

    students = []


    if request.method == "POST":

        subject = request.form["subject"]


        conn = get_db()


        students = conn.execute(
            """
            SELECT * FROM students
            WHERE subject LIKE ?
            """,
            (
                "%" + subject + "%",
            )
        ).fetchall()


        conn.close()



    return render_template(
        "filter.html",
        students=students
    )



# ---------------- LOGIN PAGE ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]


        conn = get_db()


        user = conn.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=?
            """,
            (
                username,
                password
            )
        ).fetchone()


        conn.close()



        if user:

            session["username"] = user["username"]
            session["role"] = user["role"]


            flash(
                "Login successful!",
                "success"
            )


            return redirect("/")

        else:

            flash(
                "Invalid username or password",
                "danger"
            )



    return render_template(
        "login.html"
    )

# ---------------- REGISTER PAGE ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        role = request.form.get(
            "role",
            "student"
        )


        conn = get_db()


        existing_user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()



        if existing_user:

            conn.close()

            flash(
                "Username already exists!",
                "danger"
            )

            return redirect(
                "/register"
            )



        conn.execute(
            """
            INSERT INTO users
            (username, password, role)
            VALUES (?, ?, ?)
            """,
            (
                username,
                password,
                role
            )
        )


        conn.commit()
        conn.close()


        flash(
            "Registration successful!",
            "success"
        )


        return redirect(
            "/login"
        )



    return render_template(
        "register.html"
    )




# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()


    flash(
        "Logged out successfully!",
        "success"
    )


    return redirect(
        "/login"
    )




# ---------------- CHECK ADMIN ----------------

@app.route("/admin")
def admin():

    if "username" not in session:

        flash(
            "Please login first!",
            "danger"
        )

        return redirect(
            "/login"
        )



    if session.get("role") != "admin":

        flash(
            "Admins only! You do not have permission.",
            "danger"
        )

        return redirect(
            "/"
        )



    return render_template(
        "admin.html"
    )




# ---------------- START APPLICATION ----------------

if __name__ == "__main__":

    init_db()


    app.run(
        debug=True
    )