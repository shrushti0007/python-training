from flask import Flask 

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>college portal</h1>'

@app.route('/aboute')
def about():
    return '<h1>About Us</h1><p>This is a college management system.</p>'

@app.route('/students')
def students():
    return '<h1>Students</h1><p>All students will show here</p>'

if __name__ == '__main__':
    app.run(debug=True)
    

