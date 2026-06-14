from flask import Flask, render_template

app = Flask(__name__)

students =[
    {"name": "Tanuja", "roll": 1, "marks": 85},
    {"name": "Pratiksha", "roll": 2, "marks": 78},
    {"name": "Shalok", "roll": 3, "marks": 92},
    {"name": "Lucky", "roll": 4, "marks": 65},
]

@app.route('/')
def home():
    return render_template('home.html',students=students)

@app.route('/students')
def students():
    return render_template('Students.html', students=students)

@app.route('/courses')
def courses():
    return "Courses Page"

if __name__ == '__main__':
    app.run(debug=True)
    
    