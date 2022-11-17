import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #SERVER_NAME = 'iotbackend.gmichele.it:5000'
    #SERVER_PORT = os.environ.get('SERVER_PORT') or '5000'
    #MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    #MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
    #    ['true', 'on', '1']
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    #FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    #FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    #SSL_REDIRECT = False
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_RECORD_QUERIES = True
    #FLASKY_POSTS_PER_PAGE = 20
    #FLASKY_FOLLOWERS_PER_PAGE = 50
    #FLASKY_COMMENTS_PER_PAGE = 30
    #FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig():
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    pass

class DockerConfig(Config):
 @classmethod
 def init_app(cls, app):
    # log to stderr
    import logging
    from logging import StreamHandler
    file_handler = StreamHandler()
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
config = {
 'docker': DockerConfig,
}