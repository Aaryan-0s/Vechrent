import flask_login
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,NumberRange
from vechrent.models import user ,Vehicle
from flask_login import current_user



class Addvehicle(FlaskForm):
    vehicle_name= StringField('Vehicle Name',
                           validators=[DataRequired()])

    Description=TextAreaField('Description',
                           validators=[DataRequired(),Length(min=50, max=200)])
    
    Price=IntegerField('Price',
                           validators=[DataRequired(),NumberRange(min=0)],default=0)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
        
    
    submit = SubmitField('Update')




