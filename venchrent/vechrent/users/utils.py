import email
from email.mime import image
from turtle import title
from flask import  flash, redirect,render_template,url_for,request,abort,Blueprint,current_app
from vechrent.models import user
# ,Venue
from vechrent import bcrypt,db,mail
from flask_login import login_user,current_user,logout_user,login_required
# ,RequestResetForm,ResetPasswordForm
import secrets
from PIL import Image
import os
from flask_mail import Message


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(current_app.root_path,'static/img/profile_pic',picture_fn)

    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)


    i.save(picture_path)
    return picture_fn


def send_reset_email(User):
    token=User.get_reset_token()
    msg=Message('Password reset request ',sender='aaryanbasnet16@gmail.com',
                                        recipients=[User.email])
    msg.body=f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg) 
