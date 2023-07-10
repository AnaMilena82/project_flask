from flask import render_template, session,flash,redirect, request, url_for
import re
from flask_app import app
from flask import get_flashed_messages
from flask_app.models.model_magazines import Magazines
from flask_app.controllers import controller_users


@app.route('/dashboard',methods=['GET'])
def dashboard():
    if 'id' in session:
        list_magazines = Magazines.get_allmagazines_with_user()
        mensaje = get_flashed_messages(category_filter=['error_subscribe'])
        return render_template("magazines.html", list_magazines = list_magazines, mensaje=mensaje)
    return redirect('/')

@app.route('/new',methods=['GET'])
def get_new_magazine():
    if 'id' in session:
        return render_template("add_magazine.html")
    return redirect('/')      

@app.route('/new',methods=['POST'])
def post_new_magazine():
    data = {
        **request.form,
        "user_id": session['id']
    }
    if Magazines.validate_magazine(data) == False:
         return redirect('/new')
    else:
        id_magazine = Magazines.new_magazine(data)
        return redirect('/dashboard')

@app.route('/show/<int:id>',methods=['GET'])
def get_show_magazine(id):
    if 'id' in session:
        data = {
        "id": id
        }
        magazine = Magazines.show_one_magazine_with_user(data)
        subscribers = magazine.get_subscribers()
        return render_template("show_magazine.html", magazine = magazine, subscribers  = subscribers)
    return redirect('/')  

@app.route('/delete/<int:id>')
def delete_magazine(id):
    data = {
        "id": id
    }
    user_id = Magazines.get_user_id_by_magazine_id(id)
    print("Deleting magazine with ID:", id)
    Magazines.delete_one_magazine(data)
    return redirect(url_for('get_edit_user', id=user_id))



