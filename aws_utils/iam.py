import boto3
import json
from botocore.exceptions import ClientError


class Role:
    def __init__(self, region, aws_id):

        """
        :param region: Preferred region, e.g. eu-central-1
        :param aws_id: AWS Account ID
        """

        self.region = region
        self.aws_id = aws_id
        self.iam = boto3.client('iam', region_name=region)

    def get(self, name):

        """
        :param name: Role name
        :return: if successfull - Returns status_code = 200 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """

        return_response = {
            'status_code': '',
            'content': ''
        }

        try:

            response = self.iam.get_role(
                RoleName=name
            )

            return_response['status_code'] = response['ResponseMetadata']['HTTPStatusCode']
            return_response['content'] = response
        except ClientError as e:
            return_response['status_code'] = 500
            return_response['content'] = e
        except Exception as e:
            return_response['status_code'] = 500
            return_response['content'] = e

        return return_response

    def create(self, name, services, description=''):

        """
        :param name: Role name, must be unique within each AWS Account, e.g. test-role-123
        :param services: array of assumed AWS services, e.g. ['lambda.amazonaws.com', 's3.amazonaws.com']
        :param description: Description of the role (optional)
        :return: if successfull - Returns status_code = 200 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """

        return_response = {
            'status_code': '',
            'content': ''
        }
        try:
            document = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": services
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            response = self.iam.create_role(
                RoleName=name,
                AssumeRolePolicyDocument=json.dumps(document),
                Description=description
            )

            return_response['status_code'] = response['ResponseMetadata']['HTTPStatusCode']
            return_response['content'] = response
        except ClientError as e:
            return_response['status_code'] = 500
            return_response['content'] = e
        except Exception as e:
            return_response['status_code'] = 500
            return_response['content'] = e

        return return_response

    def attach_policy(self, role_name, policy_arn):

        """
        :param role_name: Name of the role
        :param policy_arn: arn of the policy
        :return: if successfull - Returns status_code = 200 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """
        return_response = {
            'status_code': '',
            'content': ''
        }
        try:
            response = self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            return_response['status_code'] = response['ResponseMetadata']['HTTPStatusCode']
            return_response['content'] = response
        except ClientError as e:
            return_response['status_code'] = 500
            return_response['content'] = e
        except Exception as e:
            return_response['status_code'] = 500
            return_response['content'] = e

        return return_response

    def detach_policy(self, role_name, policy_arn):

        """
        :param role_name: Name of the role
        :param policy_arn: arn of the policy
        :return: if successfull - Returns status_code = 200 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """
        return_response = {
            'status_code': '',
            'content': ''
        }
        try:
            response = self.iam.detach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            return_response['status_code'] = response['ResponseMetadata']['HTTPStatusCode']
            return_response['content'] = response
        except ClientError as e:
            return_response['status_code'] = 500
            return_response['content'] = e
        except Exception as e:
            return_response['status_code'] = 500
            return_response['content'] = e

        return return_response

    def delete(self, name):

        """
        :param name: Name of the role to be deleted
        :return: if successfull - Returns status_code = 200 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """

        return_response = {
            'status_code': '',
            'content': ''
        }

        try:

            response = self.iam.delete_role(
                RoleName=name
            )

            return_response['status_code'] = response['ResponseMetadata']['HTTPStatusCode']
            return_response['content'] = response
        except ClientError as e:
            return_response['status_code'] = 500
            return_response['content'] = e
        except Exception as e:
            return_response['status_code'] = 500
            return_response['content'] = e

        return return_response


class Policy:
    def __init__(self, region, aws_id):
        self.region = region
        self.aws_id = aws_id
        self.iam = boto3.client('iam', region_name=region)

    def get(self, arn):

        """
        :param arn: Policy Arn
        :return: if successfull - Returns status_code = 200 with content = response information
                 Otherwise - status_code = 500 with content = Error information
        """

        return_response = {
            'status_code': '',
            'content': ''
        }

        try:

            response = self.iam.get_policy(
                PolicyArn=arn
            )

            return_response['status_code'] = response['ResponseMetadata']['HTTPStatusCode']
            return_response['content'] = response
        except ClientError as e:
            return_response['status_code'] = 500
            return_response['content'] = e
        except Exception as e:
            return_response['status_code'] = 500
            return_response['content'] = e

        return return_response

    def create(self, name, permissions, description=''):

        """
        :param name: Policy name, must be unique within each AWS Account, e.g. test-role-123
        :param permissions: array of permission (or restriction) objects, e.g.
        [
            {
                "Effect": "Allow",
                "Action": ["lambda:*",  "logs:CreateLogGroup"],
                "Resource": ["arn:aws:logs:eu-central-1:123456789000:*", "arn:aws:lambda:eu-central-1:123456789000:function:my_function"]
            },
            {
                "Effect": "Allow",
                "Action": ["s3:*"],
                "Resource": "*"
            }
        ]
        :param description: Description of the policy (optional)
        :return: if successfull - Returns status_code = 200 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """

        return_response = {
            'status_code': '',
            'content': ''
        }

        try:
            document = {
                "Version": "2012-10-17",
                "Statement": permissions
            }
            response = self.iam.create_policy(
                PolicyName=name,
                Description=description,
                PolicyDocument=json.dumps(document)
            )

            return_response['status_code'] = response['ResponseMetadata']['HTTPStatusCode']
            return_response['content'] = response
        except ClientError as e:
            return_response['status_code'] = 500
            return_response['content'] = e
        except Exception as e:
            return_response['status_code'] = 500
            return_response['content'] = e

        return return_response

    def delete(self, arn):

        """
        :param arn: Arn of the policy to be deleted
        :return: if successfull - Returns status_code = 200 with content = response information.
                 Otherwise - status_code = 500 with content = Error information
        """

        return_response = {
            'status_code': '',
            'content': ''
        }

        try:

            response = self.iam.delete_policy(
                PolicyArn=arn
            )

            return_response['status_code'] = response['ResponseMetadata']['HTTPStatusCode']
            return_response['content'] = response
        except ClientError as e:
            return_response['status_code'] = 500
            return_response['content'] = e
        except Exception as e:
            return_response['status_code'] = 500
            return_response['content'] = e

        return return_response
