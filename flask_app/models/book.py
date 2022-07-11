from unittest import result
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import user

class Book:
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
    @classmethod
    def users_books_by_id(cls, id):
        data = {"id" : id}
        query = """
        SELECT * from users
        JOIN books
        ON user.id = books.user_id
        WHERE users.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db
        if result:
            user = cls(result[0])
            for books in result:
                data = {
                    "id" : books["books.id"],
                    "title" : books["title"],
                    "author" : books["author"],
                    "rating" : books["rating"],
                    "date_completed" : books["date_completed"],
                    "genre" : books["genre"],
                    "summary" : books["summary"],
                    "created_at" : books["books.created_at"],
                    "updated_at" : books["updated.created_at"]
                }
                user.books.append(cls(data))
        return user



    #update model SQL


    #delete model SQL