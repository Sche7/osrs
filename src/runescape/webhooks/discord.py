import asyncio
import datetime
import os

import aiohttp
import discord
from botocore.exceptions import ClientError
from discord import Webhook

from runescape.api.osrs.hiscores import Hiscores
from runescape.dataclasses.character import Character
from runescape.storage.aws.errors import BotoErrorCode
from runescape.storage.aws.s3 import S3Storage
from runescape.utils.osrs import (
    HiscoreProgress,
    evaluate_hiscore_progress,
    get_hiscore_from_storage,
    save_hiscore_to_storage,
)


def generate_message(progress: HiscoreProgress) -> str:
    """Generate a message from the progress dict from
    the function `evaluate_hiscore_progress`.
    """
    message = []
    # Construct the message
    if progress.experience_difference > 0:
        message.append(f"Experience progress: {progress.experience_difference:,d}\n")
        message.append(f"Combat level progress: {progress.combat_level_difference:,d}\n")
        message.append(f"Total level: {progress.current_total_level}\n")
        message.append(f"Total combat level: {progress.current_combat_level}\n")
        message.append(f"Progress time: {progress.time_difference}\n")
        if progress.combat_level_difference > 0:
            message.append(
                f"Combat level up from {progress.previous_combat_level} -> {progress.current_combat_level}\n"
            )
        if progress.total_level_difference > 0:
            message.append(
                f"Total level up from {progress.previous_total_level} -> {progress.current_total_level}\n"
            )

        message.append("\n")
        message.append("**Skills:**\n")
        for skill in progress.skills:
            if skill.experience_difference > 0:
                message.append(f"\t*{skill.skill_name}*:\n")
                message.append(f"\t\tLevel progress: {skill.level_difference:,d}\n")
                message.append(
                    f"\t\tExperience progress: {skill.experience_difference:,d}\n"
                )
                if skill.current_level - skill.previous_level > 0:
                    message.append(
                        f"\t\tLevel up from {skill.previous_level} -> {skill.current_level}\n"
                    )
                message.append("\n")
    return "".join(message)


async def get_hiscores_webhook(url, usernames: list[str]):
    """Get the hiscores for the given usernames and send them to a Discord webhook."""
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        for username in usernames:
            hiscore = Hiscores(username)
            character = hiscore.character
            now = datetime.datetime.now()
            embed = discord.Embed(
                title=username,
                description=repr(character),
                color=5763719,  # Green
                timestamp=now,
            )
            await webhook.send(embed=embed, username="OSRS Bot")


async def get_character_progress_webhook(
    url, usernames: list[str], bucket_name: str, remote_folder: str
):
    """Send a webhook with the progress of the hiscores."""
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)

        for username in usernames:
            hiscore = Hiscores(username)
            current = hiscore.character

            storage = S3Storage(bucket_name=bucket_name)
            previous_stats = None
            # Download previous stats from S3 if it exists.
            # Exception is thrown if the file does not exist.
            try:
                # Attempt to download the file
                previous_stats = get_hiscore_from_storage(
                    username=username,
                    storage=storage,
                )
            except ClientError as ex:
                # Raise the exception if it is not a NoSuchKey error
                if ex.response.get("Error", {}).get("Code") != BotoErrorCode.NO_SUCH_KEY:
                    raise

            # If character_dict is None, it means that the file does not exist.
            # In this case, we create one in S3.
            if previous_stats is not None:
                previous = Character(**previous_stats)

                result = evaluate_hiscore_progress(
                    previous=previous,
                    current=current,
                )
                message = generate_message(result)

                # Only send the webhook if there is progress
                now = datetime.datetime.now()
                if message != "":
                    embed = discord.Embed(
                        title=username,
                        description=message,
                        color=5763719,  # Green
                        timestamp=now,
                    )
                    await webhook.send(embed=embed, username="OSRS Bot")

            # Save the current stats to S3
            save_hiscore_to_storage(
                character=current,
                storage=storage,
                remote_folder=remote_folder,
            )


def main(usernames, bucket_name, remote_folder):
    url = os.getenv("DISCORD_WEBHOOK")

    if url is None:
        raise ValueError("DISCORD_WEBHOOK environment variable is not set.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        get_character_progress_webhook(
            url=url,
            usernames=usernames,
            bucket_name=bucket_name,
            remote_folder=remote_folder,
        )
    )


if __name__ == "__main__":
    USERNAMES = ["NotCrostyGIM", "NotPlucksGIM", "Zehahandsome", "Zolixo1"]
    BUCKET_NAME = "osrsbucket"
    REMOTE_FOLDER = "hiscores"

    main(USERNAMES, BUCKET_NAME, REMOTE_FOLDER)
