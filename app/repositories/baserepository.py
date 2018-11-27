from app.instance.config import app_config
import os
from pymongo import MongoClient
from app.exceptions.repositoryexception import RepositoryException


class BaseRepository():
    def __init__(self):
        try:
            config_name = os.getenv('APP_SETTINGS')
            self.config = app_config[config_name]
            connstr = self.config.MONGODB_CONNSTR.format(os.getenv('MONGODB_USER'), os.getenv('MONGODB_PASSWORD'))
            client = MongoClient(connstr)
            self.db = client[self.config.CATALOG_NAME]
        except Exception as e:
            raise RepositoryException(*e.args, **e.kwargs)

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        return