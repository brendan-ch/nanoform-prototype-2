from flask import Flask, render_template, request
# from markupsafe import escape

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        print("Form data submitted to server")
        return 'Form submitted'
    else:
        return render_template("sample.html")
