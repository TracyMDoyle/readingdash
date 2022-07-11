from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import user, book

#Create Route Controller 
@app.route('/register')
def page_to_register_user():
    return render_template("register.html")

@app.route("/create/user", methods=["POST"])
def register_user():
    if user.User.create_user(request.form):
        return redirect('/dashboard')
    return redirect ("/register")

#Read Route Controller
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/dashboard")
def user_dashboard():
    this_user = user.User.get_user_by_id(session['user_id'])
    the_users_books = book.Book.users_books_by_id()
    return render_template("dashboard.html" , this_user=this_user, the_users_books=the_users_books)

@app.route("/users/login", methods=['POST'])
def login(): 
    if user.User.login(request.form): 
        return redirect("/users/dashboard")
    return redirect('/')
    
#Update Route Controller

#Delete Route Controller 
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')