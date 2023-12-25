from .import db
from flask_login import UserMixin
from sqlalchemy.sql import func
#flask_login with usermixin takes care of user authentication ,hashed passwords and session management.


#create table for  notes
class Blog(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  data = db.Column(db.String(10000))
  date = db.Column(db.DateTime(timezone=True),default=func.now())  # for current date and time
  user_id = db.Column(db.Integer,db.ForeignKey('user.id'))  #specifying foreign key!

  def __init__(self, data, user_id):
     self.data = data
     self.user_id=user_id

# Create a table for the user
class User(db.Model,UserMixin):
  id = db.Column(db.Integer,primary_key=True)
  username = db.Column(db.String(20))
  email = db.Column(db.String(120),unique=True)
  password = db.Column(db.String(160))
  blogs=db.relationship('Blog') #user id is associated to the note table.

  def __init__(self, username, email, password):
     self.username = username
     self.email = email
     self.password = password
    
  

