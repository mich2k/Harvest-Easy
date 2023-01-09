from .database import database_blueprint
from .tables import *

#Getters
@database_blueprint.route('/accessAdmin?<string:uid>&<string:password>', methods=['GET'])
def login(uid, password):
    if db.session.query(Admin.uid == uid and Admin.password == password) is not None:
        return True
    return False

@database_blueprint.route('/checkUsername?<string:usr>', methods=['GET'])
def checkUsername(usr):
    if db.session.query(Admin.uid == usr) is not None:
        return True
    return False

@database_blueprint.route('/checkSession?<string:chatid>&<string:userid>', methods=['GET'])
def checkSession(chatid, userid):
    if db.session.query(TelegramIDChatUser.id_user == userid and TelegramIDChatAdmin.id_user == userid) is not None:
        return True
    return False

#Setters