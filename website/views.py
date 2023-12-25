from flask import Blueprint, json,jsonify ,render_template,request,flash,redirect,url_for
from flask_login import login_required, current_user 
from .import db
from .models import Blog

views=Blueprint("views",__name__)

@views.route("/",methods=['GET','POST'])
@login_required
def home():
  if request.method =='POST':
    blog=request.form.get('blog')
    print(blog)
    if blog != None:
      new_blog=Blog(data=blog,user_id=current_user.id)
      db.session.add(new_blog)
      db.session.commit()
      flash('blog added',category='success')
    else:
      flash('Blog is too short!',category='error')
  return render_template("home.html",user=current_user)

@views.route("/delete_blog",methods=['POST'])
def delete_blog():
  blog=json.loads(request.data)
  blogId=blog['blogId']
  blog=Blog.query.get(blogId)
  if blog:
    if blog.user_id == current_user.id:
      db.session.delete(blog)
      db.session.commit()
  return jsonify({})

  