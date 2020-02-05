import json
from bunch import bunchify


def get_constants():
    with open('./values/default.json', 'r') as config_file:
        config_dict = json.load(config_file)
    config = bunchify(config_dict)
    return config, config_dict
