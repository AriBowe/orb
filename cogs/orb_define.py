import discord
import os
import requests 

from discord.ext import commands 


DICT_URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
DICT_KEY = os.environ['DICT_KEY']


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
    return requests.get(url=url).json()

def _parse_dict_json(word):
    """
    Parses the JSON data and returns a Definition object

    Params:
        word (str): word requiring definition

    Returns:
        word_data (Definition): contains all info about word (word itself, definition, synonyms, example sentence,
        and whether or not it's offensive)
    """

    URL = DICT_URL + str(word) + f"?key={DICT_KEY}"
    data = _get_dict_json(URL)
    try:
        defn_obj = Definition(
            data[0]['meta']['id'],
            data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1],
            data[0]['meta']['syns'][0],
            data[0]['def'][0]['sseq'][0][0][1]['dt'][1][1][0]['t'],
            data[0]['meta']['offensive']
        )

        return defn_obj

    except TypeError:
        suggestion = ""
        if len(data) == 1:
            return data[0]
        else:
            for word in data:
                suggestion += f"{word}, "

        return f"The request word could not be found ;A; did you mean any of the following? \n{suggestion}"

    except IndexError:
        defn_obj = Definition(
            data[0]['meta']['id'],
            data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1],
            data[0]['meta']['syns'][0],
            "No examples could be found.",
            data[0]['meta']['offensive']
        )
        return defn_obj

def _create_embed(ctx, word):
    """
    Creates a discord.Embed object with info on word

    Params:
        ctx: context
        word (str): word to be looked up
    Returns:
        embed (discord.Embed): discord embed containing relevant info on word
    """
    definition = _parse_dict_json(word)

    try:
        syn_string = ""
        n = 0
        if len(definition.get_syns()) == 1:
            return syn_string + definition.get_syns()[0]
        else:
            for syn in definition.get_syns():
                if definition.get_syns() is False:
                    return "No synonyms could be found for this word"
                else:
                    n += 1
                    syn_string += f"{n}. {syn}\n"

        embed = discord.Embed(
            title=definition.get_word(),
            description=f"__**Definition**__\n {definition.get_defn()}\n "
            f"__**Synonyms**__\n {syn_string}\n"
            f"__**Example**__\n {definition.get_examp()}"
        )
        embed.set_footer(text=f"Definition requested by {ctx.author.name}.")

        return embed

    except AttributeError:
        return definition

class Define(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def define(self, ctx, word):
        """
        Defines a word using Merrian-Webster Dictionary
        """
        embed = _create_embed(ctx, word)
        try:
            await ctx.send(embed=embed)
        except AttributeError:
            await ctx.send(embed)

def setup(bot):
    bot.add_cog(Define(bot))
