import os
from app import create_app
#from app.models import User, Role
# from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'docker')
# migrate = Migrate(app, db)