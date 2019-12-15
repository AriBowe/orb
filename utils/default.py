import json
import time
import timeago as timesince
from collections import namedtuple


def get(file):
    """
    Reads a json file.

    Params:
        (str) file: JSON file
    Returns:
        (obj): Python object
    """
    try:
        with open(file, encoding='utf8') as data:
            # custom decoder for the JSON file; converts JSON data into a Python object
            # taken from here: https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
            return json.load(data,
                             object_hook=lambda dictionary: namedtuple('X', dictionary.keys())(*dictionary.values())
                             )

    except AttributeError:
        raise AttributeError('Invalid argument.')

    except FileNotFoundError:
        raise FileNotFoundError('JSON file not found.')


def create_time_text(name):
    """Creates a name for a text that contains the time at which it was created."""
    return f'{name}_{int(time.time())}.txt'


def timeago(time_interval):
    return timesince.format(time_interval)