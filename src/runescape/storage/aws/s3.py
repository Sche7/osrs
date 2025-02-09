from runescape.api.aws.s3 import S3
from runescape.storage.protocol import StorageProtocol


DEFAULT_REGION_NAME = "eu-north-1"


class S3Storage(StorageProtocol):
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        bucket_name: str,
        region_name: str = DEFAULT_REGION_NAME,
    ):
        self.s3 = S3(aws_access_key_id, aws_secret_access_key, region_name)
        self.bucket_name = bucket_name

    def save(self, content: str, filepath: str) -> None:
        """
        Upload content to an s3 bucket.
        The content is saved as a file where the fileformat
        is inferred from the filepath.

        Parameters
        ----------
        content : str
            The data to upload to the bucket.
        filepath : str
            The name of target file.

        Example
        -------
        >>> aws_storage = S3Storage(
        ...     aws_access_key_id,
        ...     aws_secret_access_key,
        ...     bucket_name,
        ... )
        >>> aws_storage.save("Hello, World!", "test.txt")
        """
        self.s3.upload_file_content(self.bucket_name, filepath, content)

    def load(self, filepath: str) -> str:
        """
        Get the contents of a file in an s3 bucket without downloading it.

        Parameters
        ----------
        filepath : str
            The name of the file to load.

        Returns
        -------
        str
            The contents of the file.

        Example
        -------
        >>> aws_storage = S3Storage(
        ...     aws_access_key_id,
        ...     aws_secret_access_key,
        ...     bucket_name,
        ... )
        >>> aws_storage.load("test.txt")
        """
        return self.s3.get_file_content(self.bucket_name, filepath)
