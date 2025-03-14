from typing import Any

import boto3


class S3:
    """A wrapper for boto3's s3 client."""

    SERVICE_NAME = "s3"

    def __init__(
        self,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        region_name: str = "eu-north-1",
    ):
        self.s3_client = boto3.client(
            service_name=self.SERVICE_NAME,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def list_buckets(self) -> list[dict[str, Any]]:
        """
        List all s3 buckets.

        Returns
        -------
        list
            A list of bucket names.
        """
        return self.s3_client.list_buckets()["Buckets"]

    def list_objects(self, bucket_name: str, folder: str = "") -> list[dict[str, Any]]:
        """
        List all objects in a bucket.

        Parameters
        ----------
        bucket_name : str
            The name of the bucket.
        folder : str, optional
            The name of the folder.
            By default, "".

        Returns
        -------
        list[dict]
            A list of objects in the bucket.
        """
        return self.s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=folder,
        )["Contents"]

    def get_object(self, bucket_name: str, key: str) -> dict[str, Any]:
        """
        Get an object from a bucket.

        Parameters
        ----------
        bucket_name : str
            The name of the bucket.
        key : str
            The name of the object.
            This also works for objects in folders, simply add the folder name
            before the object name, e.g. "test/object.txt".

        Returns
        -------
        dict
            The object.
        """
        return self.s3_client.get_object(Bucket=bucket_name, Key=key)

    def upload_file(self, bucket_name: str, key: str, filepath: str) -> None:
        """
        Upload a file to a bucket.

        Parameters
        ----------
        bucket_name : str
            The name of the bucket.
        key : str
            The name of the object.
            This also works for objects in folders, simply add the folder name
            before the object name, e.g. "test/object.txt".
        filepath : str
            The path to the file to upload.
        """
        return self.s3_client.upload_file(
            Filename=filepath,
            Bucket=bucket_name,
            Key=key,
        )

    def upload_file_content(
        self,
        bucket_name: str,
        key: str,
        content: str | bytes,
    ) -> None:
        """
        Upload a file to a bucket without having to create a file locally.

        Parameters
        ----------
        bucket_name : str
            The name of the bucket.
        key : str
            The name of the object.
            This also works for objects in folders, simply add the folder name
            before the object name, e.g. "test/object.txt".
        content : str
            The content to upload.
        """
        return self.s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=content,
        )

    def download_file(self, bucket_name: str, key: str, filepath: str) -> None:
        """
        Download a file from a bucket.

        Parameters
        ----------
        bucket_name : str
            The name of the bucket.
        key : str
            The name of the object.
            This also works for objects in folders, simply add the folder name
            before the object name, e.g. "test/object.txt".
        filepath : str
            The local target path for the downloaded file.
        """
        return self.s3_client.download_file(
            Filename=filepath,
            Bucket=bucket_name,
            Key=key,
        )

    def get_file_content(self, bucket_name: str, key: str) -> str:
        """
        Get the content of a file in a bucket without downloading it.

        Parameters
        ----------
        bucket_name : str
            The name of the bucket.
        key : str
            The name of the object.
            This also works for objects in folders, simply add the folder name
            before the object name, e.g. "test/object.txt".

        Returns
        -------
        str
            The content of the file.
        """
        data = self.get_object(bucket_name=bucket_name, key=key)
        content = data["Body"].read()
        return content

    def delete_object(self, bucket_name: str, key: str):
        """
        Delete an object from a bucket.

        Parameters
        ----------
        bucket_name : str
            The name of the bucket.
        key : str
            The name of the object.
            This also works for objects in folders, simply add the folder name
            before the object name, e.g. "test/object.txt".
        """
        return self.s3_client.delete_object(Bucket=bucket_name, Key=key)
