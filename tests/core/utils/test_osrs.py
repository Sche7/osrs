import os
import pytest
from core.utils.osrs import save_hiscores_in_s3, S3Storage, evaluate_hiscore_progress


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
    result = evaluate_hiscore_progress("Zehahandsome", "downloads")
    assert result is not None
