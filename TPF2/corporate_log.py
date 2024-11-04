import boto3
from botocore.exceptions import ClientError
import uuid
import time

dynamodb = boto3.resource('dynamodb')

class CorporateLog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CorporateLog, cls).__new__(cls)
            cls._instance.table = dynamodb.Table('CorporateLog')
        return cls._instance

    def post(self, session_uuid, method_name):
        try:
            log_entry = {
                'uuid': session_uuid,
                'cpu_uuid': str(uuid.getnode()),
                'method': method_name,
                'timestamp': int(time.time())
            }
            self.table.put_item(Item=log_entry)
            return {"status": "log saved"}
        except ClientError as e:
            return {"error": str(e)}

    def list(self, cpu_uuid, session_uuid=None):
        try:
            if session_uuid:
                response = self.table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('cpu_uuid').eq(cpu_uuid))
            else:
                response = self.table.scan()
            return response.get('Items', [])
        except ClientError as e:
            return {"error": str(e)}

