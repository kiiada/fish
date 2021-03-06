import discord
from redbot.core import commands, bot, Config

from .eris_event_lib import ErisEventMixin

BaseCog = getattr(commands, "Cog", object)


class Sudo(BaseCog, ErisEventMixin):
    def __init__(self, bot_instance: bot):
        super().__init__()
        self.bot = bot_instance

        self.whois = self.bot.get_cog("WhoIs")

        self.bot.add_listener(self.no_sudo, "on_message")

    async def no_sudo(self, message: discord.Message):
        ctx = await self.bot.get_context(message)

        async with self.lock_config.channel(message.channel).get_lock():
            allowed: bool = await self.allowed(ctx, message)
            keyword_in_message: bool = 'sudo' in message.clean_content

            if not allowed or not keyword_in_message:
                return

            author: discord.Member = message.author
            realname = author.mention
            if self.whois is not None:
                realname = self.whois.convert_realname(await self.whois.get_realname(ctx, str(author.id)))

            await message.channel.send("{} is not in the sudoers file. This incident will be reported.".format(realname))

            await self.log_last_message(ctx, message)

