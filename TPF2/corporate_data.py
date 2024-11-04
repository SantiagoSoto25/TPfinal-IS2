import boto3
from botocore.exceptions import ClientError
import uuid


dynamodb = boto3.resource('dynamodb')

class CorporateData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CorporateData, cls).__new__(cls)
            cls._instance.table = dynamodb.Table('CorporateData')
        return cls._instance

    def getData(self, session_uuid, cpu_uuid, sede_id):
        try:
            response = self.table.get_item(Key={'identificador': sede_id})
            if 'Item' in response:
                return response['Item']
            else:
                return {"error": "No data found"}
        except ClientError as e:
            return {"error": str(e)}

    def getCUIT(self, session_uuid, cpu_uuid, sede_id):
        data = self.getData(session_uuid, cpu_uuid, sede_id)
        return {"CUIT": data.get("CUIT", "No CUIT found")} if "error" not in data else data

    def getSeqID(self, session_uuid, cpu_uuid, identificador):
        try:
            response = self.table.get_item(Key={'identificador': identificador})
            if 'Item' in response:
                seq_id = response['Item']['idSeq'] + 1
                self.table.update_item(
                    Key={'identificador': identificador},
                    UpdateExpression='SET idSeq = :val',
                    ExpressionAttributeValues={':val': seq_id}
                )
                return {"idSeq": seq_id}
            else:
                return {"error": "Sequence ID not found"}
        except ClientError as e:
            return {"error": str(e)}


    def listCorporateData(self):
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except ClientError as e:
            return {"error": str(e)}
