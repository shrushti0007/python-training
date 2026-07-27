from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
 
load_dotenv() #load environment variables from .env file

from database import get_db, init_db


# Groq AI Import

import os

from groq import Groq



# ==========================
# FLASK APP
# ==========================

app = Flask(__name__)


app.secret_key = "linkkiwi2026"


# Upload Folder
UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# ==========================
# GROQ AI CLIENT
# ==========================

client = Groq(api_key=os.environ.get("GROQ_API_KEY","GROQ_API_KEY=YOUR_GROQ_API_KEY")

)





# ==========================
# INITIALIZE DATABASE
# ==========================

init_db()
# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():

    conn = get_db()


    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()



    total = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]



    passed = conn.execute(
        "SELECT COUNT(*) FROM students WHERE marks >= 45"
    ).fetchone()[0]



    excellent = conn.execute(
        "SELECT COUNT(*) FROM students WHERE marks >= 90"
    ).fetchone()[0]



    conn.close()



    return render_template(
        "home.html",
        students=students,
        total=total,
        passed=passed,
        excellent=excellent
    )





# ==========================
# STUDENTS LIST
# ==========================

@app.route("/students")
def students_page():

    conn = get_db()



    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()



    conn.close()



    return render_template(
        "students.html",
        students=students
    )
# ==========================
# STUDENT DETAIL
# ==========================

@app.route("/students/<int:id>")
def student_detail(id):

    conn = get_db()


    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()


    conn.close()



    if student is None:

        flash(
            "Student not found",
            "danger"
        )

        return redirect(
            url_for("students_page")
        )



    return render_template(
        "detail.html",
        student=student
    )





# ==========================
# ADD STUDENT
# ==========================

@app.route("/add", methods=["GET", "POST"])
def add_student():


    if session.get("role") != "admin":

        flash(
            "Admins only!",
            "danger"
        )

        return redirect(
            url_for("home")
        )



    if request.method == "POST":


        name = request.form["student_name"]

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
                int(marks),
                int(attendance)
            )
        )



        conn.commit()
        conn.close()

    

        # Photo
        file = request.files.get("photo")
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = get_db()

        conn.execute("""
            INSERT INTO students
            (name, roll, subject, marks, attendance, photo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            roll,
            subject,
            int(marks),
            int(attendance),
            filename
        ))

        conn.commit()
        conn.close()

        flash("Student added successfully!", "success")
        return redirect(url_for("students_page"))

    return render_template("add_students.html")

# ==========================
# EDIT STUDENT
# ==========================

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):


    if session.get("role") != "admin":

        flash(
            "Admins only!",
            "danger"
        )

        return redirect(
            url_for("home")
        )



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
            SET
            name=?,
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
                int(marks),
                int(attendance),
                id
            )
        )



        conn.commit()

        conn.close()



        flash(
            "Student updated successfully!",
            "success"
        )



        return redirect(
            url_for("students_page")
        )




    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()



    conn.close()



    if student is None:

        abort(404)



    return render_template(
        "edit_student.html",
        student=student
    )







# ==========================
# DELETE STUDENT
# ==========================

@app.route("/delete/<int:id>")
def delete_student(id):


    if session.get("role") != "admin":

        flash(
            "Admins only!",
            "danger"
        )

        return redirect(
            url_for("home")
        )



    conn = get_db()



    student = conn.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()



    if student is None:

        conn.close()

        flash(
            "Student not found!",
            "danger"
        )

        return redirect(
            url_for("students_page")
        )



    conn.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )



    conn.commit()

    conn.close()



    flash(
        "Student deleted successfully!",
        "success"
    )



    return redirect(
        url_for("students_page")
    )

# ==========================
# SEARCH STUDENT
# ==========================

@app.route("/search")
def search():


    q = request.args.get(
        "q",
        ""
    )



    conn = get_db()



    if q:


        students = conn.execute(
            """
            SELECT *
            FROM students
            WHERE
            name LIKE ?
            OR subject LIKE ?
            OR roll LIKE ?
            ORDER BY id DESC
            """,
            (
                f"%{q}%",
                f"%{q}%",
                f"%{q}%"
            )
        ).fetchall()



    else:


        students = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()



    conn.close()



    return render_template(
        "search.html",
        students=students,
        query=q
    )







# ==========================
# FILTER STUDENTS
# ==========================

@app.route("/filter")
def filter_students():


    subject = request.args.get(
        "subject",
        ""
    )


    grade = request.args.get(
        "grade",
        ""
    )



    conn = get_db()



    subjects = conn.execute(
        """
        SELECT DISTINCT subject
        FROM students
        WHERE subject IS NOT NULL
        ORDER BY subject
        """
    ).fetchall()



    query = "SELECT * FROM students WHERE 1=1"


    params = []



    if subject:

        query += " AND subject=?"

        params.append(subject)



    if grade == "excellent":

        query += " AND marks>=90"



    elif grade == "good":

        query += " AND marks>=75 AND marks<90"



    elif grade == "average":

        query += " AND marks>=60 AND marks<75"



    elif grade == "poor":

        query += " AND marks<45"




    query += " ORDER BY id DESC"



    students = conn.execute(
        query,
        params
    ).fetchall()



    conn.close()



    return render_template(
        "filter.html",
        students=students,
        subjects=subjects,
        selected_subject=subject,
        selected_grade=grade
    )







# ==========================
# ABOUT PAGE
# ==========================

@app.route("/about")
def about():


    return render_template(
        "about.html"
    )

# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():


    if request.method == "POST":


        username = request.form["username"].strip()

        password = request.form["password"]




        conn = get_db()



        existing = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()



        if existing:

            conn.close()


            flash(
                "Username already exists!",
                "danger"
            )


            return render_template(
                "register.html"
            )




        hashed_password = generate_password_hash(
            password
        )




        conn.execute(
            """
            INSERT INTO users
            (username, password, role)
            VALUES (?, ?, ?)
            """,
            (
                username,
                hashed_password,
                "student"
            )
        )



        conn.commit()

        conn.close()



        flash(
            "Registration successful! Please login.",
            "success"
        )



        return redirect(
            url_for("login")
        )



    return render_template(
        "register.html"
    )

# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():


    if request.method == "POST":


        username = request.form["username"].strip()

        password = request.form["password"]




        conn = get_db()



        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()



        conn.close()





        if user and check_password_hash(
            user["password"],
            password
        ):



            session["username"] = username

            session["role"] = user["role"]




            flash(
                f"Welcome {username}!",
                "success"
            )



            return redirect(
                url_for("home")
            )




        flash(
            "Invalid username or password",
            "danger"
        )



    return render_template(
        "login.html"
    )







# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():


    session.pop(
        "username",
        None
    )



    session.pop(
        "role",
        None
    )



    flash(
        "Logged out successfully.",
        "info"
    )



    return redirect(
        url_for("home")
    )


# ==========================
# SUBJECTS PAGE
# ==========================

@app.route("/subjects")
def subjects():

    conn = get_db()



    rows = conn.execute(
        """
        SELECT
            subjects.name AS subject_name,
            COUNT(students.id) AS student_count
        FROM subjects
        LEFT JOIN students
        ON students.subject = subjects.name
        GROUP BY subjects.name
        ORDER BY subjects.name
        """
    ).fetchall()



    conn.close()



    return render_template(
        "subjects.html",
        rows=rows
    )








# ==========================
# STREAMS PAGE
# ==========================

@app.route("/streams")
def streams():

    conn = get_db()



    streams = conn.execute(
        """
        SELECT DISTINCT subject
        FROM students
        WHERE subject IS NOT NULL
        ORDER BY subject
        """
    ).fetchall()



    conn.close()



    return render_template(
        "streams.html",
        streams=streams
    )









# ==========================
# ADMIN PAGE
# ==========================

@app.route("/admin")
def admin():


    if session.get("role") != "admin":


        flash(
            "Admins only!",
            "danger"
        )


        return redirect(
            url_for("home")
        )




    conn = get_db()



    users = conn.execute(
        "SELECT id, username, role FROM users"
    ).fetchall()



    conn.close()




    return render_template(
        "admin.html",
        users=users
    )









# ==========================
# 404 ERROR PAGE
# ==========================

@app.errorhandler(404)
def page_not_found(error):


    return render_template(
        "404.html"
    ),404









# ==========================
# START APPLICATION
# ==========================

if __name__ == "__main__":


    init_db()


    app.run(
        debug=True
    )