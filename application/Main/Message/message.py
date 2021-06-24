from application import db,app
from flask import Flask,request,Blueprint,jsonify
from application.Main.models import Users,UsersSchema,Product,ProductSchema,Messages,MessagesSchema,RecentChatsSchema,RecentChats,Notification,NotificationsSchema

import os
from sqlalchemy import text
from datetime import datetime
from werkzeug.utils import secure_filename


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



def InsertRecentChats(my_id,user_id):
    recent_chat = RecentChats.query.filter_by(recent_chat=user_id,recent_chat_for=my_id).first()
    if recent_chat:
        return jsonify({'msg':'already exist'})
    else:
        recent_chat = RecentChats(recent_chat=user_id,recent_chat_for=my_id)
        db.session.add(recent_chat)
        db.session.commit()


def InsertNotification(created_by,reciever,notification_txt):
    notification = Notification(created_by=created_by,notification_txt=notification_txt,seen=0,reciever=reciever)
    db.session.add(notification)
    db.session.commit()
    


def SendMessage():
    image = request.files.get('image')
    msg_txt = request.form.get('msg')
    inserted_by = request.form.get('inserted_by')
    msg_for = request.form.get('msg_for')
    if image:
        save_file(image,'message_images')
        msg = Messages(sended_by=inserted_by,message_txt=msg_txt,image=image.filename,msg_for=msg_for)

    else:
        msg = Messages(sended_by=inserted_by,message_txt=msg_txt,image='',msg_for=msg_for)

    InsertRecentChats(msg_for,inserted_by)
    InsertNotification(inserted_by,msg_for,'Sent You a Message')


    db.session.add(msg)
    db.session.commit()
    return jsonify({'msg':'Message has been inserted'})




def GetMessages():
    my_id = request.args.get('my_id')
    user_id = request.args.get('user_id')
    get_msg_sql = text("SELECT * FROM messages LEFT JOIN users on user_id=messages.msg_for WHERE  msg_for="+str(user_id)+" OR sended_by="+str(user_id))
    get_msg_query = db.engine.execute(get_msg_sql)
    msgSchema = MessagesSchema(many=True)
    msgs = msgSchema.dump(get_msg_query)
    return jsonify({'msgs':msgs})



def GetRecentChats():
    my_id = request.args.get('my_id')
    recent_chats_sql = text("SELECT * FROM recent_chats LEFT JOIN users on users.user_id=recent_chats.recent_chat WHERE  recent_chat_for="+str(my_id))
    recent_chats_query = db.engine.execute(recent_chats_sql)
    recent_chats_schema = RecentChatsSchema(many=True)
    recent_chats = recent_chats_schema.dump(recent_chats_query)
    print(recent_chats)
    return jsonify({'recent_chats':recent_chats})



def GetNotifications():
    my_id = request.args.get('my_id')
    notifications_sql = text("SELECT *  FROM notification LEFT JOIN users on users.user_id=notification.created_by WHERE reciever="+str(my_id))
    notifications_query = db.engine.execute(notifications_sql)
    notifications_schema = NotificationsSchema(many=True)
    notifications = notifications_schema.dump(notifications_query)

    notifications_count = Notification.query.filter_by(reciever=my_id,seen=0)

    return jsonify({'notifications':notifications,'notifications_count':notifications_count.count()})


def SeeAllNotifications():
    my_id = request.args.get('my_id')
    check_existance = Notification.query.filter_by(seen=0,reciever=my_id)
    if check_existance.count() >0:
        check = Notification.query.filter_by(seen=0,reciever=my_id).all()
        for seen in check:
            
            seen.seen = 1
            db.session.commit()
            
    else:
        return jsonify({'msg':'No Notifications'})

    return jsonify({'msg':'checked'})



def Delete_Notification():
    notification_id = request.args.get('notification_id')
    notification = Notification.query.filter_by(notification_id=notification_id).first()
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'msg':'Notification Deleted'})



def Delete_msg():
    msg_id = request.args.get('msg_id')
    msg =  Messages.query.filter_by(message_id=msg_id).first()
    if msg.image:
        remove_file(msg.image,'message_images')
    else:
        pass
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'msg':'Deleted'})