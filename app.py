from flask import Flask, g, render_template, request
from typing import Optional
from db.repository import Repository

app = Flask(__name__)

def get_repository():
    repository: Optional[Repository] = getattr(g, '_repository', None)
    if not repository or not repository.connection_is_open:
        repository = g._repository = Repository()
    return repository

# TODO change this to a landing page or something
@app.route("/")
def index():
    # if request.method == 'POST':
    #     print("Form data submitted to server")
    #     return 'Form submitted'
    # else:
    return render_template("sample.html")

@app.route("/form/<int:form_id>")
def show_form(form_id: int):
    repo = get_repository()
    # TODO add improved error handling, check if the form exists
    form = repo.get_form_with_questions(form_id)
    return render_template('form_template.html', **form.__dict__)
    
@app.teardown_appcontext
def close_repository(exception):
    repository = getattr(g, '_repository', None)
    if repository is not None:
        repository.close_connection()