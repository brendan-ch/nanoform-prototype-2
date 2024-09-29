from flask import g
from models.response import Response, ResponseChoice
from models.form import Form
from models.form_question import FormQuestion
from models.question_choice import QuestionChoice
import sqlite3

DATABASE = './database.db'

class Repository():
    def __init__(self, connection = sqlite3.connect(DATABASE, check_same_thread=False)):
        self.connection = connection

    def add_form(self, form: Form):
        cursor = self.connection.cursor()
        query = """
            INSERT INTO form (form_title, form_description)
            VALUES (?, ?)
        """
        params = (form.title, form.description)

        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(e)


    def add_question(self, question: FormQuestion):
        cursor = self.connection.cursor()
        query = '''
        INSERT INTO question (form_id, question_name, question_type)
        VALUES (?, ?, ?)
        '''

        params = (question.form_id, question.question_name, question.question_type.value)
        
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            return ValueError(e)

    def add_question_choice(self, question_choice: QuestionChoice):
        pass
    
    def add_user_response(self, response: Response):
        pass

    def add_user_response_choice(self, response_choice: ResponseChoice):
        pass

    def get_form_metadata(self, form_id: int) -> Form:
        pass

    def close_connection(self):
        self.connection.close()
