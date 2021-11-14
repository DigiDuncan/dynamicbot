import logging
import sys

import discord
import discordplus
from discord import Bot
from digiformatter import digilogger

from dynamicbot.lib.loglevels import CMD, LOGIN
from dynamicbot.lib.utils import truncate

logging.basicConfig(level=CMD)
dfhandler = digilogger.DigiFormatterHandler()
dfhandler.setLevel(CMD)

logger = logging.getLogger("dynamicbot")
logger.setLevel(CMD)
logger.handlers = []
logger.propagate = False
logger.addHandler(dfhandler)

discordlogger = logging.getLogger("discord")
discordlogger.setLevel(logging.WARN)
discordlogger.handlers = []
discordlogger.propagate = False
discordlogger.addHandler(dfhandler)

initial_cogs = [
    "admin"
]
initial_extensions = []

discordplus.patch()

with open("_AUTHTOKEN") as f:
    token = f.read().strip()


def main():
    bot = Bot(command_prefix = "~", allowed_mentions = discord.AllowedMentions(everyone=False), intents=discord.Intents.all(), case_insensitive=True)

    bot.remove_command("help")

    for extension in initial_extensions:
        bot.load_extension("sizebot.extensions." + extension)
    for cog in initial_cogs:
        bot.load_extension("sizebot.cogs." + cog)
    bot.load_extension("sizeroyale.cogs.royale")

    @bot.event
    async def on_first_ready():
        logger.log(LOGIN, f"Logged in as: {bot.user.name} ({bot.user.id})\n------")

        # Add a special message to bot status if we are running in debug mode
        activity = discord.Game(name = "dynamicness")
        if sys.gettrace() is not None:
            activity = discord.Activity(type=discord.ActivityType.listening, name = "DEBUGGER 🔧")

        # More splash screen.
        await bot.change_presence(activity = activity)

    @bot.event
    async def on_reconnect_ready():
        logger.error("dynamicbot has been reconnected to Discord.")

    @bot.event
    async def on_command(ctx):
        guild = truncate(ctx.guild.name, 20) if (hasattr(ctx, "guild") and ctx.guild is not None) else "DM"
        logger.log(CMD, f"G {guild}, U {ctx.message.author.name}: {ctx.message.content}")

    @bot.event
    async def on_message(message):
        # F*** smart quotes.
        message.content = message.content.replace("“", "\"")
        message.content = message.content.replace("”", "\"")
        message.content = message.content.replace("’", "'")
        message.content = message.content.replace("‘", "'")

        await bot.process_commands(message)

    @bot.event
    async def on_message_edit(before, after):
        if before.content == after.content:
            return
        await bot.process_commands(after)

    def on_disconnect():
        logger.error("SizeBot has been disconnected from Discord!")

    bot.run(token)
    on_disconnect()
