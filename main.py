from flask import Flask, g, render_template, request
from db.repository import Repository

app = Flask(__name__)

def get_repository():
    repository = getattr(g, '_repository', None)
    if not repository:
        repository = g._repository = Repository()
    return repository

@app.route("/", methods=["GET", "POST"])
def index():
    get_repository()
    if request.method == 'POST':
        print("Form data submitted to server")
        return 'Form submitted'
    else:
        return render_template("sample.html")
    
@app.teardown_appcontext
def close_repository(exception):
    repository = getattr(g, '_repository', None)
    if repository is not None:
        repository.close_connection()