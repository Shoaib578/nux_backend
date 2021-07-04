from flask import Blueprint,jsonify,request,render_template,redirect,flash,url_for,request
from application.Main.models import Product,AdminUser
from application import db,app

from werkzeug.utils import secure_filename
import os
from sqlalchemy import text
from datetime import datetime
from application.Admin_Panel.forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required

admin  = Blueprint('admin', __name__,template_folder='templates',static_folder='../static')

base_url = 'https://nux-app.herokuapp.com/'

def remove_file(file, type):
    file_name = file
    folder = os.path.join(app.root_path, "static/" + type + "/"+file_name)
    os.remove(folder)
    return 'File Has Been Removed'


@admin.route('/',methods=['GET','POST'])
@login_required
def Home():
    if AdminUser.query.count() == 0:
        admin = AdminUser(email='theadmin21@gmail.com',password='Games')
        db.session.add(admin)
        db.session.commit()
    else:
        pass


    pending_products = Product.query.filter_by(status='pending').all()

    return render_template('home.html',products=pending_products,base_url=base_url)



@admin.route('/login',methods=['GET', 'POST'])
def Login():
    if AdminUser.query.count() == 0:
        admin = AdminUser(email='theadmin21@gmail.com',password='Games')
        db.session.add(admin)
        db.session.commit()
    else:
        pass


    if current_user.is_authenticated:
        return redirect(url_for('admin.Home'))
    form = LoginForm()
    
    user = AdminUser.query.filter_by(email=form.email.data).first()

    
    if user and user.password == form.password.data:
        
        login_user(user, False)
        return redirect(url_for('admin.Home'))
    else:
        flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', form=form)

    

@admin.route('/confirm_product/<int:id>/',methods=['GET', 'POST'])
def confirm_product(id):
    product = Product.query.filter_by(product_id=id).first()
    product.status = 'confirmed'
    db.session.commit()
    flash('Product Confirmed')
    return redirect(url_for('admin.Home'))




@admin.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for('admin.Login'))