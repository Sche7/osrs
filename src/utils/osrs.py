import os
import json
from datetime import datetime
from typing import Iterator
from src.api.osrs.hiscores import Hiscores
from src.dataclasses.character import DATETIME_FORMAT
from src.storage.aws.s3 import S3Storage
from dataclasses import asdict
from botocore.exceptions import ClientError


REMOTE_FOLDER = "hiscores"


def save_hiscores_in_s3(
    usernames: list[str],
    bucket_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    remote_folder: str = REMOTE_FOLDER,
) -> dict:
    """
    Pulls the hiscores for the given usernames and saves them to S3.
    This function will create a new file if it does not exist, or update
    the file if it does exist.
    It will not update the file if the stats have not changed.

    Returns
    -------
    dict
        The most recent stats for the given usernames.
        Note that the returned dict may not be the same as the stats
        that are saved in S3. This is because the stats are updated
        in S3 only if they have changed. The returned dict will always
        be the most recent stats, even if they have not changed.

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
    # Get the hiscores for the given usernames
    for username in usernames:
        try:
            yield save_hiscore_in_s3(
                username,
                bucket_name,
                aws_access_key_id,
                aws_secret_access_key,
                remote_folder=remote_folder,
            )
        except Exception as e:
            print(str(e))
            continue


def save_hiscore_in_s3(
    username: str,
    bucket_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    remote_folder: str = REMOTE_FOLDER,
) -> dict:
    """
    Pulls the hiscores for the given username and saves them to S3.
    This function will create a new file if it does not exist, or update
    the file if it does exist.
    It will not update the file if the stats have not changed.

    Returns
    -------
    dict
        The most recent stats for the given username.
        Note that the returned dict may not be the same as the stats
        that are saved in S3. This is because the stats are updated
        in S3 only if they have changed. The returned dict will always
        be the most recent stats, even if they have not changed.

    Example
    -------
    >>> save_hiscore_in_s3(
    ...     "NotCrostyGIM",
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

    # Get the hiscores for the given username
    hiscore = Hiscores(username)

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
        if ex.response["Error"]["Code"] != "NoSuchKey":
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
        if (
            current_stats["total_experience"]
            - previous_stats["stats"]["total_experience"]
            > 0
        ):
            content = json.dumps(new_stats)
            aws_storage.save(content, remote_filepath)

    return new_stats


def evaluate_hiscore_progress(stats: dict) -> dict[str, int]:
    """
    Evaluates the progress of the given username.
    Fetches the stats from S3 and calculates the difference between the
    last two entries.

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
    username = stats["username"]
    current_stats = stats["stats"]
    current_date = datetime.strptime(current_stats["date"], DATETIME_FORMAT)

    # Get the second to last entry
    history = stats["history"]
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
