import pytest
import os

from core.storage.aws.s3 import S3Storage


@pytest.mark.aws
def test_save_and_load(aws_credentials, osrs_logo, gibberish, bucket_name, tmp_path):
    # Get AWS credentials from environment variables
    aws_access_key_id, aws_secret_access_key = aws_credentials

    # Create an instance of S3Storage
    storage = S3Storage(
        aws_access_key_id,
        aws_secret_access_key,
        bucket_name,
        download_folder=tmp_path,
    )

    remote_filepath = f"test/osrs_logo_{gibberish()}.png"

    try:
        # Call the save method
        storage.save(osrs_logo, remote_filepath)

        # Call the load method
        downloaded_filepath = storage.load(remote_filepath)

        # Assert that the file was downloaded
        assert os.path.exists(downloaded_filepath)
    finally:
        # Delete the file
        storage.s3.delete_object(bucket_name, remote_filepath)
