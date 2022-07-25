from flask import  flash, redirect,render_template,url_for,request,abort,Blueprint,current_app
from flask_login import login_user,current_user,logout_user,login_required
from requests import post
from vechrent.models import user,Vehicle



main=Blueprint('main',__name__)

@main.route("/",methods=['POST','GET'])
def home():
    page = request.args.get('page', 1, type=int)

    vehicle = Vehicle.query.paginate(page=page, per_page=4)
    count=Vehicle.query.count()
    return render_template("home.html",vehicle=vehicle,count=count)