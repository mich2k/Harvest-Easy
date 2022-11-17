from flask import Flask, render_template
#from flask_bootstrap import Bootstrap
from .main import main

# pg 111, Flask init factory pattern

#from flask_moment import Moment
#from flask_sqlalchemy import SQLAlchemy
import config



# bootstrap = Bootstrap()
# mail = Mail()
#moment = Moment()

# db = SQLAlchemy()
def create_app(config_name='docker'):
 app = Flask(__name__)
 from .main import main as main_blueprint
 app.register_blueprint(main_blueprint) #app.config.from_object(config.DockerConfig)
 #config[config_name].init_app(app)
 config.DockerConfig.init_app(app)
 # bootstrap.init_app(app)
 # mail.init_app(app)
 #moment.init_app(app)
 # db.init_app(app)
 # attach routes and custom error pages here
 return app
