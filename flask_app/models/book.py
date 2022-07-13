from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import user

class Book:
    """This class sets up student reading information by their books."""

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
        self.a_users_books = None

    #create model SQL
    @classmethod
    def create_book_log(cls, data):
        if not cls.validate_book_add(data):
            return False
        else:
            query = """
            INSERT INTO books
            (title, author, rating, date_completed, genre, summary, users_id)
            VALUES (%(title)s, %(author)s, %(rating)s, %(date_completed)s, %(genre)s, %(summary)s, %(users_id)s)
            ;"""
            new_book_id = connectToMySQL(cls.db).query_db(query, data)
            print("++++++++*****************",new_book_id,)
            return new_book_id

    # read model SQL
    @classmethod
    def users_books_by_id(cls):
        query = """
        SELECT * FROM books
        LEFT JOIN users
        ON users.id = books.users_id
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        the_users_book_list = []
        for db_row_books in result:
            user_books = cls(db_row_books)
            book_dictionary= {
                "id" : db_row_books["users.id"],
                "first_name":db_row_books['first_name'],
                "last_name": db_row_books['last_name'],
                'user_name': db_row_books['user_name'], 
                'password': db_row_books['password'],
                'grade': db_row_books['grade'],
                'school': db_row_books['school'],
                'teacher_name': db_row_books['teacher_name'],
                'created_at': db_row_books["users.created_at"], 
                'updated_at': db_row_books["users.updated_at"],
                

                # "id" : db_row_books["books.id"],
                # "title" : db_row_books["title"],
                # "author" : db_row_books["author"],
                # "rating" : db_row_books["rating"],
                # "date_completed" : db_row_books["date_completed"],
                # "genre" : db_row_books["genre"],
                # "summary" : db_row_books["summary"],
                # "created_at" : db_row_books["books.created_at"],
                # "updated_at" : db_row_books["books.updated._at"]
            }
            user_books.a_users_books = user.User(book_dictionary)
            the_users_book_list.append(user_books)
        return the_users_book_list

    #update model SQL


    #delete model SQL
    @classmethod
    def delete_book_by_id(cls, id):
        data = {"id" : id}
        query = """
        DELETE FROM books
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)


    #validate SQL book model
    @staticmethod
    def validate_book_add(data):
        is_valid = True
        if len(data['title']) < 3:
            flash("Title must be at least 3 characters")
            is_valid = False
        if len(data ["author"]) < 3:
            flash("Author must be at least 3 characters")
            is_valid = False
        if data["rating"] == "":
            flash("Please enter a rating")
            is_valid = False
        if data["date_completed"] == "":
            flash("Please enter a date")
            is_valid = False
        if len(data["genre"]) < 3:
            flash("Please enter genre")
            is_valid = False
        if len(data["summary"]) < 20:
            flash("Summary must be longer.")
            is_valid = False
        return is_valid
        
