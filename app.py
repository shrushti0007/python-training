from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
     return render_template("home.html")
@app.route('/students')
def students_page():
     return "Students page lavkar"

@app.route('/about')
def about():
     return "About page lavkar"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)   
