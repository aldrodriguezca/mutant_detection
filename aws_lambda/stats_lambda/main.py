import json
from db import get_stats

def handler(event, lambda_context):
    result = get_stats()
    
    return {
        "statusCode:" : 200,
        "body": json.dumps(result)
    }