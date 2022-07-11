from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import user

class User:
    """This user class sets up student reading information by their books."""

    db = "reading_dash" 
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.author = data["author"]
        self.rating = data["rating"]
        self.date_completed = data["date_completed"]
        self.genre = data["genre"]
        self.summary = data["summary"]
        self.created_at = data['created_at']
        self.updated_at = data['created_at']

    #create model SQL
    @classmethod
    def create_book_log():
        pass

    #read model SQL


    #update model SQL

    
    #delete model SQL