import json
import discord
import os

from urllib.request import urlopen

DICT_URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
DICT_KEY = os.environ['DICT_KEY']

TEST_URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/umpire?key=2213b92f-27e9-4c64-8099-330af1374f17"

class Definition:
    """
    This class represents a Definition object, with the attributes

        word (str): the word itself
        defn (list): the definition of the word (list attr in case there are multiple defs)
        syns (list): synonyms for the word (contained as list object)
        examp (str): an example of the word being used in a sentence
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

        return f"The request word could not be found ;A; did you mean {suggestion}?"

def send_def(ctx, word):
    definition = _parse_dict_json(word)

    syn_string = ""
    n = 0
    for syn in definition.get_syn():
        if definition.get_syn() is False:
            return "No synonyms could be found for this word"
        else:
            n += 1
            syn_string += f"{n}. {word}\\"

    embed = discord.Embed(
        title=definition.get_word(),
        description=f"1. {definition.get_defn[0]}\\ "
        f"2. {definition.get_defn()[1]}\\"
        f"__**Synonyms**__\\ {syn_string}\\"
        f"__**Example**__\\{definition.get_examp()}",
        footer=f"Definition request by {ctx.author.name}."
    )

    await ctx.message.channel.send(embed)
    
   class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def define(self, ctx, word):
        """
        Defines a word using Merrian-Webster Dictionary
        """
        embed = _create_embed(ctx, word)
        ctx.send(embed)
     
def setup(bot):
    bot.add_cog(Define(bot))
