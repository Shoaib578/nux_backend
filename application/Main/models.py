from application import db,login_manager
from marshmallow_sqlalchemy import ModelSchema

from flask_login import UserMixin
import datetime 


@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
    return AdminUser.query.get(int(user_id))


class AdminUser(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))



class Users(db.Model,UserMixin):
    user_id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100),nullable=False)
    user_name = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    foreign_logged_in = db.Column(db.Integer)
    location = db.Column(db.String(200))
    member_since = db.Column(db.String(100))
    phone_no = db.Column(db.String(100))
    descriptions = db.Column(db.String(500))
    profile_pic = db.Column(db.String(200))

class UsersSchema(ModelSchema):
    class Meta:
        fields = ('user_id','user_name','email','password','foreign_logged_in','member_since','location','phone_no','descriptions','profile_pic')



class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_title = db.Column(db.String(200))
    product_description = db.Column(db.String(500))
    product_category = db.Column(db.String(200))
    product_image1 = db.Column(db.String(300))
    product_image2 = db.Column(db.String(300))
    product_image3 = db.Column(db.String(300))
    product_location = db.Column(db.String(200))
    posted_by = db.Column(db.Integer,db.ForeignKey('users.user_id',ondelete='CASCADE'))
    posted_date = db.Column(db.String(100))
    new_or_used = db.Column(db.String(100))
    status = db.Column(db.String(100))
    price = db.Column(db.String(100))
class ProductSchema(ModelSchema):
    class Meta:
        fields = ('user_id','user_name','product_location','phone_no','product_id',
        'product_title','product_description','product_category','product_image1',
        'product_image2','product_image3','posted_by','posted_date','posted_date',
        'status','price','is_favorite','likes_count','is_liked','profile_pic')



class FavoriteProducts(db.Model):
    favorite_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'))
    favorite_by = db.Column(db.Integer,db.ForeignKey('users.user_id'))

class FavoriteProductSchema(ModelSchema):
    class Meta:
        fields = ('user_id','user_name','product_location','phone_no','product_id',
        'product_title','product_description','product_category','product_image1',
        'product_image2','product_image3','posted_by','posted_date','posted_date',
        'status','price','favorite_id','favorite_by','is_favorite','likes_count','is_liked','profile_pic')


class Likes(db.Model):
    like_id = db.Column(db.Integer,primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'))
    liked_by = db.Column(db.Integer,db.ForeignKey('users.user_id'))

class LikesSchema(ModelSchema):
    class Meta:
        fields = ('user_id','product_id','like_id','favorite_by','is_favorite')



class Messages(db.Model):
    message_id = db.Column(db.Integer(), primary_key=True)
    sended_by = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    message_txt = db.Column(db.String(1000))
    image = db.Column(db.String(200))
    msg_for = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    

class MessagesSchema(ModelSchema):
    class Meta:
        fields = ('user_id','message_id','sended_by','message_txt','image','profile_pic','user_name','msg_for')


class RecentChats(db.Model):
    recent_id = db.Column(db.Integer, primary_key=True)
    recent_chat = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    recent_chat_for = db.Column(db.Integer,db.ForeignKey('users.user_id'))

class RecentChatsSchema(ModelSchema):
    class Meta:

        fields = ('recent_id','user_id','user_name','recent_chat','recent_chat_for','member_since',)



class Notification(db.Model):
    notification_id = db.Column(db.Integer(),primary_key=True)
    notification_txt = db.Column(db.String(100))
    created_by = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    reciever = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    seen = db.Column(db.Integer())


class NotificationsSchema(ModelSchema):
    class Meta:
        fields = ('user_id','notification_id','notification_txt','created_by','seen','reciever','notification_count','user_name','notifications_count')