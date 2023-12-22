import boto3


class S3:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str = "eu-north-1",
    ):
        self.s3 = boto3.client(
            service_name="s3",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def list_buckets(self) -> list[dict]:
        """
        List all s3 buckets.

        Returns
        -------
        list
            A list of bucket names.
        """
        return self.s3.list_buckets()["Buckets"]

    def list_objects(self, bucket_name: str, folder: str = "") -> list[dict]:
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
        return self.s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=folder,
        )["Contents"]

    def get_object(self, bucket_name: str, key: str) -> dict:
        """
        Get an object from a bucket.

        Parameters
        ----------
        bucket_name : str
            The name of the bucket.
        key : str
            The name of the object.

        Returns
        -------
        dict
            The object.
        """
        return self.s3.get_object(Bucket=bucket_name, Key=key)
