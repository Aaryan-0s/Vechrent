
import flask_login
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,NumberRange
from vechrent.models import user 
# ,Venue
from flask_login import current_user


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Update')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    def validate_username(self, username):
        if username.data != current_user.username:
            User = user.query.filter_by(username=username.data).first()
            if User:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            User = user.query.filter_by(email=email.data).first()
            if User:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
        email = StringField('Email',
                        validators=[DataRequired(), Email()])
        submit=SubmitField('Request Password reset')

        def validate_email(self, email):
                
                    User = user.query.filter_by(email=email.data).first()
                    if User is None :
                        raise ValidationError('That email doesnt exist.')


class ResetPasswordForm(FlaskForm):
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
        submit=SubmitField('Reset Password ')
