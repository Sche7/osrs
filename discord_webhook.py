import asyncio
import discord
import aiohttp
import datetime
import os
from dotenv import load_dotenv
from discord import Webhook
from core.api.osrs.hiscores import Hiscores


load_dotenv()  # take environment variables from .env.


async def send_webhook(url):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)

        data = []
        for username in ["NotCrostyGIM", "NotPlucksGIM", "Zehahandsome", "Zolixo1"]:
            data.append("\n")
            hiscore = Hiscores(username)
            data.append(repr(hiscore.character))

        now = datetime.datetime.now()
        data = "".join(data)
        embed = discord.Embed(
            title="OSRS Skill overview",
            description=data,
            color=5763719,  # Green
            timestamp=now,
        )
        await webhook.send(embed=embed, username="OSRS Bot")


if __name__ == "__main__":
    url = os.getenv("DISCORD_WEBHOOK")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_webhook(url))
