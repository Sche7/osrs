import os
import pytest
from src.utils.osrs import save_hiscores_in_s3, S3Storage, evaluate_hiscore_progress


@pytest.mark.aws
def test_save_hiscores_to_s3(aws_credentials, bucket_name, tmp_path):
    aws_access_key_id, aws_secret_access_key = aws_credentials

    usernames = ["NotCrostyGIM", "NotPlucksGIM", "Zehahandsome"]

    # Call the function
    save_hiscores_in_s3(
        usernames,
        bucket_name,
        aws_access_key_id,
        aws_secret_access_key,
        remote_folder="test",
    )

    # Check that the files were uploaded
    storage = S3Storage(
        aws_access_key_id,
        aws_secret_access_key,
        bucket_name,
        download_folder=tmp_path,
    )

    for username in usernames:
        remote_filepath = f"hiscores/{username}.json"
        downloaded_filepath = storage.load(remote_filepath)
        assert os.path.exists(downloaded_filepath)


def test_evaluate_hiscore_progress():
    result = evaluate_hiscore_progress("Zehahandsome", "tests/data/")

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