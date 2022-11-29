from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
db = SQLAlchemy()
database_blueprint = Blueprint('database', __name__, template_folder='templates')
