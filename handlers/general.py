import boto3
from botocore.exceptions import ClientError

def handle_action(action):
    return_response = {
        'status_code': '',
        'content': ''
    }
    try:
        response = action
        return_response['status_code'] = response['ResponseMetadata']['HTTPStatusCode']
        return_response['content'] = response
    except ClientError as e:
        return_response['status_code'] = 500
        return_response['content'] = e
    except Exception as e:
        return_response['status_code'] = 500
        return_response['content'] = e

    return return_response
