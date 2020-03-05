import json
import discord
import os

from urllib.request import urlopen
from urllib.parse import quote as urlquote

DICT_URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
DICT_KEY = os.environ['DICT_KEY']

TEST_URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/umpire?key=2213b92f-27e9-4c64-8099-330af1374f17"

class Definition:
    """
    This class represents a Definition object, with the attributes

        word (str): the word itself
        defn (list): the definition of the word (list attr in case there are multiple defs)
        syns (list): synonyms for the word (contained as list object)
        examp: an example of the word being used in a sentence
        offens (Bool): True if word is offensive, False otherwise
    """
    def __init__(self, word, defn, syns, examp, offens):
        self.word = word
        self.defn = defn
        self.syns = syns
        self.examp = examp
        self.offens = offens

    def get_word(self):
        """

        :return:
        """
        return self.word

    def get_defn(self):
        return self.defn

    def get_syns(self):
        return self.syns

    def get_examp(self):
        return self.examp

    def get_offens(self):
        return self.offens

    def __str(self):
        return '%s: %s %s %s %s ' %(
            self.word,
            self.defn,
            self.syns,
            self.examp,
            self.offens
        )

def _get_dict_json(url):
    file = urlopen(url)
    data = json.loads(file.read().decode('utf-8'))
    file.close()
    return data

def _parse_dict_json(word):
    """
    Parses the JSON data and returns a Definition object

    Params:
        data (dict): JSON data from the API
        word (str): word requiring definition

    Returns:
        word_data (Definition): contains all info about word (word itself, definition, synonyms, example sentence,
        and whether or not it's offensive)
    """

    URL = DICT_URL + word + DICT_KEY
    data = _get_dict_json(URL)[1]['meta']

    try:

        word_data = Definition(
            data[1]['meta']['id'],
            [
                data[1]['def'][0]['sseq'][0][0][1]['dt'][0][1],
                data[1]['shortdef'][0]
            ],
            data[1]['meta']['syns'][0],
            data[1]['def'][0]['sseq'][0][0][1]['dt'][1][1][0]['t'],
            data[0]['meta']['offensive']
        )

        return word_data

    except KeyError:
        suggestion = ""
        for word in data:
            suggestion += f"{word}, "

        return f"Did you mean {suggestion}"

def send_def(ctx, word):
    raise NotImplementedError
