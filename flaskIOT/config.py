class Config:

    # General Flask Config
    SECRET_KEY = b'ergergergergegg/'
    USE_PROXYFIX = True

    APPLICATION_ROOT = '/'

    FLASK_APP = 'flasky.py'
    FLASK_RUN_HOST = '0.0.0.0'
    FLASK_RUN_PORT = 5000

    FLASK_DEBUG = 1
    FLASK_ENV = "development" #production
    #FLASK_ENV = "production"  # production

    DEBUG = False
    TESTING = False #True

    SESSION_TYPE = 'sqlalchemy' #'redis'
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_COOKIE_NAME = 'my_cookieGetFace'
    SESSION_PERMANENT = True

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"  # = 'mysql://username:password@localhost/db_name'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "simple"  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT =  100
