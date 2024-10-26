import unittest
import sqlite3
from datetime import datetime
from db.repository import Repository
from models.form import Form
from models.response import Response, ResponseChoice
from models.form_question import FormQuestion, FormQuestionType
from models.question_choice import QuestionChoice
from models.form_with_questions import FormWithQuestions
from models.form_question_with_choices import FormQuestionWithChoices

class TestDbRepository(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(':memory:', check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.repository = Repository(self.connection)

        with open('./db/schema.sql', 'r') as schema_file:
            schema_sql = schema_file.read()
            self.connection.executescript(schema_sql)

    def tearDown(self):
        self.repository.close_connection()

    def test_add_form_and_return_row_id(self):
        sample_form = Form(
            form_title='Capybara interest survey',
            form_description='We\'d love to know your thoughts on capybaras! Please take a moment to answer the following questions.'
        )

        lastrowid = self.repository.add_form(sample_form)

        test_query = '''
        SELECT form_title, form_description, form_id
        FROM form;
        '''
        cursor = self.connection.cursor()
        cursor.execute(test_query)
        result = cursor.fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['form_title'], sample_form.form_title)
        self.assertEqual(result[0]['form_description'], sample_form.form_description)
        self.assertEqual(result[0]['form_id'], lastrowid)
    
    def test_add_multiple_forms(self):
        form1 = Form(form_title='Capybara interest survey', form_description='Tell us about your experience with capybaras.')
        form2 = Form(form_title='Capybara feedback', form_description='Provide feedback on our recent capybara event.')

        rowid1 = self.repository.add_form(form1)
        rowid2 = self.repository.add_form(form2)

        test_query = '''
        SELECT form_title, form_description
        FROM form;
        '''
        cursor = self.connection.cursor()
        cursor.execute(test_query)
        result = cursor.fetchall()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['form_title'], form1.form_title)
        self.assertEqual(result[0]['form_description'], form1.form_description)
        self.assertEqual(result[1]['form_title'], form2.form_title)
        self.assertEqual(result[1]['form_description'], form2.form_description)

        self.assertEqual(rowid1, 1)
        self.assertEqual(rowid2, 2)

    def test_add_form_rollback_on_failure(self):
        form1 = Form(form_title='Valid Form', form_description='Valid description')
        form2 = Form(form_title=None, form_description='Invalid Form')

        self.repository.add_form(form1)
        with self.assertRaises(ValueError):
            self.repository.add_form(form2)

        test_query = '''
        SELECT form_title, form_description
        FROM form;
        '''

        cursor = self.connection.cursor()
        cursor.execute(test_query)
        result = cursor.fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['form_title'], form1.form_title)

    def test_add_question(self):
        sample_form = Form(
            form_title='Capybara interest survey',
            form_description='We\'d love to know your thoughts on capybaras! Please take a moment to answer the following questions.'
        )

        form_id = self.repository.add_form(sample_form)

        sample_question = FormQuestion(
            question_name="How familiar are you with capybaras?",
            question_type=FormQuestionType.MULTIPLE_CHOICE,
            form_id=form_id
        )

        question_id = self.repository.add_question(sample_question)

        test_query = '''
        SELECT question_id, form_id, question_name, question_type
        FROM question;
        '''

        cursor = self.connection.cursor()
        cursor.execute(test_query)
        result = cursor.fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(question_id, result[0]['question_id'])
        self.assertEqual(result[0]['form_id'], form_id)
        self.assertEqual(result[0]['question_name'], sample_question.question_name)
        self.assertEqual(result[0]['question_type'], sample_question.question_type.value)

    def test_add_question_choice(self):
        sample_form = Form(
            form_title='Capybara interest survey',
            form_description='We\'d love to know your thoughts on capybaras! Please take a moment to answer the following questions.'
        )

        form_id = self.repository.add_form(sample_form)

        sample_question = FormQuestion(
            question_name="How familiar are you with capybaras?",
            question_type=FormQuestionType.MULTIPLE_CHOICE,
            form_id=form_id
        )

        question_id = self.repository.add_question(sample_question)

        sample_question_choice = QuestionChoice(
            choice_name="Very familiar",
            choice_position=0,
            has_free_response_field=False,
            question_id=question_id
        )

        question_choice_id = self.repository.add_question_choice(sample_question_choice)

        test_query = '''
        SELECT choice_name, choice_position, choice_id, has_free_response_field
        FROM choice
        '''

        cursor = self.connection.cursor()
        cursor.execute(test_query)
        result = cursor.fetchall()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(question_choice_id, result[0]['choice_id'])
        self.assertEqual(result[0]['choice_name'], sample_question_choice.choice_name)
        self.assertEqual(result[0]['choice_position'], sample_question_choice.choice_position)
        self.assertEqual(result[0]['has_free_response_field'], bool(sample_question_choice.has_free_response_field))

    def test_add_user_response_and_response_choice(self):
        sample_form = Form(
            form_title='Capybara interest survey',
            form_description='We\'d love to know your thoughts on capybaras! Please take a moment to answer the following questions.'
        )
        form_id = self.repository.add_form(sample_form)

        sample_question = FormQuestion(
            question_name="How familiar are you with capybaras?",
            question_type=FormQuestionType.MULTIPLE_CHOICE,
            form_id=form_id
        )
        question_id = self.repository.add_question(sample_question)

        sample_question_choice = QuestionChoice(
            choice_name="Very familiar",
            choice_position=0,
            has_free_response_field=False,
            question_id=question_id
        )
        question_choice_id = self.repository.add_question_choice(sample_question_choice)

        sample_response = Response(
            question_id=1,
        )
        response_id = self.repository.add_user_response(sample_response)

        sample_response_choice = ResponseChoice(
            choice_id=question_choice_id,
            response_id=response_id,
        )

        self.repository.add_user_response_choice(sample_response_choice)

        test_query = '''
        SELECT response.time_submitted, response.question_id, response.response_id, response_choice.choice_id
        FROM response
        INNER JOIN response_choice
        ON response_choice.response_id = response.response_id
        '''

        cursor = self.connection.cursor()
        cursor.execute(test_query)
        result = cursor.fetchall()

        self.assertEqual(len(result), 1)

        date_from_string = datetime.strptime(result[0]['time_submitted'], '%Y-%m-%d %H:%M:%S.%f')
        self.assertEqual(date_from_string, sample_response.timestamp)
        self.assertEqual(result[0]['question_id'], sample_response.question_id)
        self.assertEqual(result[0]['response_id'], sample_response_choice.response_id)
        self.assertEqual(result[0]['choice_id'], sample_response_choice.choice_id)

    def test_get_form_metadata(self):
        sample_form = Form(
            form_title='Capybara interest survey',
            form_description='We\'d love to know your thoughts on capybaras! Please take a moment to answer the following questions.'
        )

        query = '''
            INSERT INTO form (form_title, form_description)
            VALUES (?, ?)
        '''
        params = (sample_form.form_title, sample_form.form_description)

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        form_id = cursor.lastrowid

        form = self.repository.get_form_metadata(form_id)
        self.assertEqual(form.form_description, sample_form.form_description)
        self.assertEqual(form.form_title, sample_form.form_title)
        self.assertEqual(form.form_id, form_id)
    
    def test_get_form_metadata_not_found(self):
        sample_form = Form(
            form_title='Capybara interest survey',
            form_description='We\'d love to know your thoughts on capybaras! Please take a moment to answer the following questions.'
        )

        query = '''
            INSERT INTO form (form_title, form_description)
            VALUES (?, ?)
        '''
        params = (sample_form.form_title, sample_form.form_description)
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.rollback()

        # TODO introduce a more specific exception for this method
        form_id = 1
        with self.assertRaises(Exception):
            self.repository.get_form_metadata(form_id)

    def test_get_form_with_questions(self):
        # TODO check whether the method returns the exact same data model
        # TODO check whether question choices are returned in order

        sample_questions = [
            FormQuestionWithChoices(
                question_type=FormQuestionType.MULTIPLE_CHOICE,
                question_name='How familiar are you with capybaras?',
                choices=[
                    QuestionChoice(
                        choice_name='Very familiar',
                        choice_position=0,
                        has_free_response_field=False
                    ),
                    QuestionChoice(
                        choice_name='Somewhat familiar',
                        choice_position=1,
                        has_free_response_field=False
                    ),
                    QuestionChoice(
                        choice_name='Not familiar at all',
                        choice_position=2,
                        has_free_response_field=False
                    )
                ]
            ),
            FormQuestionWithChoices(
                question_type=FormQuestionType.MULTIPLE_CHOICE,
                question_name='What do you think of capybaras?',
                choices=[
                    QuestionChoice(
                        choice_name='Adorable',
                        choice_position=0,
                        has_free_response_field=False
                    ),
                    QuestionChoice(
                        choice_name='Calm and peaceful',
                        choice_position=1,
                        has_free_response_field=False
                    ),
                    QuestionChoice(
                        choice_name='Fascinating',
                        choice_position=2,
                        has_free_response_field=False
                    ),
                    QuestionChoice(
                        choice_name='I don\'t have a strong opinion',
                        choice_position=3,
                        has_free_response_field=False
                    ),
                    QuestionChoice(
                        choice_name='Other',
                        choice_position=4,
                        has_free_response_field=True
                    ),
                ]
            ),
        ]

        sample_form_with_questions = FormWithQuestions(
            form_title='Capybara interest survey',
            form_description='We\'d love to know your thoughts on capybaras! Please take a moment to answer the following questions.',
            questions=sample_questions
        )

        cursor = self.connection.cursor()
        insert_form_query = '''
            INSERT INTO form (form_title, form_description)
            VALUES (?, ?);
        '''
        params = (sample_form_with_questions.form_title, sample_form_with_questions.form_description)

        cursor.execute(insert_form_query, params)
        sample_form_with_questions.form_id = cursor.lastrowid

        insert_question_query = '''
            INSERT INTO question (form_id, question_name, question_type)
            VALUES (?, ?, ?);
        '''

        # TODO surely there's a better way to get a bunch of question IDs
        # from an executemany statement, rather than looping execute statements
        for question in sample_questions:
            params = (
                sample_form_with_questions.form_id,
                question.question_name,
                question.question_type.value,
            )

            cursor.execute(insert_question_query, params)
            question.question_id = cursor.lastrowid
            
            for choice in question.choices:
                choice.question_id = question.question_id

        insert_choice_query = '''
            INSERT INTO choice (choice_name, question_id, choice_position, has_free_response_field)
            VALUES (?, ?, ?, ?);
        '''
        for question in sample_questions:
            params = [
                (
                    choice.choice_name,
                    choice.question_id,
                    choice.choice_position,
                    choice.has_free_response_field
                )
                for choice in question.choices
            ]

            cursor.executemany(insert_choice_query, params)

        self.connection.commit()
