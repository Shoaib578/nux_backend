
from application import db,app
from flask import Flask,request,Blueprint,jsonify
from application.Main.models import Users,UsersSchema,Product,ProductSchema,FavoriteProducts,FavoriteProductSchema,Likes,LikesSchema

import os
from sqlalchemy import text
from datetime import datetime
from werkzeug.utils import secure_filename

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




def InserProduct():
    product_title = request.form.get('product_title')
    product_description = request.form.get('product_description')
    product_price = request.form.get('product_price')
    product_category = request.form.get('product_category')
    product_location = request.form.get('product_location')
    product_image1 = request.files.get('product_image1')
    product_image2 = request.files.get('product_image2')
    product_image3 = request.files.get('product_image3')
    posted_by = request.form.get('posted_by')
    posted_date = datetime.now()
    condtion = request.form.get('condition')
    print(condtion)
    
    save_file(product_image1,'product_images')
    save_file(product_image2,'product_images')
    save_file(product_image3,'product_images')

    product = Product(product_title=product_title,product_description=product_description,product_category=product_category,
    product_image1=product_image1.filename,product_image2=product_image2.filename,product_image3=product_image3.filename,
    product_location=product_location,posted_by=posted_by,posted_date=posted_date.strftime('%Y-%m-%d'),new_or_used=condtion,
    price=product_price,status='pending')
    db.session.add(product)
    db.session.commit()
    return jsonify({'msg':'Product Has Been Uploaded. Now Wait for Confirmation'})



def MyAds():
    my_id = request.args.get('my_id')
    want_to_filter = request.args.get('want_to_filter')
    
    if want_to_filter == 'false':

        sql = text("SELECT *,(SELECT count(*) FROM favorite_products WHERE   favorite_products.favorite_by="+str(my_id)+" AND favorite_products.product_id=product.product_id ) as is_favorite, (SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count,(SELECT count(*) FROM likes  where likes.product_id=product.product_id and liked_by="+str(my_id)+") as is_liked FROM product LEFT JOIN users on users.user_id=posted_by  WHERE  posted_by="+str(my_id))
        query = db.engine.execute(sql)
        product_schema = ProductSchema(many=True)
        products = product_schema.dump(query)
        return jsonify({'products':products})
    else:
        filter_data= request.args.get('filter_data')
        print(filter_data)
        sql = text("SELECT *,(SELECT count(*) FROM favorite_products WHERE favorite_by="+str(my_id)+" AND favorite_products.product_id=product_id) as is_favorite , (SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count ,(SELECT count(*) FROM likes  where likes.product_id=product.product_id and liked_by="+str(my_id)+") as is_liked FROM product LEFT JOIN users on users.user_id=posted_by  WHERE  posted_by="+str(my_id)+" AND status='"+str(filter_data)+"'")
        query = db.engine.execute(sql)
        product_schema = ProductSchema(many=True)
        products = product_schema.dump(query)
        return jsonify({'products':products})

def SeeAnotherUserProfile():
    product_owner_id = request.args.get('product_owner_id')

    is_loggedin = request.args.get('is_loggedin')

    if is_loggedin == 'true':
        my_id = request.args.get('my_id')
        sql = text("SELECT *,(SELECT count(*) FROM favorite_products WHERE   favorite_products.favorite_by="+str(my_id)+" AND favorite_products.product_id=product.product_id ) as is_favorite, (SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count,(SELECT count(*) FROM likes  where likes.product_id=product.product_id and liked_by="+str(my_id)+") as is_liked FROM product LEFT JOIN users on users.user_id=posted_by  WHERE  posted_by="+str(product_owner_id))
        query = db.engine.execute(sql)
        product_schema = ProductSchema(many=True)
        products = product_schema.dump(query)
        return jsonify({'products':products})
    else:
        sql = text("SELECT *, (SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count FROM product LEFT JOIN users on users.user_id=posted_by  WHERE  posted_by="+str(product_owner_id))
        query = db.engine.execute(sql)
        product_schema = ProductSchema(many=True)
        products = product_schema.dump(query)
        return jsonify({'products':products})




def MakeFavorite():
    user_id =request.args.get('user_id')
    product_id = request.args.get('product_id')

    print(user_id,product_id)
    favorite = FavoriteProducts.query.filter_by(favorite_by=user_id,product_id=product_id).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'msg':'unfavorite'})
    else:
        favorite = FavoriteProducts(favorite_by=user_id,product_id=product_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'msg':'favorite'})


def MyFavorite():
    user_id = request.args.get('user_id')
    sql = text("SELECT *,(SELECT count(*) FROM favorite_products WHERE  favorite_products.product_id=product.product_id AND favorite_products.favorite_by="+str(user_id)+") as is_favorite, (SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count,(SELECT count(*) FROM likes  where likes.product_id=product.product_id and liked_by="+str(user_id)+") as is_liked FROM favorite_products LEFT JOIN product on product.product_id=favorite_products.product_id WHERE favorite_products.favorite_by="+str(user_id))
    query = db.engine.execute(sql)
    favorite_products_schema = FavoriteProductSchema(many=True)
    products = favorite_products_schema.dump(query)
    return jsonify({'products':products})


def Like_or_Unlike():
    user_id = request.args.get('user_id')
    product_id = request.args.get('product_id')

    is_liked = Likes.query.filter_by(liked_by=user_id,product_id=product_id).first()
    if is_liked:
        db.session.delete(is_liked)
        db.session.commit()
        return jsonify({'msg':'UnLiked'})
    else:
        like = Likes(product_id=product_id,liked_by=user_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'msg':'Liked'})


def ViewProduct():
    product_id = request.args.get('product_id')
    get_product_sql = text("SELECT * FROM product LEFT JOIN users on users.user_id=product.posted_by WHERE product_id="+str(product_id))
    get_product_query = db.engine.execute(get_product_sql)
    product_schema = ProductSchema(many=True)
    product = product_schema.dump(get_product_query)
    return jsonify({'product': product})


def RalatedProducts():
    product_category = request.args.get('product_category')
    product_id = request.args.get('product_id')

    is_loggedin = request.args.get('is_loggedin')
    if is_loggedin == 'true':
        my_id = request.args.get('my_id')
        
        get_products_sql = text("SELECT *,(SELECT count(*) FROM favorite_products WHERE  favorite_products.product_id=product.product_id AND favorite_products.favorite_by="+str(my_id)+") as is_favorite, (SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count,(SELECT count(*) FROM likes  where likes.product_id=product.product_id and liked_by="+str(my_id)+") as is_liked FROM product WHERE  product_category='"+str(product_category)+"' AND product_id !="+str(product_id)+" AND status !='pending' ORDER BY product_id DESC  LIMIT 20")
        get_products_query = db.engine.execute(get_products_sql)
        product_schema = ProductSchema(many=True)
        products = product_schema.dump(get_products_query)
        return jsonify({'products': products})
    else:
        get_products_sql = text("SELECT *,(SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count FROM product WHERE  product_category='"+str(product_category)+"' AND product_id !="+str(product_id)+" AND status !='pending' ORDER BY product_id DESC  LIMIT 20")
        get_products_query = db.engine.execute(get_products_sql)
        product_schema = ProductSchema(many=True)
        products = product_schema.dump(get_products_query)
        return jsonify({'products': products})




def Mark_as_Sold_or_Unsold():
    product_id = request.args.get('product_id')

    product = Product.query.filter_by(product_id=product_id).first()

    if product.status != 'sold':
        product.status = 'sold'
    else:
        product.status = 'confirmed'
    
    db.session.commit()
    return jsonify({'msg':'Successfuly'})


def GetAllAds():
    
    want_to_filter = request.args.get('want_to_filter')
    want_all = request.args.get('want_all')
    if want_all == 'false':
        location = request.args.get('location')
        my_id = request.args.get('my_id')
        if want_to_filter == 'false':
            products_sql = text("SELECT *,(SELECT count(*) FROM favorite_products WHERE  favorite_products.product_id=product.product_id AND favorite_products.favorite_by="+str(my_id)+") as is_favorite, (SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count,(SELECT count(*) FROM likes  where likes.product_id=product.product_id and liked_by="+str(my_id)+") as is_liked FROM product LEFT JOIN users on users.user_id=posted_by  WHERE  product_location='"+str(location)+"' AND status !='pending'")
            query = db.engine.execute(products_sql)
            product_schema = ProductSchema(many=True)
            products = product_schema.dump(query)
            return jsonify({'products':products})
        else:
            return jsonify({'products':'Nothing'})
    else:
        products_sql = text("SELECT *,(SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count FROM product LEFT JOIN users on users.user_id=posted_by  WHERE  status !='pending'")
        query = db.engine.execute(products_sql)
        product_schema = ProductSchema(many=True)
        products = product_schema.dump(query)
        return jsonify({'products':products})



def QuickSearch():
    location = request.args.get('location')
    category = request.args.get('category')
    
    is_loggedin = request.args.get('is_loggedin')

    if is_loggedin == 'true':
        my_id = request.args.get('my_id')
        product_sql = text("SELECT *,(SELECT count(*) FROM favorite_products WHERE  favorite_products.product_id=product.product_id AND favorite_products.favorite_by="+str(my_id)+") as is_favorite, (SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count,(SELECT count(*) FROM likes  where likes.product_id=product.product_id and liked_by="+str(my_id)+") as is_liked FROM product LEFT JOIN users on users.user_id=posted_by  WHERE  product_location='"+str(location)+"' AND product_category='"+str(category)+"' AND status !='pending'")
        product_query = db.engine.execute(product_sql)
        product_schema = ProductSchema(many=True)
        products = product_schema.dump(product_query)
        return jsonify({'products':products})
    else:
        product_sql = text("SELECT *, (SELECT count(*) from likes where likes.product_id=product.product_id) as likes_count FROM product LEFT JOIN users on users.user_id=posted_by  WHERE  product_location='"+str(location)+"' AND product_category='"+str(category)+"' AND status !='pending'")
        product_query = db.engine.execute(product_sql)
        product_schema = ProductSchema(many=True)
        products = product_schema.dump(product_query)
        return jsonify({'products':products})