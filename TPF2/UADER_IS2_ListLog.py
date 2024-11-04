import boto3
import json
import logging
import uuid
from decimal import Decimal

logging.basicConfig(level=logging.INFO)

def decimal_to_float(obj):
    if isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)  
    else:
        return obj

def list_log_by_cpu_uuid(cpu_uuid):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CorporateLog')
    
    try:
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('cpu_uuid').eq(cpu_uuid)
        )
        logs = response.get('Items', [])
        
        logs = decimal_to_float(logs)
        
        logging.info("Logs obtenidos de CorporateLog con uuidCPU:")
        logging.info(logs)
        
        return json.dumps(logs, indent=4)
    
    except Exception as e:
        logging.error("Error al obtener logs de CorporateLog:", exc_info=True)
        return json.dumps({"error": str(e)}, indent=4)

if __name__ == "__main__":
    cpu_uuid = str(uuid.getnode())
    json_data = list_log_by_cpu_uuid(cpu_uuid)
    print(json_data)
