from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class DB_status:

    database = None
    already_done = False

    def setstatus(self, db, status):
        self.database = db
        self.already_done = status
