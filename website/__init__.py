from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path


#object of db
db=SQLAlchemy()
DB_NAME='database.db'

def create_app():
  app=Flask(__name__)
  app.config['SECRET_KEY']='helloworld'
  app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'  
  db.init_app(app) #initializing the db

   #sqlalchemy database is stored at this location


  

  
  from .views import views
  from .auth import auth

  app.register_blueprint(views,url_prefix="/")
  app.register_blueprint(auth, url_prefix="/")
  
  #database creation
  from .models import User, Blog


  create_database(app)

  login_manager=LoginManager()
  login_manager.login_view ='auth.login'
  login_manager.init_app(app)


  #load the user by their ID
  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))
 
  return app
  
def create_database(app):
    if not path.exists('instance/' + DB_NAME):
      with app.app_context():
        db.create_all()
      print("Created Database!")
   
  