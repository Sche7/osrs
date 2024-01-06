import pytest

from src.storage.aws.s3 import S3Storage


@pytest.mark.aws
def test_save_and_load(aws_credentials, gibberish, bucket_name, tmp_path):
    # Get AWS credentials from environment variables
    aws_access_key_id, aws_secret_access_key = aws_credentials

    # Create an instance of S3Storage
    storage = S3Storage(
        aws_access_key_id,
        aws_secret_access_key,
        bucket_name,
        download_folder=tmp_path,
    )

    content = b'{"test": "test"}'
    remote_filepath = f"test/test_s3_storage_{gibberish()}.json"

    try:
        # Call the save method
        storage.save(content, remote_filepath)

        # Call the load method
        loaded_content = storage.load(remote_filepath)

        # Assert that the content is not empty
        assert content == loaded_content

    finally:
        # Delete the file
        storage.s3.delete_object(bucket_name, remote_filepath)
