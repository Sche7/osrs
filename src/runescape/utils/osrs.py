import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from botocore.exceptions import ClientError

from runescape.api.osrs.hiscores import Hiscores
from runescape.dataclasses.character import DATETIME_FORMAT, Character
from runescape.storage.aws.errors import BotoErrorCode
from runescape.storage.aws.s3 import S3Storage
from runescape.storage.protocol import StorageProtocol

REMOTE_FOLDER = "hiscores"


@dataclass
class SkillProgress:
    skill_name: str
    level_difference: int
    experience_difference: int
    previous_level: int
    previous_experience: int
    current_level: int
    current_experience: int


@dataclass
class HiscoreProgress:
    username: str
    experience_difference: int
    total_level_difference: int
    previous_total_level: int
    current_total_level: int
    combat_level_difference: int
    previous_combat_level: int
    current_combat_level: int
    time_difference: str
    skills: list[SkillProgress]


def save_hiscores_in_s3(
    usernames: list[str],
    bucket_name: str,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    remote_folder: str = REMOTE_FOLDER,
):
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


def get_hiscore_from_storage(
    username: str,
    storage: StorageProtocol,
    remote_folder: str = REMOTE_FOLDER,
) -> dict[str, Any]:
    """Fetches the hiscores for the given username from S3."""
    remote_filepath = Path(remote_folder) / f"{username}.json"

    # Attempt to download the file
    content = storage.load(str(remote_filepath))
    return json.loads(content)


def save_hiscore_to_storage(
    character: Character,
    storage: StorageProtocol,
    remote_folder: str = REMOTE_FOLDER,
) -> None:
    """Uploads the given stats to S3."""
    remote_filepath = Path(remote_folder) / f"{character.username}.json"
    content = json.dumps(asdict(character))
    storage.save(content, str(remote_filepath))


def save_hiscore_in_s3(
    username: str,
    bucket_name: str,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    remote_folder: str = REMOTE_FOLDER,
) -> Character:
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
        bucket_name=bucket_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # Get the hiscores for the given username
    hiscore = Hiscores(username)

    # Fetch current character stats
    username = hiscore.character.username
    current_stats = hiscore.character

    previous_stats = None
    # Download previous stats from S3 if it exists.
    # Exception is thrown if the file does not exist.
    try:
        # Attempt to download the file
        stats = get_hiscore_from_storage(
            username=username,
            storage=aws_storage,
        )
        previous_stats = Character(**stats)
    except ClientError as ex:
        # Raise the exception if it is not a NoSuchKey error
        if ex.response.get("Error", {}).get("Code") != BotoErrorCode.NO_SUCH_KEY:
            raise

    # If character_dict is None, it means that the file does not exist.
    # In this case, we create one in S3.
    if previous_stats is None:
        save_hiscore_to_storage(
            character=current_stats,
            storage=aws_storage,
            remote_folder=remote_folder,
        )
    else:
        # If the stats have not changed, then we do not need to upload the file.
        if current_stats.total_experience - previous_stats.total_experience > 0:
            save_hiscore_to_storage(
                character=current_stats,
                storage=aws_storage,
                remote_folder=remote_folder,
            )

    return current_stats


def evaluate_hiscore_progress(stats: dict) -> HiscoreProgress:
    """
    Evaluates the progress of the given username.
    Fetches the stats from S3 and calculates the difference between the
    last two entries.

    Example
    -------
    >>> evaluate_hiscore_progress(user_stats)
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
    }
    """
    username = stats["username"]
    current_stats = stats["stats"]
    current_date = datetime.strptime(current_stats["date"], DATETIME_FORMAT)

    # Get last entry
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

    # Calculate difference in total level
    total_level_difference = current_stats["total_level"] - prev_stats["total_level"]

    # Calculate the difference in combat level
    combat_level_difference = current_stats["combat_level"] - prev_stats["combat_level"]

    skills = []
    for skill_name, skill in current_stats["skills"].items():
        prev_skill = prev_stats["skills"][skill_name]
        skill_info = {
            "skill_name": skill_name,
            "level_difference": skill["level"] - prev_skill["level"],
            "experience_difference": skill["experience"] - prev_skill["experience"],
            "previous_level": prev_skill["level"],
            "previous_experience": prev_skill["experience"],
            "current_level": skill["level"],
            "current_experience": skill["experience"],
        }
        skills.append(SkillProgress(**skill_info))

    progress = {
        "username": username,
        "experience_difference": experience_difference,
        "total_level_difference": total_level_difference,
        "previous_total_level": prev_stats["total_level"],
        "current_total_level": current_stats["total_level"],
        "combat_level_difference": combat_level_difference,
        "previous_combat_level": prev_stats["combat_level"],
        "current_combat_level": current_stats["combat_level"],
        "time_difference": str(current_date - prev_date),
        "skills": skills,
    }

    return HiscoreProgress(**progress)
