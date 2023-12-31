import os
from datetime import datetime
from typing import Iterator
from core.api.osrs.hiscores import Hiscores
from core.dataclasses.character import DATETIME_FORMAT
from core.storage.aws.s3 import S3Storage
from core.storage.json import JSONStorage
from dataclasses import asdict
from botocore.exceptions import ClientError


REMOTE_FOLDER = "hiscores"


def get_hiscores(usernames: list[str]) -> Iterator[Hiscores]:
    for username in usernames:
        try:
            yield Hiscores(username)
        except Exception as e:
            print(str(e))
            continue


def save_hiscores_in_s3(
    usernames: list[str],
    bucket_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    remote_folder: str = REMOTE_FOLDER,
    tmp_dir: str = "downloads",
) -> None:
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    aws_storage = S3Storage(
        aws_access_key_id,
        aws_secret_access_key,
        bucket_name,
    )
    json_storage = JSONStorage()

    for hiscore in get_hiscores(usernames):
        username = hiscore.character.username
        character = asdict(hiscore.character)

        character_stats = None
        result = None
        # Download the file if it exists
        remote_filepath = os.path.join(remote_folder, f"{username}.json")
        try:
            # Attempt to download the file
            download_path = aws_storage.load(remote_filepath)

            # If the file exists, load it
            character_stats = json_storage.load(download_path)
        except ClientError:
            pass

        # If the file does not exist, create a new one
        # Otherwise, append the new stats to the history
        if character_stats is None:
            result = {
                "username": username,
                "stats": character,
                "history": [character],
            }
        else:
            character_stats["stats"] = character
            character_stats["history"].append(character)
            result = character_stats

        # Save the file to the local filesystem
        filepath = f"{tmp_dir}/{username}.json"
        json_storage.save(result, filepath)

        # Upload the file to S3
        aws_storage.save(filepath, remote_filepath)


def evaluate_hiscore_progress(
    username: str,
    tmp_dir: str = "downloads",
) -> dict[str, int]:
    json_storage = JSONStorage()
    # Download the file if it exists
    filepath = os.path.join(tmp_dir, f"{username}.json")

    # If the file exists, load it
    character_stats = json_storage.load(filepath)

    # Get the last entry
    current_stats = character_stats["history"][-1]
    current_date = datetime.strptime(current_stats["date"], DATETIME_FORMAT)

    # Get the second to last entry
    prev_stats = character_stats["history"][-2]
    prev_date = datetime.strptime(prev_stats["date"], DATETIME_FORMAT)

    # Calculate the difference in experience
    experience_difference = (
        current_stats["total_experience"] - prev_stats["total_experience"]
    )

    # Calculate the difference in combat level
    combat_level_difference = current_stats["combat_level"] - prev_stats["combat_level"]

    difference = {}
    for skill_name, skill in current_stats["skills"].items():
        difference[skill_name] = {
            "level": skill["level"] - prev_stats["skills"][skill_name]["level"],
            "experience": skill["experience"]
            - prev_stats["skills"][skill_name]["experience"],
        }

    return {
        "username": username,
        "experience_difference": experience_difference,
        "combat_level_difference": combat_level_difference,
        "time_difference": str(current_date - prev_date),
        "skills": difference,
    }
