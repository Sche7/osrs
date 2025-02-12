import json
from typing import Literal

import pytest
from botocore.exceptions import ClientError

from src.runescape.storage.json import JSONStorage
from src.runescape.utils.osrs import (
    S3Storage,
    evaluate_hiscore_progress,
    save_hiscores_in_s3,
)


@pytest.mark.aws
def test_save_hiscores_to_s3(
    aws_credentials: tuple[str, str],
    bucket_name: Literal["osrsbucket"],
):
    aws_access_key_id, aws_secret_access_key = aws_credentials

    usernames = ["NotCrostyGIM", "NotPlucksGIM"]
    remote_folder = "test"

    # Check that the files were uploaded
    storage = S3Storage(
        bucket_name=bucket_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    for stats in save_hiscores_in_s3(
        usernames,
        bucket_name,
        aws_access_key_id,
        aws_secret_access_key,
        remote_folder=remote_folder,
    ):
        username = stats["username"]
        remote_filepath = f"{remote_folder}/{username}.json"

        # Assert that the file was uploaded
        content = storage.load(remote_filepath)

        # Assert that the content is a string
        assert isinstance(content, bytes)

        # Assert that the content is not empty
        assert content

        # Assert that file is json compatible
        assert isinstance(json.loads(content), dict)

        # Delete the file
        response = storage.s3.delete_object(bucket_name=bucket_name, key=remote_filepath)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 204

        # See that file was deleted successfully
        with pytest.raises(ClientError, match="The specified key does not exist."):
            storage.s3.get_object(bucket_name=bucket_name, key=remote_filepath)


def test_evaluate_hiscore_progress():
    json_storage = JSONStorage()
    stats = json_storage.load("tests/data/Zehahandsome.json")
    result = evaluate_hiscore_progress(stats)

    for key in [
        "username",
        "experience_difference",
        "combat_level_difference",
        "time_difference",
        "skills",
    ]:
        assert key in result

    assert result["username"] == "Zehahandsome"
    assert result["experience_difference"] == 4635
    assert result["combat_level_difference"] == 0
    assert result["time_difference"] == "0:27:30"
    assert len(result["skills"]) == 23
