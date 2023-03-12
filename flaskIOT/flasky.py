from flask import Flask, session
from config import Config
from app.database.__init__ import db
from app.database.database import database_blueprint
from app.queries.getters.getters import get_blueprint
from app.queries.setters.setters import set_blueprint
from app.queries.checkers.checkers import check_blueprint
from app.neighbor.neighbor import neighbor_blueprint
from app.bestpath.bestpath import path_blueprint
from app.map.map import map_blueprint
from app.fbprophet.fbprophet import fbprophet_blueprint
from app.handler.error_handler import handler_blueprint
from app.login.login import login_blueprint
from app.utils.utils import Utils
from os import getenv
from flask_cors import CORS
from app.login.__init__ import bcrypt, jwt
from flasgger import Swagger


def getUtils():
    return myutils


# creo applicazione
appname = "IOT - SmartBin"
app = Flask(appname)

try:
    session.clear()
except:
    print('Session already cleaned')

template = {
    "swagger": "2.0",
    "info": {
        "title": "Harvest Easy",
        "description": "API about our Smart Bin",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": ""
        },
        "version": "1.0.0",
        "basePath": "api",
        "schemes": ["http", "https"],
        "operationId": "getmybin"
    }
}

swagger = Swagger(app, template=template)

CORS(app, resource={
    r"/login/*": {
        'origins': '*'
    },
    r"/get/*": {
        'origins': '*'
    },
    r"/db/*": {
        'origins': '*'
    }
}, supports_credentials=True)

myconfig = Config
app.config.from_object(myconfig)
myutils = Utils()

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
        DEBUG=True,
        TESTING=False,
    )
    print("NOTE: Using docker debug config")
elif(getenv('FLASK_CONFIG') == 'local'):
    app.config.update(
        #SQLALCHEMY_DATABASE_URI = 'sqlite:///out.db',
        DEBUG=True,
        TESTING=False,
    )
    print("NOTE: Using local config")
elif(getenv('FLASK_CONFIG') == 'docker_production'):
    app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///database.db',
        DEBUG=False,
        TESTING=False,
    )
    print("NOTE: Using docker production config")
else:
    pass
    #raise RuntimeError("Wrong config, exiting..")


# Inizializzazione DB
db.init_app(app)

# Inizializzazione Bcrypt
bcrypt = bcrypt.init_app(app)
jwt.init_app(app)


# Registrazione Blueprint
app.register_blueprint(database_blueprint, url_prefix='/db')
app.register_blueprint(get_blueprint, url_prefix='/get')
app.register_blueprint(set_blueprint, url_prefix='/set')
app.register_blueprint(check_blueprint, url_prefix='/check')
app.register_blueprint(neighbor_blueprint, url_prefix='/neighbor')
app.register_blueprint(path_blueprint, url_prefix='/bpath')
app.register_blueprint(map_blueprint, url_prefix='/map')
app.register_blueprint(fbprophet_blueprint, url_prefix='/pred')
app.register_blueprint(handler_blueprint)
app.register_blueprint(login_blueprint)
