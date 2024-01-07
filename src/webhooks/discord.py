import asyncio
import discord
import aiohttp
import datetime
import os
from discord import Webhook
from src.utils.osrs import save_hiscores_in_s3, evaluate_hiscore_progress


USERNAMES = ["NotCrostyGIM", "NotPlucksGIM", "Zehahandsome", "Zolixo1"]
BUCKET_NAME = "osrsbucket"
REMOTE_FOLDER = "hiscores"


async def send_webhook(url):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)

        # Get the hiscores, sync them to S3, evaluate them
        # and send them to the Discord webhook.
        message = []
        for user_stats in save_hiscores_in_s3(
            usernames=USERNAMES,
            bucket_name=BUCKET_NAME,
            remote_folder=REMOTE_FOLDER,
        ):
            username = user_stats["username"]
            result = evaluate_hiscore_progress(user_stats)

            # Construct the message
            if result["experience_difference"] != 0:
                message.append(f"**{username}**\n")
                message.append(
                    f"Experience progress: {result['experience_difference']:,d}\n"
                )
                message.append(
                    f"Combat level progress: {result['combat_level_difference']:,d}\n"
                )
                message.append(f"Progress time: {result['time_difference']}\n")
                if result["combat_level_difference"] > 0:
                    message.append(
                        f"Combat level up from {result['previous_combat_level']} -> {result['current_combat_level']}\n"
                    )
                message.append("\n")
                message.append("**Skills:**\n")
                for skill_name, skill in result["skills"].items():
                    if skill["experience_difference"] != 0:
                        message.append(f"\t*{skill_name}*:\n")
                        message.append(
                            f"\t\tLevel progress: {skill['level_difference']:,d}\n"
                        )
                        message.append(
                            f"\t\tExperience progress: {skill['experience_difference']:,d}\n"
                        )
                        if skill["current_level"] - skill["previous_level"] > 0:
                            message.append(
                                f"\t\tLevel up from {skill['previous_level']} -> {skill['current_level']}\n"
                            )
                        message.append("\n")
                message.append("------------------------------------------------\n")

        now = datetime.datetime.now()
        message = "".join(message)

        # Only send the webhook if there is progress
        if message != "":
            embed = discord.Embed(
                title="OSRS Skill overview",
                description=message,
                color=5763719,  # Green
                timestamp=now,
            )
            await webhook.send(embed=embed, username="OSRS Bot")


def main():
    url = os.getenv("DISCORD_WEBHOOK")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_webhook(url))


if __name__ == "__main__":
    main()
