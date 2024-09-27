from db import db
from flask import Flask, g, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    cur = db.get_db().cursor()
    print(cur)

    if request.method == 'POST':
        print("Form data submitted to server")
        return 'Form submitted'
    else:
        return render_template("sample.html")
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()