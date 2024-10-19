import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os

from configs.app_config import appConfig


class StorageUtil:
    def __init__(self):
        self.space_name = appConfig.STORAGE_SPACE_NAME
        self.region = appConfig.STORAGE_REGION

        self.s3_client = boto3.client(
            's3',
            region_name=self.region,
            endpoint_url=f'https://{self.region}.digitaloceanspaces.com',
            aws_access_key_id=appConfig.STORAGE_ACCESS_ID,
            aws_secret_access_key=appConfig.STORAGE_SECRET_KEY
        )

    def upload_file(self, file_path: str, object_name: str = None):
        try:
            if not object_name:
                object_name = os.path.basename(file_path)

            content_type = 'application/pdf' if file_path.endswith(
                '.pdf') else 'application/octet-stream'

            self.s3_client.upload_file(file_path, self.space_name, object_name, ExtraArgs={
                                       'ACL': 'public-read', 'ContentType': content_type})
            print(
                f"File '{file_path}' uploaded to Space '{self.space_name}' as '{object_name}'.")

        except FileNotFoundError:
            print("The file was not found.")
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            print(f"An error occurred: {e}")

    def get_cdn_file_url(self, object_name: str):
        return f"https://{self.space_name}.{self.region}.cdn.digitaloceanspaces.com/{object_name}"
