import pytest
from core.api.aws.s3 import S3


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
def test_list_objects(aws_credentials):
    # Get AWS credentials from environment variables
    aws_access_key_id, aws_secret_access_key = aws_credentials

    # Create an instance of S3
    s3 = S3(aws_access_key_id, aws_secret_access_key)

    # Call the list_objects method
    objects = s3.list_objects(bucket_name="osrsbucket")

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
def test_get_object(aws_credentials):
    # Get AWS credentials from environment variables
    aws_access_key_id, aws_secret_access_key = aws_credentials

    # Create an instance of S3
    s3 = S3(aws_access_key_id, aws_secret_access_key)
    # Call the get_object method
    obj = s3.get_object(bucket_name="osrsbucket", key="osrs_logo.PNG")

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
