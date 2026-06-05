from flask import Flask , render_template

app = Flask(__name__)

# project data - dictionary
stud = [
    { "name": "Shrushti", "roll": 1, "marks": 85},
    { "name": "Soham", "roll": 2, "marks": 92},
    {"name": "Ganagaprasad", "roll": 3, "marks": 78},
    {"name": "Aarti", "roll": 4, "marks": 65},
]

@app.route('/')
def home():
    # Crereate using HTMl
    html = '<h1>College Portal - Students</h1>'
    html += '<ul>'
    # Student list 
    for Student in stud:
        html += f'<li>{Student["name"]} - Roll: {Student["roll"]} - Maeks: {Student["marks"]}</li>'
    html += '</ul>'
    return html

@app.route('/aboute')
def about():
    return '<h1>About Us</h1><p>This is a college management system.</p>'

@app.route('/students')
def students():
    return '<h1>students</h1><p>All students will show here</p>'

if __name__ == '__main__':
    app.run(debug=True)
    
     

