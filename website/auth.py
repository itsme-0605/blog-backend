from flask import Blueprint, render_template,request,flash,redirect,url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import login_user, logout_user, login_required, current_user

#usermixin is used so that we can use current user


auth=Blueprint("auth",__name__)

@auth.route("/login",methods=['GET','POST'])
def login():
  
  if request.method =='POST':
    email=request.form.get('email')
    password1=request.form.get('password')
   
    #filter all users that have the entered email.
    user=User.query.filter_by(email=email).first()
   
    if user:
      print('hi')
      if password1 is not None and check_password_hash(user.password, password1):
        flash('Logged in successfully',category='success')
        login_user(user,remember=True)
        return redirect(url_for('views.home'))
      else: 
        flash('Incorrect password,try again',category='error')
    else:
          flash('Email does not exist',category='error')

  return render_template("login.html",user=current_user)

@auth.route("/sign-up",methods=['GET','POST'])
def sign_up():

  if request.method =='POST':
    email=request.form.get('email')
    username=request.form.get('username')
    password1=request.form.get('password1')
    password2=request.form.get('password2')   

    user=User.query.filter_by(email=email).first()

    if user:
      flash('user already exists',category='error')
    if email is None or len(email) < 4 :
      flash('Email must be greater than 3 characters.',category='error')
    elif username is  None or len(username) < 2:
       flash('Username must be greater than 1 characters.',category='error')
    elif password1!=password2:
        flash('Passwords don\'t match.', category='error')
    elif password1 is None or len(password1) < 7:
        flash('Password must be at least 7 characters.', category='error')
    else:
      hashed_password = generate_password_hash(password1, method='pbkdf2', salt_length=16)
      new_user = User(email=email, username=username, password=hashed_password)
      db.session.add(new_user)
      db.session.commit()
      login_user(user,remember=True)
      flash('Account created!', category='success')
      return redirect(url_for('views.home')) #url for will pick up the url for views.home
      
  return render_template("sign_up.html",user=current_user)



@auth.route("/logout")
@login_required    #cannot access this page until the user is logged in
def logout():
  logout_user()
  return redirect(url_for('auth.login')) 