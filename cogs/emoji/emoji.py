import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from typing import Union

class Emoji:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def emoji(self, ctx, emoji: Union[str, discord.Emoji]):
        """ Expand an emoji """
        print(emoji)
        print(emoji.url)
        await self.bot.say(emoji)


def setup(bot):
    n = Emoji(bot)
    bot.add_cog(n)
