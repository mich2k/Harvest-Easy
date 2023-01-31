from flask import Flask, request, session
from config import Config
from app.database.__init__ import db
from app.database.database import database_blueprint
from app.neighbor.neighbor import neighbor_blueprint
from app.bestpath.bestpath import path_blueprint
from app.map.map import map_blueprint
from app.geofirstrecord.geofirstrecord import geofirstrecord_blueprint
from app.fbprophet.fbprophet import fbprophet_blueprint
from app.handler.error_handler import handler_blueprint
from app.login.login import login_blueprint
from app.utils.utils import Utils
from os import getenv
from flask_cors import CORS
from app.login.__init__ import login_manager, bcrypt


#creo applicazione
appname = "IOT - SmartBin"
app = Flask(appname)



CORS(app, resource={
    r"/db/*":{
        'origins':'*'
    }   
})

myconfig = Config
app.config.from_object(myconfig)
myutils = Utils()

def getUtils():
    return myutils

# config update according to environment,
    # will be mandatory when the app will be larger

# print(getenv('FLASK_CONFIG')) # if you want to print the env var you are passing
    # notice: is already passed by localboot.sh, so you don't need to pass it again

# is very important to refer to the db path from the config file, otherwise 
    # it will not work

if(getenv('FLASK_CONFIG') is None):
    print("FLASK_CONFIG not set in environment")
    #raise RuntimeError("Wrong env var value, exiting..")
elif(getenv('FLASK_CONFIG') == 'docker'):
    app.config.update(
        #SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db',
        DEBUG = True,
        TESTING = False,
    )
    print("NOTE: Using docker debug config")
elif(getenv('FLASK_CONFIG') == 'local'):
    app.config.update(
        #SQLALCHEMY_DATABASE_URI = 'sqlite:///out.db',
        DEBUG = True,
        TESTING = False,
    )
    print("NOTE: Using local config")
elif(getenv('FLASK_CONFIG') == 'docker_production'):
    app.config.update(
        SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db',
        DEBUG = False,
        TESTING = False,
    )
    print("NOTE: Using docker production config")
else:
    pass
    #raise RuntimeError("Wrong config, exiting..")


#Inizializzazione DB
db.init_app(app)

#Inizializzazione Bcrypt e LoginManager
bcrypt = bcrypt.init_app(app)
login_manager.init_app(app)

#Registrazione Blueprint
app.register_blueprint(geofirstrecord_blueprint, url_prefix='/geofr')
app.register_blueprint(database_blueprint, url_prefix='/db')
app.register_blueprint(neighbor_blueprint, url_prefix='/neighbor')
app.register_blueprint(path_blueprint, url_prefix='/bpath')
app.register_blueprint(map_blueprint, url_prefix='/map')
app.register_blueprint(fbprophet_blueprint, url_prefix='/pred')
app.register_blueprint(handler_blueprint)
app.register_blueprint(login_blueprint)

@app.route('/') 
def testoHTML():
    session.clear()
    return '<h1>Smart Bin</h1>'

@app.route('/esp', methods=['POST'])
def data():
    data = request.get_json()
    return 'Value: ' + data.get('temp', 'No name')

@app.route('/<string:name>&<int:id>')
def test(name, id):
    return '<h2> name:' + str(type(name)) + ' id:' + str(type(id)) + '</h2>'