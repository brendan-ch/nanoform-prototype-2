from flask import g
from models.response import Response, ResponseChoice
from models.form import Form
from models.form_question import FormQuestion
from models.form_question_with_choices import FormQuestionWithChoices
from models.question_choice import QuestionChoice
from models.form_with_questions import FormWithQuestions
from dataclasses import field, fields
from exceptions.NotFoundException import NotFoundException
import sqlite3

DATABASE = './database.db'

def filter_dict_for_dataclass(data: dict, cls) -> dict:
    """Filter dictionary to match the dataclass fields."""
    return {k: v for k, v in data.items() if k in {field.name for field in fields(cls)}}

class Repository():
    def __init__(self, connection = None):
        if not connection:
            self.connection = sqlite3.connect(DATABASE, check_same_thread=False)
        else:
            self.connection = connection

        self.connection_is_open = True

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
        cursor = self.connection.cursor()
        cursor.row_factory = sqlite3.Row
        query = '''
        SELECT form_title, form_description, form_id
        FROM form
        WHERE form_id = ?
        '''

        params = (form_id,)
        cursor.execute(query, params)
        result = cursor.fetchone()

        if not result:
            raise NotFoundException

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
        SELECT
            choice.choice_id,
            choice.choice_name,
            choice.choice_position,
            choice.has_free_response_field,
            choice.question_id,
            q.question_type,
            q.question_name,
            q.form_id,
            q.question_position
        FROM choice
        INNER JOIN (SELECT question_type, question_name, question_id, form_id, question_position
            FROM question
            WHERE form_id = ?
            ORDER BY question_position ASC) q
            ON q.question_id = choice.question_id;
        '''

        cursor = self.connection.cursor()
        cursor.row_factory = sqlite3.Row
        params = (form_id,)
        cursor.execute(get_questions_query, params)
        results = cursor.fetchall()

        questions: dict[int, FormQuestionWithChoices] = {}
        for result in results:
            result_for_question = filter_dict_for_dataclass(dict(**result), FormQuestion)
            question = FormQuestionWithChoices(**result_for_question)
            if question.question_id not in questions:
                questions[question.question_id] = question

            if not questions[question.question_id].choices:
                questions[question.question_id].choices = []

            result_for_choice = filter_dict_for_dataclass(dict(**result), QuestionChoice)
            questions[question.question_id].choices.append(QuestionChoice(**result_for_choice))

        form_with_questions.questions = list(questions.values())
        return form_with_questions

    def close_connection(self):
        self.connection.close()
        self.connection_is_open = False
