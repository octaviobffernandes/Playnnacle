import os


class Config(object):
    """Parent configuration class."""
    DEBUG = True
    CSRF_ENABLED = True
    ENV = ""


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    ENV = ""
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'redsfsfsfsfis'


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    ENV = ""
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'redsfsfsfsfis'


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
    ENV = ""
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'redsfsfsfsfis'


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
