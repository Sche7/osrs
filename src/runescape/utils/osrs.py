import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from runescape.dataclasses.character import DATETIME_FORMAT, Character
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


def evaluate_hiscore_progress(previous: Character, current: Character) -> HiscoreProgress:
    """
    Evaluates the progress of the given username.
    Fetches the stats from S3 and calculates the difference between the
    last two entries.
    """
    # See that the username is the same
    assert previous.username == current.username, "Usernames do not match."
    username = previous.username
    current_date = datetime.strptime(current.date, DATETIME_FORMAT)
    prev_date = datetime.strptime(previous.date, DATETIME_FORMAT)
    experience_difference = current.total_experience - previous.total_experience
    total_level_difference = current.total_level - previous.total_level
    combat_level_difference = current.combat_level - previous.combat_level
    diff_skills = current.skills - previous.skills

    skills = []
    for skill_name, diff_skill in diff_skills.__dict__.items():
        prev_skill = previous.skills.__dict__[skill_name]
        curr_skill = current.skills.__dict__[skill_name]
        skill_info = {
            "skill_name": skill_name,
            "level_difference": diff_skill["level"],
            "experience_difference": diff_skill["experience"],
            "previous_level": prev_skill["level"],
            "previous_experience": prev_skill["experience"],
            "current_level": curr_skill["level"],
            "current_experience": curr_skill["experience"],
        }
        skills.append(SkillProgress(**skill_info))

    progress = {
        "username": username,
        "experience_difference": experience_difference,
        "total_level_difference": total_level_difference,
        "previous_total_level": previous.total_level,
        "current_total_level": current.total_level,
        "combat_level_difference": combat_level_difference,
        "previous_combat_level": previous.combat_level,
        "current_combat_level": current.combat_level,
        "time_difference": str(current_date - prev_date),
        "skills": skills,
    }

    return HiscoreProgress(**progress)
