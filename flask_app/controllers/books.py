from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import user
from flask_app.models import book

#Create Route Controller
@app.route('/add_book')
def render_page_to_add_book():
    if "user_id" not in session:
        return redirect('/')
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template("add.html", this_user=this_user)

@app.route("/book/add", methods = ["POST"])
def adds_book_to_user_dash():
    if "user_id" not in session:
        return redirect('/')
    if book.Book.create_book_log(request.form):
        return redirect("/users/dashboard")
    return redirect('/add_book')

#read Route Controller

#Update Route Controller
#Delete Route Controller