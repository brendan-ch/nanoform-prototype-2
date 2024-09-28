import unittest
import sqlite3
from db.repository import Repository
from models.response import Response

class TestDbRepository(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(':memory:', check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.repository = Repository(self.connection)

    def tearDown(self):
        self.repository.close_connection()

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