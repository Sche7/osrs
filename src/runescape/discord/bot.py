import os

import dotenv
from discord import ApplicationContext
from discord.ext import commands
from loguru import logger

from runescape.api.osrs.hiscores import Hiscores

bot = commands.Bot()


@bot.event
async def on_ready() -> None:
    logger.info(f"{bot.user} is ready and online!")


@bot.slash_command(name="hiscore")
async def hiscore(ctx: ApplicationContext, username) -> None:
    logger.info(f"Retrieving hiscore for user [{username}]")
    if username is not None:
        try:
            user = Hiscores(username)
            logger.info(f"Hiscore successfully retrieved for user [{username}]")
            output = "```apache\n" + repr(user.character) + "```"
            await ctx.respond(output)
        except ValueError as e:
            logger.error(
                f"Could not retrieve hiscore for user [{username}] with error: {e}"
            )
            await ctx.respond(
                f"```apache\nCould not find user with name [{username}].```"
            )
    else:
        await ctx.respond("```apache\nPlease provide a username.```")


def main():
    dotenv.load_dotenv()
    token = os.getenv("DISCORD_BOT_TOKEN")
    if token is None:
        raise ValueError("DISCORD_BOT_TOKEN has not been set.")
    bot.run(token)
