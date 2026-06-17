from flask import Flask,render_template, request,url_for,flash
app = Flask(__name__)
app.secret_key = "linkkiwi2026" # Needed for flash
@app.route("/")
def home():
    return '<h1>My Project</h1>'

if __name__ == "__main__":
    app.run(debug=True)