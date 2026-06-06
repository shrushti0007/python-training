from flask import Flask

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return  "<h1>EXAM LEAK DETECTION & TRANSPARENCY PLATFORM</H1>"

# About page
@app.route('/about')
def about():
    return """
    <h1>About Us</h1>
    <p>This project Helps Users Report Exam-related Issues</p>
    <a href="/">Back to Home</a>
    """

# Report page
@app.route('/students')
def students():

    reports = [
        {
            "reports_id": "ELD-001",
            "exam_name": "MSBTE Summer 2026",
            "subject_name": "MICROPROCESSOR PROGRAMMING",
            "college_name": "Goverment Polytechnic Hingoli",
            "status": "pending",
            "report_date": "01-06-2026",

        },
        {
            "reports_id": "ELD-002",
            "exam_name": "MSBTE Summer 2026",
            "subject_name": "Data Structure",
            "college_name": "Goverment Polytechnic Hingoli",
            "status": "Resolved",
            "report_date": "02-06-2026"
        },

        {
            "reports_id": "ELD-003",
            "exam_name": "MSBTE Summer 2026",
            "subject_name": "DATABASE MANAGEMENT SYSTEM",
            "college_name": "Goverment Polytechnic Hingoli",
            "status": "Resolved",
            "report_date": "03-06-2026",
        },   
        {
            "reports_id": "ELD-004",
            "exam_name": "MSBTE Summer 2026",
            "subject_name": "DTE",
            "college_name": "Goverment Polytechnic Hingoli",
            "status": "pending",
            "report_date": "04-06-2026"
        }
    ]
    html = "<h1>Exam Leak Reports</h1><ul>"
    for r in reports:
        html += f"<li>{r['exam_name']} - {r['subject_name']} - {r['status']}</li>"
    html += """
     </ul>

     <form> 
             Exam Name:<br>
             <input type="text"><br><br>

             Subject Name:<br>
             <input type="text"><br><br>

             College Name:<br>
             <input type="text"><br><br>

             Status:<br>
             <input type="text"><br><br>

             Report Date:<br>
             <input type="text"><br><br>

             Issue Description:<br>
             <textarea rows="5" cols="30"></textarea><br><br>

             <input type="submit" value="Submit Report">
        </form>

        <br>
        <a href="/">Back to Home</a>
        """

    return html
    
print("STARTING FLASK")
print(__name__)

if __name__ == '__main__':
    print("INSIDE MAIN")
    app.run(debug=True)
    