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
        cursor = self.connection.cursor()
        query = '''
        INSERT INTO choice (question_id, choice_name, choice_position, has_free_response_field)
        VALUES (?, ?, ?, ?)
        '''

        params = (
            question_choice.question_id,
            question_choice.choice_name,
            question_choice.choice_position,
            question_choice.has_free_response_field
        )
        
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            return ValueError(e)
    
    def add_user_response(self, response: Response):
        cursor = self.connection.cursor()
        query = '''
        INSERT INTO response (time_submitted, question_id)
        VALUES (?, ?)
        '''

        params = (response.timestamp, response.question_id)
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            return ValueError(e)

    def add_user_response_choice(self, response_choice: ResponseChoice):
        cursor = self.connection.cursor()
        query = '''
        INSERT INTO response_choice (choice_id, response_id, associated_text)
        VALUES (?, ?, ?)
        '''

        params = (response_choice.choice_id, response_choice.response_id, response_choice.associated_text)
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            return ValueError(e)

    def get_form_metadata(self, form_id: int) -> Form:
        pass

    def close_connection(self):
        self.connection.close()
