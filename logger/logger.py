import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def setup_logger(logs_folder='logs', log_file='bot.log'):
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    log_path = os.path.join(logs_folder, log_file)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(log_path, when='W0', interval=1, backupCount=3)
    handler.suffix = '%d'
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
