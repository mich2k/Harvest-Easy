from datetime import timedelta


class Config:

    # General Flask Config
    SECRET_KEY = b''
    USE_PROXYFIX = True

    APPLICATION_ROOT = '/'

    FLASK_APP = 'main.py'
    FLASK_RUN_HOST = '0.0.0.0'
    FLASK_RUN_PORT = 5000

    FLASK_DEBUG = 1
    FLASK_ENV = "development"  # production
    # FLASK_ENV = "production"  # production

    DEBUG = False
    TESTING = False  # True

    SESSION_TYPE = 'sqlalchemy'  # "redis"
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_COOKIE_NAME = 'my_cookieGetFace'
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    # SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")

    # Database
    # = 'mysql://username:password@localhost/db_name'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "simple"  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 100

    BCRYPT_LOG_ROUNDS = 13

    JWT_SECRET_KEY = "sec_key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
