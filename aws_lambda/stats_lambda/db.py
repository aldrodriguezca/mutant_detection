import boto3
import json
import os

dynamo_resource = boto3.resource(service_name = 'dynamodb', region_name = 'us-east-1')
dna_table = dynamo_resource.Table(os.environ.get("DYNAMODB_TABLE"))

def query_mutant_status_count(is_mutant: bool) -> int:
    """ Perform the query in order to get the count of a specific human-type (Human or Mutant) sequences stored in DB.
 
    Args:
        is_mutant: bool
            Boolean indicating the type of human the query is going to count. (Human or mutant)

    Returns:
        Number with the counting result.

    """
    return dna_table.query(
        Select='COUNT',
        KeyConditions={
            'Key': {
                'AttributeValueList': [
                    "SEQUENCE"
                ],
                'ComparisonOperator': 'EQ'
            }
        },
        QueryFilter={
            'IsMutant': {
                'AttributeValueList': [
                    is_mutant,
                ],
                'ComparisonOperator': 'EQ'
            }
        }
    )


def get_stats() -> dict:
    """ Query the existing DNA-records in DB and computes basic stats.

    Returns:
        Dictionary holding the following structure:
        {
            "count_mutant_dna": int,
            "count_human_dna": int,
            "ratio": float
        }
    """
    mutant_response = query_mutant_status_count(True)
    human_response = query_mutant_status_count(False)

    ratio = mutant_response["Count"] / (human_response["Count"] + mutant_response["Count"])
    return {
        "count_mutant_dna": mutant_response["Count"],
        "count_human_dna": human_response["Count"],
        "ratio": ratio
    }
