from flask import Flask, g, render_template, request, abort
from typing import Optional
from db.repository import Repository
from models.response import Response, ResponseChoice
from exceptions.NotFoundException import NotFoundException

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
    try:
        form = repo.get_form_with_questions(form_id)
    except NotFoundException:
        abort(404)

    return render_template('form_template.html', **form.__dict__)

@app.route("/form/<int:form_id>/submit", methods=["POST"])
def submit_form(form_id: int):
    repo = get_repository()

    try:
        response = None

        # TODO optimize so multiple responses are added before committing
        for form_key in request.form:
            if '-associated-text' not in form_key:
                question_id = form_key
                choice_id = request.form[question_id]

                # Each response is associated with exactly one question
                # So, when the question ID changes, create a new response
                if not response or str(response.question_id) != question_id:
                    response = Response(int(question_id))
                    response.response_id = repo.add_user_response(response)

                response_choice = ResponseChoice(
                    choice_id=int(choice_id),
                    response_id=response.response_id
                )

                if f'{choice_id}-associated-text' in request.form:
                    response_choice.associated_text = request.form[f'{choice_id}-associated-text']

                repo.add_user_response_choice(response_choice)

        return "Your responses have been submitted"
    except ValueError as e:
        print(e)
        return "There was an issue with one or more form values"
    
@app.teardown_appcontext
def close_repository(exception):
    repository = getattr(g, '_repository', None)
    if repository is not None:
        repository.close_connection()