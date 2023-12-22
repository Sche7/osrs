import os

from typing import Iterator
from core.api.osrs.hiscores import Hiscores
from core.storage.aws.s3 import S3Storage
from core.storage.json import JSONStorage
from dataclasses import asdict
from botocore.exceptions import ClientError


def get_hiscores(usernames: list[str]) -> Iterator[Hiscores]:
    for username in usernames:
        try:
            yield Hiscores(username)
        except Exception as e:
            print(str(e))
            continue


def link_hiscores_to_s3(
    usernames: list[str],
    bucket_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
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

        character_history = None
        result = None
        # Download the file if it exists
        try:
            download_path = aws_storage.load(f"hiscores/{username}.json")
            character_history = json_storage.load(download_path)
        except ClientError:
            pass

        if character_history is None:
            result = {
                "username": username,
                "history": [character],
            }
        else:
            character_history["history"].append(character)
            result = character_history

        upload_path = f"{tmp_dir}/{username}.json"
        json_storage.save(result, upload_path)
        aws_storage.save(upload_path, f"hiscores/{hiscore.character.username}.json")
