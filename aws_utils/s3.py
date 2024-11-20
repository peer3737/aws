import boto3
from botocore.exceptions import ClientError
from handlers import general


class S3:
    def __init__(self, region, aws_id):
        self.region = region
        self.aws_id = aws_id
        self.s3 = boto3.client('s3')

    def get(self, bucket_name, key_name):

        """
        :param bucket_name: Name of S3 bucket
        :param key_name: Path to S3 folder or file
        :return: if successfull - Returns status_code = 200 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """

        return general.handle_action(self.s3.get_object(Bucket=bucket_name, Key=key_name))


    def create(self, bucket_name, key_name, file_path, metadata=None):

        """

        :param bucket_name: Name of the S3 bucket
        :param key_name: Name of the S3 filepath within the S3 bucket
        :param file_path: File path of the file to be uploaded, e.g. c:\temp\file.txt
        :param metadata: Metadata of the file. This is a json object e.g.
                {
                    "creation_date": "2024-10-11 09:30:30,
                    "description": "Just a file"
                }
        :return: if successfull - Returns status_code = 201 with content = information of the created key.
                 Otherwise - status_code = 500 with content = Error information

        """
        return_response = {
            'status_code': '',
            'content': ''
        }
        try:
            self.s3.upload_file(
                Filename=file_path,
                Bucket=bucket_name,
                Key=key_name,
                ExtraArgs={"Metadata": metadata}
            )
            return_response['status_code'] = 201
            return_response['content'] = self.get(bucket_name=bucket_name, key_name=key_name)['content']

        except ClientError as e:
            return_response['status_code'] = 500
            return_response['content'] = e
        except Exception as e:
            return_response['status_code'] = 500
            return_response['content'] = e

        return return_response

    def list(self, bucket_name):
        """

        :param bucket_name: S3 Bucket name get listed
        :return: if successfull - Returns status_code = 200 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """

        return general.handle_action(self.s3.list_objects_v2(Bucket=bucket_name))

    def key_exists(self, bucket_name, key_name):
        try:
            self.s3.head_object(Bucket=bucket_name, Key=key_name)
            return True
        except ClientError:
            return False

    def delete(self, bucket_name, key_name):

        """
        :param bucket_name: S3 Bucket where a key has to be deleted
        :param key_name: Key to be deleted
        :return: if successfull - Returns status_code = 204 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """

        return general.handle_action(self.s3.delete_object(Bucket=bucket_name, Key=key_name))
