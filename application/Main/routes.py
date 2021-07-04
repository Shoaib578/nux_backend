
from flask import Blueprint

from application.Main.Product import product
from application.Main.User import user
from application.Main.Message import message

main = Blueprint('main', __name__,static_folder='../static')


   
   
   





@main.route('/register_user_with_email',methods=['POST'])
def RegisterWithEmail():
    return user.RegisterWithEmail()



@main.route('/register_phone_number',methods=['POST'])
def RegisterWithPhoneNumber():

    return user.RegisterWithPhoneNumber()

        

@main.route('/register_with_facebook',methods=['POST'])
def LoginWithFacebook():
    return user.LoginWithFacebook()
    
        

@main.route('/login_with_google',methods=['POST'])
def LoginWithGoogle():
    return user.LoginWithGoogle()






@main.route('/get_user_info')
def GetUserInfo():
   return user.GetUserInfo()






@main.route('/edit_profile',methods=['POST'])
def EditProfile():
    return user.EditProfile()


@main.route('/insert_product',methods=['POST'])
def all_products():

   return  product.InserProduct()


@main.route('/get_all_my_ads')
def GetAllMyAds():
    return product.MyAds()


@main.route('/get_all_ads',methods=['GET'])
def GetAllAds():
    return product.GetAllAds()

@main.route('/make_favorite',methods=['GET'])
def MakeFavorite():
    return product.MakeFavorite()


@main.route('/my_favorite',methods=['GET'])
def MyFavorite():
    return product.MyFavorite()

@main.route('/like_or_unlike',methods=['GET'])
def Like_or_Unlike():
    return product.Like_or_Unlike()

@main.route('/view_product',methods=['GET'])
def ViewProduct():
    return product.ViewProduct()

@main.route('/get_related_products',methods=['GET'])
def RalatedProducts():
    return product.RalatedProducts()


@main.route('/mark_it_as_sold_or_unsold',methods=['GET'])
def Mark_as_Sold_or_Unsold():
    return product.Mark_as_Sold_or_Unsold()

@main.route('/another_user_ads',methods=['GET'])
def SeeAnotherUserProfile():
    return product.SeeAnotherUserProfile()


@main.route('/quicksearch',methods=['GET'])
def QuickSearch():
    return product.QuickSearch()


@main.route('/send_message',methods=['POST'])
def SendMessage():
    return message.SendMessage()


@main.route('/get_messages',methods=['GET'])
def GetMessages():
    return message.GetMessages()

@main.route('/get_recent_chats',methods=['GET'])
def GetRecentChats():
    return message.GetRecentChats()


@main.route('/get_notifications',methods=['GET'])
def GetNotifications():
    return message.GetNotifications()

@main.route('/see_all_notifications',methods=['GET'])
def SeeAllNotifications():
    return message.SeeAllNotifications()


@main.route('/delete_notifications',methods=['GET'])
def Delete_Notification():
    return message.Delete_Notification()


@main.route('/delete_msg',methods=['GET'])
def Delete_Message():
    return message.Delete_msg()


@main.route('/update_password',methods=['POST'])
def UpdatePassword():
    return user.UpdatePassword()