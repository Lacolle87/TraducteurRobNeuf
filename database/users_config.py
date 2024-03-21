import json

CONFIG_FILE = 'database/users_config.json'


def load_users_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            users_config = json.load(file)
            return users_config
    except FileNotFoundError:
        users_config = {}
        return users_config


def save_users_config(users_config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(users_config, file, indent=4)
