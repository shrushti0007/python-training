from flask import Flask, render_template, request, flash

from database import get_db, init_db # importing the database connection function

app = Flask(__name__)
app.secret_key = "linkkiwi" # Needed for flashing messages

students = [
    {"name": "Tanuja", "roll": 1, "marks": 85},
    {"name": "Pratiksha", "roll": 2, "marks": 78},
    {"name": "Shalok", "roll": 3, "marks": 92},
    {"name": "Lucky", "roll": 4, "marks": 65},
]


@app.route("/")
def home():
    return render_template("home.html", students=students)

@app.route('/about')
def about():
    return render_template('about.html', students=students)

    return render_template('students.html', students=students)







@app.route("/add", methods=["GET", "POST"])
def add_student(): 
    if request.method == "POST":
        name = request.form["student_name"]
        marks = request.form["marks"]
        roll = request.form["roll"]
        subject = request.form["subject"]
        attendance = request.form["attendance"]
        if not name or not marks:
            flash('please provide both name and marks.' 'danger')
            return render_template("add_student.html")
        
        conn = get_db()
        conn.execute('''INSERT INTO students
                    (name,roll,marks,subject,attendance) VALUES(?,?,?,?,?)''',
                    (name,roll, int(marks), subject, int(attendance))
                    )
        conn.commit()
        conn.close()

        #print to terminal
        print(f"Recived new student: {name} with marks: {marks}")
        # #new student dictionary
        new_student ={"name": name,"marks": int(marks)}
        students.append(new_student)
        #Flask message to user
        flash(f"Student {name} added successfully!", "success")
        print(f"Updated students list: {students}")
    return render_template('add_students.html')
  
if __name__ == '__main__':
    app.run(debug=True)
    
    