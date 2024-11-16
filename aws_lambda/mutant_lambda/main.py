import json
from service import verify_and_save_sequence

def mutant_verification(event, context):
    json_body = json.loads(event['body']) # This unwrapping is necessary since the objects come from API Gateway.
    if ('dna' not in json_body.keys()):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Malformed input object"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    is_mutant = verify_and_save_sequence(json_body)
    if is_mutant:
        return {
            'statusCode': 200,
            'body': json.dumps('Mutant found!')
        }
    else:
        return {
            'statusCode': 403,
            'body': json.dumps('Mere Human found.')
        }
