import os
import logging


def setup_logger(log_file='bot.log'):
    logs_folder = 'logs'

    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    log_path = os.path.join(logs_folder, log_file)
    logging.basicConfig(
        filename=log_path,
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
