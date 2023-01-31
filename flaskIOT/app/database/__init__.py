from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields


db = SQLAlchemy()
ma = Marshmallow()
#api = Api()

class DB_status:

    database = None
    already_done = False

    def setstatus(self, db, status):
        self.database = db
        self.already_done = status
