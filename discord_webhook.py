import asyncio
import discord
import aiohttp
import datetime
import os
from dotenv import load_dotenv
from discord import Webhook
from core.utils.osrs import save_hiscores_in_s3, evaluate_hiscore_progress


load_dotenv()  # take environment variables from .env.


USERNAMES = ["NotCrostyGIM", "NotPlucksGIM", "Zehahandsome", "Zolixo1"]
BUCKET_NAME = "osrsbucket"
REMOTE_FOLDER = "hiscores"
TMP_DIR = "downloads"


async def send_webhook(url):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)

        # Save the hiscores to S3
        # This will sync the hiscores to S3 and download them to the local machine
        # at tmp_dir.
        save_hiscores_in_s3(
            usernames=USERNAMES,
            bucket_name=BUCKET_NAME,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            remote_folder=REMOTE_FOLDER,
            tmp_dir=TMP_DIR,
        )

        # Get the hiscores from the local machine
        # and send them to the webhook
        data = []
        for username in USERNAMES:
            result = evaluate_hiscore_progress(username, TMP_DIR)

            if result["experience_difference"] != 0:
                data.append(f"**{username}**\n")
                data.append(f"Experience progress: {result['experience_difference']}\n")
                data.append(
                    f"Combat level progress: {result['combat_level_difference']}\n"
                )
                data.append(f"Progress time: {result['time_difference']}\n")
                data.append("\n")
                data.append("Skills:\n")
                for skill_name, skill in result["skills"].items():
                    if skill["experience_difference"] != 0:
                        data.append(f"\t{skill_name}:")
                        data.append(
                            f"\t\tLevel progress: {skill['level_difference']}\n"
                        )
                        data.append(
                            f"\t\tExperience progress: {skill['experience_difference']}\n"
                        )
                data.append("\n")

        now = datetime.datetime.now()
        data = "".join(data)

        # Only send the webhook if there is progress
        if data != "":
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
