import os

from typing import Iterator
from core.api.osrs.hiscores import Hiscores
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

        # Convert datetime to string
        # as the datetime object is not serializable
        character.update({"date": str(character["date"])})

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
