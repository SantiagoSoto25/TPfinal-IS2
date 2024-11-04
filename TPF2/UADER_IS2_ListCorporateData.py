import boto3
import json
import logging
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

def list_corporate_data():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CorporateData')
    
    try:
        response = table.scan()
        data = response.get('Items', [])
        
        data = decimal_to_float(data)
        
        logging.info("Datos obtenidos de CorporateData:")
        logging.info(data)
        
        return json.dumps(data, indent=4)
    
    except Exception as e:
        logging.error("Error al obtener datos de CorporateData:", exc_info=True)
        return json.dumps({"error": str(e)}, indent=4)

if __name__ == "__main__":
    json_data = list_corporate_data()
    print(json_data)

