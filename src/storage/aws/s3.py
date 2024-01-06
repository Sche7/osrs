import os

from src.api.aws.s3 import S3
from src.storage.protocol import StorageProtocol


class S3Storage(StorageProtocol):
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        bucket_name: str,
        region_name: str = "eu-north-1",
        download_folder: str = "downloads",
    ):
        self.s3 = S3(aws_access_key_id, aws_secret_access_key, region_name)
        self.bucket_name = bucket_name
        self.download_folder = download_folder

        if not os.path.exists(self.download_folder):
            print(f"Creating {self.download_folder}...")
            os.makedirs(self.download_folder, exist_ok=True)

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
        """
        return self.s3.get_file_content(self.bucket_name, filepath)
