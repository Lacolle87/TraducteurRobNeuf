import os
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger(log_file='bot.log'):
    logs_folder = 'logs'

    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    log_basename = os.path.splitext(log_file)[0]  # Extracting the base name without extension
    log_path = os.path.join(logs_folder, log_file)

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    handler = TimedRotatingFileHandler(log_path, when='W0', interval=1, backupCount=4)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
