import logging
import os
from logging.handlers import TimedRotatingFileHandler
from instance.config import app_config

def setup_custom_logger(name):
    config = app_config[os.getenv('APP_SETTINGS')]
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = TimedRotatingFileHandler(config.LOG_PATH, when='midnight')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
