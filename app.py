from flask import Flask, render_template_string, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bestill', methods=["POST", "GET"])
def bestill():
    return render_template('bestill.html')

@app.route('/admin', methods=["POST", "GET"])
def admin():
    return render_template("admin.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('login.html', methods=["POST", "GET"])

@app.route('/register')
def register():
    return render_template('register.html', methods=["POST", "GET"])

if __name__ == "__main__":
    app.run()