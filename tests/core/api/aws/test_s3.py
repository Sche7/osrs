import pytest
import os
from core.api.aws.s3 import S3
from botocore.exceptions import ClientError


@pytest.mark.aws
def test_list_buckets(aws_credentials):
    # Get AWS credentials from environment variables
    aws_access_key_id, aws_secret_access_key = aws_credentials

    # Create an instance of S3
    s3 = S3(aws_access_key_id, aws_secret_access_key)

    # Call the list_buckets method
    buckets = s3.list_buckets()

    # Assert that the returned value is a list
    assert isinstance(buckets, list)

    # Assert that each bucket is a dictionary
    for bucket in buckets:
        assert isinstance(bucket, dict)


@pytest.mark.aws
def test_list_objects(aws_credentials, bucket_name):
    # Get AWS credentials from environment variables
    aws_access_key_id, aws_secret_access_key = aws_credentials

    # Create an instance of S3
    s3 = S3(aws_access_key_id, aws_secret_access_key)

    # Call the list_objects method
    objects = s3.list_objects(bucket_name=bucket_name)

    # Assert that the returned value is a list
    assert isinstance(objects, list)

    # Assert that each object is a dictionary
    for obj in objects:
        assert isinstance(obj, dict)
        assert "Size" in obj
        assert "ETag" in obj
        assert "LastModified" in obj
        assert "StorageClass" in obj
        assert "Key" in obj


@pytest.mark.aws
def test_get_object(aws_credentials, bucket_name, osrs_logo):
    # Get AWS credentials from environment variables
    aws_access_key_id, aws_secret_access_key = aws_credentials

    # Create an instance of S3
    s3 = S3(aws_access_key_id, aws_secret_access_key)
    # Call the get_object method
    obj = s3.get_object(bucket_name=bucket_name, key="test/osrs_logo.PNG")

    # Assert that the returned value is a dictionary
    assert isinstance(obj, dict)

    # Assert that the dictionary contains the expected keys
    assert "Body" in obj
    assert "ContentLength" in obj
    assert "ContentType" in obj
    assert "ETag" in obj
    assert "LastModified" in obj
    assert "Metadata" in obj
    assert "ResponseMetadata" in obj
    assert "VersionId" in obj


@pytest.mark.aws
def test_upload_file(aws_credentials, osrs_logo, gibberish, bucket_name):
    # Get AWS credentials from environment variables
    aws_access_key_id, aws_secret_access_key = aws_credentials

    # Create an instance of S3
    s3 = S3(aws_access_key_id, aws_secret_access_key)

    key = f"test/osrs_logo_{gibberish()}.png"
    # Call the upload_file method
    s3.upload_file(
        bucket_name=bucket_name,
        key=key,
        filepath=osrs_logo,
    )

    # Assert that the file was uploaded
    objects = s3.list_objects(bucket_name=bucket_name, folder="test/")
    uploaded_object = [obj for obj in objects if key == obj["Key"]]
    assert len(uploaded_object) == 1
    assert uploaded_object[0]["Key"] == key

    # Delete the file
    response = s3.delete_object(bucket_name=bucket_name, key=key)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 204

    # See that file was deleted successfully
    with pytest.raises(ClientError, match="The specified key does not exist."):
        s3.get_object(bucket_name=bucket_name, key=key)


@pytest.mark.aws
def test_download_file(aws_credentials, osrs_logo, gibberish, bucket_name, tmp_path):
    # Get AWS credentials from environment variables
    aws_access_key_id, aws_secret_access_key = aws_credentials

    # Create an instance of S3
    s3 = S3(aws_access_key_id, aws_secret_access_key)

    key = f"test/osrs_logo_{gibberish()}.png"
    # Call the upload_file method
    s3.upload_file(
        bucket_name=bucket_name,
        key=key,
        filepath=osrs_logo,
    )

    # Call the download_file method
    local_filepath = f"{tmp_path}/logo.png"

    # Assert that the file does not exist yet
    assert not os.path.exists(local_filepath)

    s3.download_file(
        bucket_name=bucket_name,
        key=key,
        filepath=local_filepath,
    )

    # Assert that the file was downloaded
    assert os.path.exists(local_filepath)

    # Delete the file
    response = s3.delete_object(bucket_name=bucket_name, key=key)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 204

    # See that file was deleted successfully
    with pytest.raises(ClientError, match="The specified key does not exist."):
        s3.get_object(bucket_name=bucket_name, key=key)
