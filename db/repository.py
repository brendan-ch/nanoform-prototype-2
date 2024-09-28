from flask import g
from models.response import Response
from models.form import Form
from models.form_question import FormQuestion
from models.question_choice import QuestionChoice
import sqlite3

DATABASE = './database.db'

class Repository():
    def __init__(self, connection = sqlite3.connect(':memory:', check_same_thread=False)):
        self.connection = connection

    def add_form(self, form: Form):
        pass

    def add_question(self, question: FormQuestion):
        pass

    def add_question_choice(self, question_choice: QuestionChoice):
        pass
    
    def add_user_response(self, response: Response):
        pass

    def get_form_metadata(self, form_id: int) -> Form:
        pass

    def close_connection(self):
        self.connection.close()
