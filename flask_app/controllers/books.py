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
@app.route("/read/<int:id>")
def read_a_book_log(id):
    the_book_log = book.Book.get_a_book_by_id(id)
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template("book.html", the_book_log=the_book_log, this_user=this_user)

#Update Route Controller
@app.route("/edit/<int:id>")
def render_page_to_edit_book(id):
    the_book = book.Book.get_a_book_by_id(id)
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template("edit.html", the_book=the_book, this_user=this_user)

@app.route("/updated", methods = ["POST"])
def updated_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if book.Book.update_book_log_by_id(request.form) == True:
        return redirect("/users/dashboard")
    return render_template("edit.html", the_book=request.form)


#Delete Route Controller
#delete recipes
@app.route('/delete/<int:id>')
def delete_book_log(id):
    this_book=book.Book.get_a_book_by_id(id)
    if this_book["users_id"] == session["user_id"]:
        book.Book.delete_book_by_id(id)
        return redirect("/users/dashboard")
    else:
        return render_template('/naughty.html')
