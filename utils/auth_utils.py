from app import db
from app.models import User
from flask_login import login_user, logout_user
from flask import flash, redirect, url_for

def register_user(form):
   
    user = User(username=form.username.data, email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Your account has been created! You are now able to log in', 'success')
    return redirect(url_for('auth.login'))

def login_user_logic(form):
   
    user = User.query.filter_by(email=form.email.data).first()
    if user and user.password == form.password.data:
        login_user(user)
        flash('You have been logged in!', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
        return None

def logout_user_logic():
    
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
