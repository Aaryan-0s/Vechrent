import email
from tkinter import CASCADE
from flask import current_app
from datetime import datetime
from vechrent import db,login_manager
from email.policy import default
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(id):
    return user.query.get(int(id))

class user(db.Model,UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(120),nullable=False,default='default.jpg')
    password=db.Column(db.String(60),nullable=False)
    booking=db.relationship('vehicle_rental',backref='author',cascade='all,delete-orphan',lazy=True)


    


    def get_reset_token(self,expires_sec=1800 ):
        s=Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None 
        return user.query.get(user_id)
    def __repr__(self):
        return f"user('{self.username}','{self.email}','{self.password}')"



class Vehicle(db.Model):
    __tablename__='vehicle'
    vehicle_id=db.Column(db.Integer,primary_key=True)
    vehicle_name=db.Column(db.String(80),nullable=False)
    description=db.Column(db.Text,nullable=False)
    price=db.Column(db.Numeric(10,2),nullable=False)
    date_posted=db.Column(db.Date,nullable=False,default=datetime.utcnow())
    image_file=db.Column(db.String(120),nullable=False,default='car1.jpg')
    booking=db.relationship('vehicle_rental',backref='authors',cascade='all,delete-orphan',lazy=True)
    

    def __repr__(self):
        return f"user('{self.venue_name}','{self.venue_address}','{self.price}')"

    
    
#     #needs to be changed

class vehicle_rental(db.Model):
    __tablename__='rental'
    rent_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    vehicle_id=db.Column(db.Integer,db.ForeignKey('vehicle.vehicle_id',ondelete='CASCADE'),nullable=False)
    rented_from=db.Column(db.DateTime,nullable=False)
    
    