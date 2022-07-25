import email
from email.mime import image
from turtle import title
from flask import  flash, redirect,render_template,url_for,abort,Blueprint,current_app,request
from vechrent.models import user
#,Venue
from vechrent import bcrypt,db,mail
from flask_login import login_user,current_user,logout_user,login_required
from vechrent.users.forms import UpdateAccountForm,RequestResetForm,ResetPasswordForm
from vechrent.users.utils import save_picture,send_reset_email
import secrets
from PIL import Image
import os
from flask_mail import Message


from flask import Blueprint
users=Blueprint('users',__name__)


@users.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method=='POST':
        if request.form['btn']=='signup':
            if (user.query.filter_by(username=request.form['username']).first()):
                flash("Username is already taken ","danger")
            elif (user.query.filter_by(email=request.form['email']).first()):
                flash("email is already taken ","danger")
            else:
                hashed_password=bcrypt.generate_password_hash(request.form['password-signup']).decode('utf-8')
                User=user(username=request.form['username'],email=request.form['email'],password=hashed_password)
                db.session.add(User)
                db.session.commit()
                flash(f"Account created for {request.form['username']}!",'primary')
                        
        if request.form['btn']=='signin':
            User=user.query.filter_by(username=request.form['username-login']).first()
            if User and bcrypt.check_password_hash(User.password,request.form['password-login']):
                login_user(User)
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                 flash("Login unsucessfull",'danger')
    return render_template("login-signup.html",title="login")


@users.route("/account" ,methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Account updated","success")
        return redirect(url_for('users.account'))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email

    image_file=url_for('static',filename='img/profile_pic/'+current_user.image_file)
    return render_template('account.html',title="account",
                                image_file=image_file,form=form)

@users.route("/loginout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route('/admin',methods=['GET','POST'])
@login_required
def admin():
    id=current_user.id
    if id==1:             
        return render_template("admin/admin.html",title="adminpanel")
    else:
        flash("Sorry this page is restricted",'danger')
        return redirect(url_for("main.home"))

@users.route('/admin/userslist',methods=['GET','POST'])
@login_required
def delete_account():
    id=current_user.id
    Users = user.query.all()
    if id==1:
        if request.method=='POST':
            if request.form['delete']=='delete':
                user_delete=user.query.filter_by(id=request.form['Id']).first()
                db.session.delete(user_delete)
                db.session.commit()
                return redirect(url_for('users.delete_account'))               
        return render_template("admin/delete_account.html",title="delete_account",Users=Users)
    else:
        flash("Sorry this page is restricted",'danger')
        return redirect(url_for("main.home"))

@users.route("/reset_password",methods= ['GET','POST'])
def reset_request():
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        form=RequestResetForm()
        if form.validate_on_submit():
            User=user.query.filter_by(email=form.email.data).first()
            send_reset_email(User)
            flash("An email has been  sent with instruction to reset your password ","info ")
            return redirect(url_for('users.login'))
        return render_template('reset_request.html',title="Reset Password",form=form )

@users.route("/reset_password/<token>",methods= ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    User=user.verify_reset_token(token)
    if User is None:
        flash("That is an invalid or expired token ","warning")
        return redirect(url_for("users.reset_request"))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title="Reset Password",form=form)
