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
    tmp_dir: str = "downloads",
) -> None:
    """
    Pulls the hiscores for the given usernames and saves them to S3.

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

        character_dict = None
        result = None
        # Download the file if it exists
        remote_filepath = os.path.join(remote_folder, f"{username}.json")
        try:
            # Attempt to download the file
            content = aws_storage.load(remote_filepath)
            character_dict = json.loads(content)

        except ClientError:
            pass

        # If the file does not exist, then create one
        # Otherwise, append the new stats to the history
        if character_dict is None:
            result = {
                "username": username,
                "stats": character,
                "history": [],
            }
        else:
            # Add the previous stats to the history
            character_dict["history"].append(character_dict["stats"])

            # Update the stats
            character_dict["stats"] = character
            result = character_dict

        # Save the file to the local filesystem
        filepath = f"{tmp_dir}/{username}.json"
        json_storage.save(result, filepath)

        # Upload the file to S3
        aws_storage.save(filepath, remote_filepath)


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
