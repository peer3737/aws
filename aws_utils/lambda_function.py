import boto3
import json
from aws_utils import general


class Lambda:
    def __init__(self, region, aws_id):
        self.region = region
        self.aws_id = aws_id
        self.connection = boto3.client('lambda',  region_name=region)

    def get(self, arn):

        """
        :param arn:
        :return:
        """

        return general.handle_action(self.connection.get_function(
                FunctionName=arn
            ))

    def create(self, name, runtime, s3_bucket, s3_key, handler, role, timeout=180, publish=True, description=''):
        """

        :param name: Name of the Lambda function
        :param runtime: Name of the runtime of the Lambda function, e.g. python3.11
        :param s3_bucket: S3 bucket where default code is stored
        :param s3_key: S3 key of the zip file with default code
        :param handler: Path to the handler that starts the execution, e.g. src.main.lambda_handler
        :param role: Arn of the role attached to the function
        :param timeout: Timeout in seconds (optinal, default = 180)
        :param publish: Publish the function (optional, default = True)
        :param description: Description of the function (optional)
        :return:
        """

        return general.handle_action(self.connection.create_function(
            Code={
                'S3Bucket': s3_bucket,
                'S3Key': s3_key
            },
            Description=description,
            FunctionName=name,
            Handler=handler,
            Publish=publish,
            Role=role,
            Timeout=timeout,
            Runtime=runtime
        ))

    def execute(self, arn, payload=None, sync=False):
        if sync:
            event_type = 'RequestResponse'
        else:
            event_type = 'Event'

        # Invoke the Lambda function
        return general.handle_action(self.connection.invoke(
            FunctionName=arn,
            InvocationType=event_type,  # 'RequestResponse' (sync) or 'Event' (async)
            Payload=json.dumps(payload)
        ))

    def delete(self, arn):

        """
        :param arn:
        :return:
        """

        return general.handle_action(self.connection.delete_function(
                FunctionName=arn
            ))
