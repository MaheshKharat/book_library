import os


class Config:
    SECRET_KEY = '77267359473df1bc1afc54529cbc5e36a8c8283b'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///book_library.db'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False


class DebugConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


config_dict = {
    'Production': ProductionConfig,
    'Development': DevelopmentConfig,
    'Debug': DebugConfig
}


def load(app):
    config_mode = config_dict['Development']
    app.config.from_object(config_mode)
