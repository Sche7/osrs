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

    def save(self, data: str, filepath: str) -> None:
        """
        This uploads a file to the bucket.

        Parameters
        ----------
        data : str
            The data to upload.
        filepath : str
            The name of target file.
        """
        self.s3.upload_file(self.bucket_name, filepath, data)

    def load(self, filepath: str) -> str:
        """
        Load data from a bucket.

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
