import asyncio
import discord
from discord import Webhook
import aiohttp
from core.scrapers.character_stats import CharacterStats


async def send_webhook(url):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)

        data = []
        for username in ["NotCrostyGIM", "NotPlucksGIM", "Zehahandsome", "Zolixo1"]:
            data.append("\n")
            scraper = CharacterStats(username)
            character = scraper.get_character_stats()
            data.append(repr(character))
        
        data = "".join(data)
        embed = discord.Embed(title="OSRS Skill overview", description=data)
        await webhook.send(embed=embed, username="OSRS Bot")


url = (
    "https://discord.com/api/webhooks/1187456676496949338/SyAgqTj8_6qSw24wrrY8hpTIGVgI1OaKtyha-zjvfeKUzbsQMj9ajmdR-1TyVxkfgQgl"
)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_webhook(url))
