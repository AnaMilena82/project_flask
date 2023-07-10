from flask import render_template, session, request, redirect, flash, url_for, abort
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.model_users import User
from flask_app.models.model_magazines import Magazines
from flask_app.controllers import controller_subscriptions

bcrypt = Bcrypt( app )

@app.route( '/', methods = ['GET'] )
@app.route( '/login', methods = ['GET'] )
@app.route( '/register', methods = ['GET'] )
def get_login_register():
    return render_template( 'index.html' )

@app.route( '/register', methods = ['POST'] )
def new_user():
    if User.validate_register( request.form ) == True:
        encrypted_password = bcrypt.generate_password_hash( request.form['password'] )
        new_user = {
            **request.form,
            "password" : encrypted_password
        }

        user_id = User.new_one_user( new_user )
        
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['id'] = user_id
        return redirect( '/dashboard' )
    else:
        return redirect( '/' )
    
@app.route( '/login', methods = ['POST'] )
def login():
    data = {
        "email" : request.form['email_login'],
        "password" : request.form['password_login']
    }
    user = User.get_one_with_email( data )

    if User.validate_login( user ) == True:
        
        if not bcrypt.check_password_hash( user.password, data['password'] ):
            flash( "Incorrect Credentials.", "error_password_login")
            return redirect( '/login' );
        else:
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['id'] = user.id
            return redirect( '/dashboard' )
    else:
        return redirect( '/login' )

@app.route( '/logout' )
def logout():
    session.clear()
    return redirect( '/login' )


@app.route('/user/account/<int:id>',methods=['GET'])
def get_edit_user(id):
    if 'id' in session:
        data = {
        "id": id
        }
        user = User.show_one_user(data) 
        magazines = Magazines.get_magazines_by_user_id(session['id'])
        subscribed_magazines = {}

        for magazine in magazines:
            subscribers = controller_subscriptions.get_subscribers(magazine.id)
            subscribed_magazines[magazine.id] = subscribers
        print("cantidad: ",subscribed_magazines)
        return render_template("account.html", user = user, magazines = magazines, subscribed_magazines= subscribed_magazines )
    return redirect('/')  

@app.route('/user/account/<int:id>', methods = ['POST'])
def update_user(id):
    
    if User.validate_update(request.form) == False:
         return redirect(f'/user/account/{id}')
    else:
        data = {
            **request.form,
            "id": id
           
        }
        User.update_one_user(data)
        return redirect(f'/user/account/{id}')
    
@app.route('/user/subscribe/<int:magazine_id>')
def user_subscribe(magazine_id):
    if 'id' in session:
        user_id = session['id']
        result = controller_subscriptions.subscribe(user_id, magazine_id)
        if result:
            flash('Successfully subscribed to the magazine!', 'success')
            session['subscribe_message'] = {'magazine_id': magazine_id, 'message': 'Successfully subscribed to the magazine!'}
            return redirect('/dashboard')  
        else:
            flash('Unable to subscribe to the magazine.', 'error_subscribe')
            session['subscribe_message'] = {'magazine_id': magazine_id, 'message': 'Unable to subscribe to the magazine.'}
            return redirect('/dashboard')  
    
    return redirect('/login')
