import unittest
import sqlite3
from db.repository import Repository
from models.form import Form
from models.response import Response

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

    def test_add_form(self):
        sample_form = Form(
            title='Capybara interest survey',
            description='We\'d love to know your thoughts on capybaras! Please take a moment to answer the following questions.'
        )

        self.repository.add_form(sample_form)

        test_query = '''
        SELECT form_title, form_description
        FROM form;
        '''
        cursor = self.connection.cursor()
        cursor.execute(test_query)
        result = cursor.fetchall()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['form_title'], sample_form.title)
        self.assertEqual(result[0]['form_description'], sample_form.description)
    
    def test_add_multiple_forms(self):
        form1 = Form(title='Capybara interest survey', description='Tell us about your experience with capybaras.')
        form2 = Form(title='Capybara feedback', description='Provide feedback on our recent capybara event.')

        self.repository.add_form(form1)
        self.repository.add_form(form2)

        test_query = '''
        SELECT form_title, form_description
        FROM form;
        '''
        cursor = self.connection.cursor()
        cursor.execute(test_query)
        result = cursor.fetchall()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['form_title'], form1.title)
        self.assertEqual(result[0]['form_description'], form1.description)
        self.assertEqual(result[1]['form_title'], form2.title)
        self.assertEqual(result[1]['form_description'], form2.description)

    def test_add_form_rollback_on_failure(self):
        form1 = Form(title='Valid Form', description='Valid description')
        form2 = Form(title=None, description='Invalid Form')

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
        self.assertEqual(result[0]['form_title'], form1.title)

    # add_user_response test cases
    # TODO write nominal test cases
    def test_add_user_response(self):
        pass

    # TODO write fail and edge cases for add_user_response
    # - attempted multiple concurrent calls to same method

    # get_form_metadata test cases
    # TODO write nominal test cases
    def test_get_form_metadata(self):
        pass

    # TODO write edge cases for get_form_metadata
    # - attempted multiple concurrent calls to same method