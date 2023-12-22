import os
import pytest
from core.utils.osrs import link_hiscores_to_s3, S3Storage


@pytest.mark.aws
def test_link_hiscores_to_s3(
    aws_credentials, bucket_name, gibberish, osrs_logo, tmp_path
):
    aws_access_key_id, aws_secret_access_key = aws_credentials

    usernames = ["NotCrostyGIM", "NotPlucksGIM", "Zehahandsome", "Zolixo1"]

    # Call the function
    link_hiscores_to_s3(
        usernames,
        bucket_name,
        aws_access_key_id,
        aws_secret_access_key,
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
