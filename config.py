import os
basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.db')
#SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

#WTF_CSRF_ENABLED = True
#SECRET_KEY = 'you-will-never-guess'

#OPENID_PROVIDERS = [
#        {'name':'Google','url':'https://www.google.com/accounts/o8/id'},
#        {'name':'Yahoo','url':'https://me.yahoo.com'},
#        {'name':'AOL','url':'http://openid.aol.com/<username>'},
#        {'name':'Flickr','url':'http://flickr.com/<username>'},
#        {'name':'MyOpenID','url':'https://www.myopenid.com'}]

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <peng.weilin@yahoo.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')  or \
            'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
            'sqlite:///' + os.path.join(basedir,'data-test.sqlite')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir,'data.sqlite')

    MAIL_SERVER = 'smtp.mail.yahoo.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @classmethod
    def init_app(cls,app):
        Config.init_app(app)

        """
        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls,'MAIL_USERNAME',None) is not None:
            credentials = (cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
            if getattr(cls,'MAIL_USE_TLS',None):
                secure = ()
        mail_handler = SMTPHandler(
                mailhost=(cls.MAIL_SERVER,cls.MAIL_PORT),
                fromaddr=cls.FLASKY_MAIL_SENDER,
                toaddrs=[cls.FLASKY_ADMIN],
                subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + 'Application Error',
                credentials=credentials,
                secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        """

class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE')) or True

    @classmethod
    def init_app(cls,app):
        ProductionConfig.init_app(app)

        #handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

config = {
        'development':DevelopmentConfig,
        'testing':TestingConfig,
        'production':ProductionConfig,
        'default':DevelopmentConfig,
        'heroku':HerokuConfig,
        }
