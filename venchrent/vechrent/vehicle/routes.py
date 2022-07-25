import email
from email.mime import image
from turtle import title
from flask import  flash, redirect,render_template,url_for,request,abort,Blueprint,current_app
from vechrent.models import user,Vehicle,vehicle_rental 
from vechrent import bcrypt,db,mail
from flask_login import login_user,current_user,logout_user,login_required
from vechrent.vehicle.forms import  Addvehicle
from vechrent.vehicle.utils import save_post_picture
import secrets
from PIL import Image
import os
from datetime import date
today=date.today()


from flask_mail import Message

from flask import Blueprint

vehicle_route=Blueprint('vehicle_route',__name__)

@vehicle_route.route("/addvehicle",methods= ['GET','POST'])
@login_required
def addvehicle():
    id=current_user.id
    
    form=Addvehicle()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_post_picture(form.picture.data)
            
        Post=Vehicle(
                    vehicle_name=form.vehicle_name.data,
                    description=form.Description.data,
                    price=form.Price.data,
                    image_file=picture_file,
                    )

        db.session.add(Post)
        db.session.commit()
        flash("Post has been created",'success')
        return redirect(url_for("main.home"))
    if id==1:
         return render_template("admin/add_vehicle.html",title="addvehicle",form=form,legend="Addvehicle")
    else:
        flash("Sorry this page is restricted")
        return redirect(url_for("main.home"))


@vehicle_route.route('/admin/vehiclelist',methods=['GET','POST'])
@login_required
def vehicle_list():
    id=current_user.id
    vehicle = Vehicle.query.all()
    if id==1:
        if request.method=='POST':
            if request.form['delete']=='delete':
                vehicle_delete=Vehicle.query.filter_by(vehicle_id=request.form['Id']).first()
                db.session.delete(vehicle_delete)
                db.session.commit()
                return redirect(url_for('vehicle_route.vehicle_list'))
   

        return render_template("admin/vehicle_list.html",title="Vehicle list",vehicle=vehicle)
    else:
        flash("Sorry this page is restricted",'danger')
        return redirect(url_for("main.home"))


@vehicle_route.route("/admin/vehiclelist/<int:vehicle_id>/update",methods= ['GET','POST'])
@login_required
def update_vehicle(vehicle_id):
    vehicle=Vehicle.query.get_or_404(vehicle_id)
    id=current_user.id
    if id!=1:
        abort(403)
    form=Addvehicle()
    if form.validate_on_submit():
        vehicle.vehicle_name=form.vehicle_name.data
        vehicle.description=form.Description.data
        vehicle.price=form.Price.data
        db.session.commit()
        flash("The vechicle details  has been updated!","success")
        return redirect(url_for("vehicle_route.vehicle_list",vehicle_id=vehicle_id))
    elif request.method=="GET":
        form.vehicle_name.data=vehicle.vehicle_name
        form.Description.data=vehicle.description
        form.Price.data=vehicle.price
    return render_template("admin/add_vehicle.html",title="Update Vechicle",form=form,legend="Update vehicle")

@vehicle_route.route("/vehicle_post",methods=['POST','GET'])
def vehicle_post():
    page = request.args.get('page', 1, type=int)

    vehicle = Vehicle.query.paginate(page=page, per_page=4)
   
    return render_template("vehicle_post.html",vehicle=vehicle)

@vehicle_route.route("/vehicle_detail/<int:vehicle_id>")
def vehicle_detail(vehicle_id):
    vehicle=Vehicle.query.get_or_404(vehicle_id)
    return render_template('vehicle_detail.html', title=vehicle.vehicle_name,vehicle=vehicle)



@vehicle_route.route("/rent_vehicle/<int:vehicle_id>",methods=['POST','GET'])
@login_required
def rent_vehicle(vehicle_id):
    
        if request.method=='POST':
                vehicle=Vehicle.query.get_or_404(vehicle_id)

    
        
                exists = db.session.query(vehicle_rental).filter_by(vehicle_id=vehicle.vehicle_id,rented_from=request.form['occasion_date']).first() is not None
                
                if exists:
                    flash("vehicle is taken that day ","warning")
                    
                   
                else:
                    rental=vehicle_rental(
                            user_id=current_user.id,
                            vehicle_id=vehicle.vehicle_id,
                            rented_from=request.form['occasion_date'],
                            name=request.form['fullname'],
                            )
                    db.session.add(rental)
                    db.session.commit()
                    flash("vehicle has been rented sucessfully",'success')
        return render_template('rent_form.html', title='checkout')
    
@vehicle_route.route('/rentlist',methods=['GET','POST'])
@login_required
def rent_list():
    
    rental = db.session.query(vehicle_rental).filter_by(user_id=current_user.id).all()
       
   

       
    return render_template('rent_list.html',rental=rental)

        