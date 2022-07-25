
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from vechrent.config import Config
from os import path 



db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='info'

mail = Mail()


def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
   
        
        
    from vechrent.users.routes import users
    from vechrent.main.routes import main
    from vechrent.vehicle.routes import vehicle_route

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(vehicle_route)

    with app.app_context():
        db.create_all()

    return app
            
