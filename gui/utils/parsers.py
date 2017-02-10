import json
import os


def conversion(options, key):
    """ Tries to return the value of a given key of given dict

    :returns None if keyerror, otherwise the value
    """
    try:
        return options[key].get()
    except KeyError:
        return None


def get_from_config(key, file_path):
    """
    :param key: The key from the config file
    :param file_path: the main filepath where config is located

    :return: The value associated to the key in the config file
    """
    with open(os.path.join(file_path, 'config.json')) as file:
        data = json.load(file)
        return data[key]
