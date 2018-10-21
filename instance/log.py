import logging
import os
from logging.handlers import TimedRotatingFileHandler
from instance.config import app_config


def setup_custom_logger(name):
    config = app_config[os.getenv('APP_SETTINGS')]
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    file_handler = TimedRotatingFileHandler(os.getenv('LOG_PATH'), when='midnight')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
