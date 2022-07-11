from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import book
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
PASSWORD_REGEX=re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$") 

class User:
    """This user class sets up student information."""

    db = "reading_dash" 
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.grade = data["grade"]
        self.school = data["school"]
        self.teacher_name = data["teacher_name"]
        self.user_name = data["user_name"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_books = [] 

    # Create - models - SQL
    @classmethod 
    def create_user(cls, data):
        if not cls.validate_user(data):
            return False
        else:
            data = cls.parse_registration_data(data)
            query = """
            INSERT INTO users 
            (first_name, last_name, grade, school, teacher_name, user_name, password)
            VALUES
            (%(first_name)s, %(last_name)s, %(grade)s, %(school)s, %(teacher_name)s, %(user_name)s, %(password)s)
            ;"""
            user_id = connectToMySQL(cls.db).query_db(query,data)
            session["user_id"] = user_id
            return user_id
    

    # Read - models - SQL
    @classmethod
    def get_user_by_user_name(cls, user_name):
        data = {"user_name" : user_name}
        query = """
        SELECT * 
        FROM users
        WHERE user_name = %(user_name)s
        ;"""
        user = MySQLConnection(cls.db).query_db(query, data)
        if user:
            user = cls(user[0])
        return user

    @classmethod
    def get_user_by_id(cls, id):
        data = {"id" : id}
        query = """
        SELECT * 
        FROM users
        WHERE id = %(id)s
        ;"""
        user = MySQLConnection(cls.db).query_db(query, data)
        if user:
            user = cls(user[0])
        return user
    # Update - models - SQL
    

    # Delete - models - SQL

    # Parse Data - models - SQL
    @staticmethod
    def parse_registration_data(data):
        parsed_data = {}
        parsed_data ["first_name"] = data["first_name"]
        parsed_data ["last_name"] = data["last_name"]
        parsed_data ["user_name"] = data ["user_name"]
        parsed_data ["grade"] = data["grade"]
        parsed_data ["school"] = data["school"]
        parsed_data ["teacher_name"] = data["teacher_name"]

        parsed_data ["password"] = bcrypt.generate_password_hash(data["password"])
        return parsed_data 

    # Validate - models - SQL
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters long.")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters long.")
            is_valid = False
        if data["grade"] == "":
            flash("You must enter your grade level")
            is_valid = False
        if len(data["school"]) < 2:
            flash("School name must be at least 2 characters long")
            is_valid = False
        if len(data["teacher_name"]) < 2:
            flash("Teacher must be at least 2 characters long")
            is_valid = False
        if User.get_user_by_user_name(data["user_name"]):
            flash("User name is already registered")
            is_valid = False
        if len(data["user_name"]) < 5:
            flash("User Name must be at least 5 characters long")
            is_valid = False
        if not PASSWORD_REGEX.match(data["password"]):
            flash("Your password must be 8 characters and contain at least one uppercase letter, a number, and a lowercase letter")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Passwords do not match")
            is_valid = False
        return is_valid
    
    @staticmethod
    def login(data):
        this_user=User.get_user_by_user_name(data["user_name"])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data["password"]):
                print(this_user)
                session["user_id"] = this_user.id
                return True
        flash("Your login info is incorrect")
        return False
