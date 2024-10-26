from flask import g
from models.response import Response, ResponseChoice
from models.form import Form
from models.form_question import FormQuestion
from models.form_question_with_choices import FormQuestionWithChoices
from models.question_choice import QuestionChoice
from models.form_with_questions import FormWithQuestions
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
        params = (form.form_title, form.form_description)

        try:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(e)


    def add_question(self, question: FormQuestion):
        cursor = self.connection.cursor()
        query = '''
        INSERT INTO question (form_id, question_name, question_type, question_position)
        VALUES (?, ?, ?, ?)
        '''

        params = (question.form_id, question.question_name, question.question_type.value, question.question_position)
        
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
        # TODO implement improved error handling
        # in case the form doesn't exist
        cursor = self.connection.cursor()
        query = '''
        SELECT form_title, form_description, form_id
        FROM form
        WHERE form_id = ?
        '''

        params = (form_id,)
        cursor.execute(query, params)
        result = cursor.fetchone()

        return Form(**result)

    def get_form_with_questions(self, form_id: int) -> FormWithQuestions:
        form = self.get_form_metadata(form_id)
        form_with_questions = FormWithQuestions(
            form_title=form.form_title,
            form_id=form.form_id,
            form_description=form.form_description,
            questions=[]
        )

        # If we're ever at a point where we need to get
        # individual questions, split this into a separate method/
        # write separate tests

        get_questions_query = '''
        SELECT question_type, question_name, question_id, form_id, question_position
        FROM question
        WHERE form_id = ?
        ORDER BY question_position ASC;
        '''

        cursor = self.connection.cursor()
        params = (form_id,)
        cursor.execute(get_questions_query, params)
        results = cursor.fetchall()

        form_with_questions.questions = [FormQuestionWithChoices(**result) for result in results]


        return form_with_questions

    def close_connection(self):
        self.connection.close()
