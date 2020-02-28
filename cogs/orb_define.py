import json
import discord

from urllib.request import urlopen
from urllib.parse import quote as urlquote


class Definition:
    """
    This class represents a Definition object, with the attributes:
    word: the word itself
    defn: the definition of the word
    syns: synonyms for the word
    examp: an example of the word being used in a sentence
    offens (Boolean): True if word is offensive, False otherwise
    """
    def __init__(self, word, defn, syns, examp, offens):
        self.word = word
        self.defn = defn
        self.syns = syns
        self.examp = examp
        self.offens = offens

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

def _parse_dict_json(data):
    raise NotImplementedError

