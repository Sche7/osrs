import pytest
import os
from src.utils.randomize import random_string


@pytest.fixture(scope="session")
def aws_credentials():
    """Fixture that returns a tuple of AWS credentials."""
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    assert aws_access_key_id and aws_secret_access_key, "AWS credentials not found."
    return aws_access_key_id, aws_secret_access_key


@pytest.fixture(scope="session")
def bucket_name():
    """Fixture that returns the name of the bucket."""
    return "osrsbucket"


@pytest.fixture(scope="session")
def osrs_logo():
    """Fixture that returns the path to the OSRS logo."""
    return "tests/data/osrs_logo.png"


@pytest.fixture(scope="function")
def gibberish():
    """Fixture that returns a random string."""

    def _gibberish(length: int = 10) -> str:
        return random_string(length)

    return _gibberish
