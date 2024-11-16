import os
import json
import boto3

dynamo_resource = boto3.resource(service_name = 'dynamodb', region_name = 'us-east-1')
dna_table = dynamo_resource.Table(os.environ.get("DYNAMODB_TABLE"))

def save_sequence(dna: str, hash_id: str, is_mutant: bool):
    """ Store DNA-sequence-related data into a DynamoDB table.

    Args:
        dna: dict
            String with the filename containing DNA-sequence data path (stored in S3).

        hash_id: str
            String representing the hash identifying the corresponding DNA-sequence.

        is_mutant
    """
    dna_table.put_item(
        Item={
            'Key': 'SEQUENCE',
            'Sort': str(hash_id),
            'Sequence': dna,
            'IsMutant': is_mutant
        }
    )