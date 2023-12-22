import pytest
import os


@pytest.fixture(scope="session")
def aws_credentials():
    """Fixture that returns a tuple of AWS credentials."""
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    assert aws_access_key_id and aws_secret_access_key, "AWS credentials not found."
    return aws_access_key_id, aws_secret_access_key
