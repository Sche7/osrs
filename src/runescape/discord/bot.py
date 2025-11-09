import os

import dotenv
from discord import ApplicationContext
from discord.ext import commands

from runescape.api.osrs.hiscores import Hiscores

dotenv.load_dotenv()
bot = commands.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="hiscore")
async def hiscore(ctx: ApplicationContext, username):
    if username is not None:
        try:
            user = Hiscores(username)
            await ctx.respond(repr(user.character))
        except ValueError:
            await ctx.respond(f"Could not find user with name {username}")
    else:
        await ctx.respond("Please provide a username.")


token = str(os.getenv("DISCORD_BOT_TOKEN"))
bot.run(token)
