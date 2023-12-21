import asyncio
import discord
import aiohttp
import datetime
from discord import Webhook
from core.api.hiscores import Hiscores


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
            title="OSRS Skill overview", description=data, color=5763719, timestamp=now
        )
        await webhook.send(embed=embed, username="OSRS Bot")


url = "https://discord.com/api/webhooks/1187456676496949338/SyAgqTj8_6qSw24wrrY8hpTIGVgI1OaKtyha-zjvfeKUzbsQMj9ajmdR-1TyVxkfgQgl"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_webhook(url))
