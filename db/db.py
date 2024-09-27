import sqlite3
from flask import g
from models.response import Response
from models.form import Form

DATABASE = './database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    
    return db

def add_user_response(response: Response):
    pass

def get_form_metadata(form_id: int) -> Form:
    pass
