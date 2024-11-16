import boto3
import json
import os
import hashlib

from typing import List
from dynamodb import save_sequence

# Resource instead of client to ease implementation.
s3 = boto3.resource('s3')

def verify_and_save_sequence(dna_object: dict):
    """Verify whether the input DNA-sequence corresponds to a human or mutant being. 
    Also stores the corresponding result in DB.

    Args:
        dna_object: Dict[str, Any]
        Dictionary containing DNA-data

    Returns:
        Boolean indicating whether the provided DNA sequence corresponds to mutant or human.
    """
    seq_hash = get_sequence_hash(dna_object)
    store_sequence(dna_object, seq_hash)
    is_mutant = check_mutant_dna(dna_object['dna'])
    save_sequence(dna_object, seq_hash, is_mutant)
    return is_mutant


def get_sequence_hash(dna_object: dict) -> str:
    """ Return a hash for the input DNA sequence

    Args:
        dna_object: Dict[str, Any]
            Dictionary containing input data for DNA sequence.

    Returns:
        String containing hashed contend for input DNA sequence
    """
    plain_sequence = ''.join(dna_object['dna'])
    h = hashlib.new('sha512', usedforsecurity=False)
    h.update(str.encode(plain_sequence))
    hashed_seq = h.hexdigest()

    return hashed_seq


def store_sequence(dna_object: dict, dna_hash: str):
    """ Store a .json file in an S3 bucket containing the received DNA data.

    Args:
        dna_object: dict
            Dictionary containing DNA-data to be processed.

        hash: str
            String containing the hash identiying the corresponding DNA-sequence.

    Returns:
        None
    """
    tmp_path = '/tmp/dnaData.json'
    with open(tmp_path, 'w') as f:
        json.dump(dna_object, f)

    storage_bucket = os.environ.get('STORAGE_BUCKET')
    bucket = s3.Bucket(storage_bucket)
    bucket.upload_file(tmp_path, f'{dna_hash}.json')


def check_mutant_dna(dna_matrix: List[str]) -> bool:
    """Verifiy the DNA-sequence data in order to see if the mutant-defining criteria is met

    Args:
        dna_matrix: List[str]
            List of strings containing DNA-strings

    Returns:
        Boolean value indicating whether the provided dna sequence (matrix) 
        corresponds to a mutant (True) or human (False).
    """
    repeated_seqs = 0
    seq_len_criteria = 4
    mutant_threshold = 1

    W = range(len(dna_matrix))
    H = range(len(dna_matrix[0]))
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    dir = 0
    repeated_seqs = 0
    
    while dir < len(directions) and repeated_seqs <= mutant_threshold:
        scan_path = []
        dx, dy = directions[dir]
        dir +=1
        
        if dx > 0:
            scan_path += [(0, y) for y in H]
            
        if dy > 0:   # scanning down
            scan_path += [(x, 0) for x in W]
            
        if dy < 0:   # scanning up
            scan_path += [(x, H[-1]) for x in W]
            
        for sx, sy in scan_path:
            seq = 0; mark = None
            x, y = sx, sy
            
            while x in W and y in H:
                if dna_matrix[x][y] == mark:
                    seq += 1
                else:
                    mark = dna_matrix[x][y]
                    seq = 1
                if mark is not None and seq >= seq_len_criteria:
                    repeated_seqs += 1

                if repeated_seqs > mutant_threshold:
                    return True
                x, y = x + dx, y + dy

    return repeated_seqs > mutant_threshold