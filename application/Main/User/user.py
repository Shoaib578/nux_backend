from application import db,app
from flask import Flask,request,Blueprint,jsonify
from application.Main.models import Users,UsersSchema
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Mail, Message
import os
from sqlalchemy import text
from datetime import datetime
from werkzeug.utils import secure_filename
import smtplib
import random
import requests


def remove_file(file, type):
    file_name = file
    folder = os.path.join(app.root_path, "static/" + type + "/"+file_name)
    os.remove(folder)
    return 'File Has Been Removed'


def save_file(file, type):
    file_name = secure_filename(file.filename)
    file_ext = file_name.split(".")[1]
    folder = os.path.join(app.root_path, "static/" + type + "/")
    file_path = os.path.join(folder, file_name)
    try:
        file.save(file_path)
        return True, file_name
    except:
        return False, file_name




def RegisterWithEmail():
    email = request.form.get('email')
    req_time = request.form.get('req_time')
    user = Users.query.filter_by(email=email).first()
    
    print(req_time)
    random_v = 0
    for rand in random.sample(range(1000, 2000),4):
        random_v =  rand
 
    if  req_time == '1':
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("theshoaibihsan9@gmail.com","Games578")
        server.sendmail("theshoaibihsan9@gmail.com",email,f'Your Verification Code is {random_v}')
        return jsonify({'msg':'Verify','v_code':random_v})

    elif req_time == '2' and  user:
        users_schema = UsersSchema()
        user_info = users_schema.dump(user)
        return jsonify({'msg':'You are Successfully Registered','user':user_info})
    elif req_time == '2' and not user:
        print('Not Signed')
        
        return jsonify({'msg':'Please Create your Password'})
    elif req_time == '3':
        email = request.form.get('email')
        password = request.form.get('password')
        hash_password = generate_password_hash(password)

        user_name = request.form.get('user_name')
        member_since = datetime.now().strftime('%Y-%m-%d')
        location = request.form.get('location')
        phone_no = request.form.get('phone_no')
        token = request.form.get('token')
        user = Users(user_name=user_name, email=email, password=hash_password,member_since=member_since,foreign_logged_in=0,location=location,phone_no=phone_no,token=token)
        db.session.add(user)
        db.session.commit()
        user = Users.query.filter_by(email=email).first()
        users_schema = UsersSchema()
        user_info = users_schema.dump(user)
        return jsonify({'msg':'You are Successfully Registered','user':user_info})






def RegisterWithPhoneNumber():

    phone_no = request.form.get('phone_no')
    req_time = request.form.get('req_time')
    
    user = Users.query.filter_by(email=phone_no).first()

    if req_time == '1' and  user :
        users_schema = UsersSchema()
        user_info = users_schema.dump(user)
        return jsonify({'msg':'need a password'})
    elif req_time == '1' and not user:
        print('Not Signed')
        
        return jsonify({'msg':'Please Create your Password'})
    elif req_time == '2':
        password = request.form.get('password')
        phone_no = request.form.get('phone_no')
        user = Users.query.filter_by(email=phone_no).first()
        if user and check_password_hash(user.password,password):

            users_schema = UsersSchema()
            user_info = users_schema.dump(user)
            return jsonify({'msg':'logged in','user':user_info})
        else:
            return jsonify({'msg':'wrong password'})
    
    elif req_time == '3':
        token = request.form.get('token')

        phone_no = request.form.get('phone_no')
        password = request.form.get('password')
        hash_password = generate_password_hash(password)

        user_name = request.form.get('user_name')
        member_since = datetime.now()
        location = request.form.get('location')
        user = Users(user_name=user_name, email=phone_no, password=hash_password,member_since=member_since,foreign_logged_in=0,location=location,token=token,phone_no=phone_no)
        db.session.add(user)
        db.session.commit()
        user = Users.query.filter_by(email=phone_no).first()
        users_schema = UsersSchema()
        user_info = users_schema.dump(user)
        return jsonify({'msg':'You are Successfully Registered','user':user_info})




def LoginWithFacebook():
    req_time = request.form.get('req_time')
    user_name = request.form.get('user_name')
    user = Users.query.filter_by(email=user_name).first()

    if req_time == '1' and user:
        users_schema = UsersSchema()
        user_info = users_schema.dump(user)
        return jsonify({'msg':'found','user':user_info})
        
    if req_time == '1' and not user:
        return jsonify({'msg':'not found'})
    
    if req_time == '2':
        user_name = request.form.get('user_name')
        phone_no = request.form.get('phone_no')
        location = request.form.get('location')
        password =  generate_password_hash('default')
        member_since = datetime.now()
        token = request.form.get('token')


        user = Users(user_name=user_name,location=location,password=password,member_since=member_since,phone_no=phone_no,email=user_name,foreign_logged_in=1,token=token)
        db.session.add(user)
        db.session.commit()

        user = Users.query.filter_by(email=user_name).first()
        users_schema = UsersSchema()
        user_info = users_schema.dump(user)
        return jsonify({'msg':'logged in','user':user_info})


    


def LoginWithGoogle():
    req_time = request.form.get('req_time')
    email = request.form.get('email')
    user = Users.query.filter_by(email=email).first()

    if req_time == '1' and user:
        users_schema = UsersSchema()
        user_info = users_schema.dump(user)
        return jsonify({'msg':'found','user':user_info})
        
    if req_time == '1' and not user:
        return jsonify({'msg':'not found'})

    
    if req_time == '2':

        token = request.form.get('token')

        user_name = request.form.get('user_name')
        phone_no = request.form.get('phone_no')
        location = request.form.get('location')
        password =  generate_password_hash('default')
        email = request.form.get('email')
        member_since = datetime.now()

        user = Users(user_name=user_name,location=location,password=password,member_since=member_since,phone_no=phone_no,email=email,foreign_logged_in=1,token=token)
        db.session.add(user)
        db.session.commit()

        user = Users.query.filter_by(email=email).first()
        users_schema = UsersSchema()
        user_info = users_schema.dump(user)
        return jsonify({'msg':'logged in','user':user_info})

    

def GetUserInfo():
    user_id = request.args.get('user_id')
    user = Users.query.filter_by(user_id=user_id).first()
    user_schema = UsersSchema()
    user_info = user_schema.dump(user)

    
    return jsonify({'user':user_info})



def EditProfile():
    user_id = request.form.get('user_id')
    user_name = request.form.get('user_name')
    phone_no = request.form.get('phone_no')
    location = request.form.get('location')
    
    description = request.form.get('description')
    image = request.files.get('image')
    user = Users.query.filter_by(user_id=user_id).first()

    if user:
        if description:
            user.descriptions = description
        else:
            pass
        

        if image:

            if user.profile_pic:
                remove_file(user.profile_pic,'profile_pics')
            else:
                pass
                
            user.profile_pic = image.filename
            save_file(image,'profile_pics')
        else:
            pass   
        user.user_name = user_name
        user.phone_no = phone_no
        user.location = location

        db.session.commit()
        return jsonify({'msg':'Succesfully Updated'})
    else:
        return jsonify({'msg':"Coud'nt Found User"})



def UpdatePassword():
    user_id = request.form.get('user_id')
    password = request.form.get('password')
    hash_password = generate_password_hash(password)

    user = Users.query.filter_by(user_id=user_id).first()
    user.password = hash_password
    return jsonify({'msg':'Successfully Update'})



def DeleteAccount():
    user_id = request.args.get('user_id')
    user = Users.query.filter_by(user_id=user_id).first()
    db.session.delete(user)
    return jsonify({'msg':'Deleted Succesfully'})