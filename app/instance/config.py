class Config:
    """Parent configuration class."""
    DEBUG = True
    CSRF_ENABLED = True
    ENV = ""


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    ENV = ""
    MONGODB_CONNSTR = 'mongodb://{0}:{1}@cluster0-shard-00-00-uu4dq.mongodb.net:27017,cluster0-shard-00-01-uu4dq.mongodb.net:27017,cluster0-shard-00-02-uu4dq.mongodb.net:27017/TestDb?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
    CATALOG_NAME = 'PlaynaccleDb'
    IMPORT_API_URL = 'https://www.giantbomb.com/api/'


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
