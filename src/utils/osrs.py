import os
import json
from datetime import datetime
from typing import Iterator
from src.api.osrs.hiscores import Hiscores
from src.dataclasses.character import DATETIME_FORMAT
from src.storage.aws.s3 import S3Storage
from src.storage.json import JSONStorage
from dataclasses import asdict
from botocore.exceptions import ClientError


REMOTE_FOLDER = "hiscores"


def get_hiscores(usernames: list[str]) -> Iterator[Hiscores]:
    """
    Convenience function for getting the hiscores for the given usernames.

    Example
    -------
    >>> usernames = ["NotCrostyGIM", "NotPlucksGIM", "Zehahandsome"]
    >>> for hiscore in get_hiscores(usernames):
    ...     print(hiscore.character)
    """
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
) -> None:
    """
    Pulls the hiscores for the given usernames and saves them to S3.
    This function will create a new file if it does not exist, or update
    the file if it does exist.

    It will not update the file if the stats have not changed.

    Example
    -------
    >>> save_hiscores_in_s3(
    ...     ["NotCrostyGIM", "NotPlucksGIM", "Zehahandsome"],
    ...     "osrs-hiscores",
    ...     "aws_access_key_id",
    ...     "aws_secret_access_key",
    ...     remote_folder="test",
    ... )
    """

    # Connect to S3
    aws_storage = S3Storage(
        aws_access_key_id,
        aws_secret_access_key,
        bucket_name,
    )

    # Get the hiscores for the given usernames
    for hiscore in get_hiscores(usernames):
        # Fetch current character stats
        username = hiscore.character.username
        current_stats = asdict(hiscore.character)

        new_stats = None
        previous_stats = None
        remote_filepath = os.path.join(remote_folder, f"{username}.json")
        
        # Download previous stats from S3 if it exists.
        # Exception is thrown if the file does not exist.
        try:
            # Attempt to download the file
            content = aws_storage.load(remote_filepath)
            previous_stats = json.loads(content)
        except ClientError as ex:
            if ex.response['Error']['Code'] != 'NoSuchKey':
                raise

        # If character_dict is None, it means that the file does not exist.
        # In this case, we create one in S3.
        if previous_stats is None:
            new_stats = {
                "username": username,
                "stats": current_stats,
                "history": [],
            }
            content = json.dumps(new_stats)
            aws_storage.save(content, remote_filepath)
        else:
            # Otherwise, if the file exists then add the previous stats to the history
            new_stats = {
                "username": username,
                "stats": current_stats,
                "history": previous_stats["history"] + [previous_stats["stats"]],
            }

            # If the stats have not changed, then we do not need to upload the file.
            if (current_stats["total_experience"] - previous_stats["stats"]["total_experience"] > 0):
                content = json.dumps(new_stats)
                aws_storage.save(content, remote_filepath)


def evaluate_hiscore_progress(
    username: str,
    tmp_dir: str = "downloads",
) -> dict[str, int]:
    """
    Evaluates the progress of the given username.

    Example
    -------
    >>> evaluate_hiscore_progress("NotCrostyGIM")
    {
        "username": "NotCrostyGIM",
        "experience_difference": 0,
        "combat_level_difference": 0,
        "previous_combat_level": 3,
        "current_combat_level": 3,
        "time_difference": "0:00:00",
        "skills": {
            "overall": {
                "level_difference": 0,
                "experience_difference": 0,
                "previous_level": 3,
                "previous_experience": 0,
                "current_level": 3,
                "current_experience": 0
            },
            "attack": {
                "level_difference": 0,
                "experience_difference": 0,
                "previous_level": 1,
                "previous_experience": 0,
                "current_level": 1,
                "current_experience": 0
            },
            "defence": {
                "level_difference": 0,
                "experience_difference": 0,
                "previous_level": 1,
                "previous_experience": 0,
                "current_level": 1,
                "current_experience": 0
            },
            "strength": {
                "level_difference": 0,
                "experience_difference": 0,
                "previous_level": 1,
                "previous_experience": 0,
                "current_level": 1,
                "current_experience": 0
            },
            "hitpoints": {
                "level_difference": 0,
                "experience_difference": 0,
                "previous_level": 10,
                "previous_experience": 1154,
                "current_level": 10,
                "current_experience": 1154
            },
            "ranged": {
                "level_difference": 0,
                "experience_difference": 0,
                "previous_level": 1,
                "previous_experience": 0,
                "current_level": 1,
                "current_experience": 0
            },
            "prayer": {
                "level_difference": 0,
                "experience_difference": 0,
                "previous_level": 1,
                "previous_experience": 0,
                "current_level": 1,
                "current_experience": 0
            },
            "magic": {
                "level_difference": 0,
                "experience_difference": 0,
                "previous_level": 1,
                "previous_experience": 0,
                "current

    """
    json_storage = JSONStorage()
    # Download the file if it exists
    filepath = os.path.join(tmp_dir, f"{username}.json")

    # If the file exists, load it
    character_stats = json_storage.load(filepath)

    # Get the last entry
    current_stats = character_stats["stats"]
    current_date = datetime.strptime(current_stats["date"], DATETIME_FORMAT)

    # Get the second to last entry
    history = character_stats["history"]
    if len(history) == 0:
        prev_stats = current_stats
    else:
        prev_stats = history[-1]

    prev_date = datetime.strptime(prev_stats["date"], DATETIME_FORMAT)

    # Calculate the difference in experience
    experience_difference = (
        current_stats["total_experience"] - prev_stats["total_experience"]
    )

    # Calculate the difference in combat level
    combat_level_difference = current_stats["combat_level"] - prev_stats["combat_level"]

    difference = {}
    for skill_name, skill in current_stats["skills"].items():
        prev_skill = prev_stats["skills"][skill_name]
        skill_info = {
            "level_difference": skill["level"] - prev_skill["level"],
            "experience_difference": skill["experience"] - prev_skill["experience"],
            "previous_level": prev_skill["level"],
            "previous_experience": prev_skill["experience"],
            "current_level": skill["level"],
            "current_experience": skill["experience"],
        }
        difference[skill_name] = skill_info

    return {
        "username": username,
        "experience_difference": experience_difference,
        "combat_level_difference": combat_level_difference,
        "previous_combat_level": prev_stats["combat_level"],
        "current_combat_level": current_stats["combat_level"],
        "time_difference": str(current_date - prev_date),
        "skills": difference,
    }
