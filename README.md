# mutant_detection

Application to help [Magneto](https://x-men.fandom.com/es/wiki/Magneto) in the recruiting process of mutants to fight the [X-Men](https://x-men.fandom.com/es/wiki/Wiki_X-Men).

The implementation has 2 approaches:

## AWS-Lambda based implementation.

![AWS_lambda_architecture](./meli_test_aws_lambda.drawio.svg)

The implemented Lambda function reside behind an API Gateway, which allows the corresponding endpoints to be consumed from the following URLs:

### POST endpoint (/mutant)
```
https://ystms3071e.execute-api.us-east-2.amazonaws.com/dev/v1/mutant

Body request example:
{
  "dna": [
    "ATGCGA",
    "CAGTGC",
    "TTATGT",
    "AGATGG",
    "CCCCTA",
    "TCACTG"
  ]
}

Response examples:
Mutant case:
{
  "statusCode": 200,
  "body": "Mutant found."
}

Human case:
{
  "statusCode": 200,
  "body": "Mere Human found."
}

```

### GET endpoint (/stats)
```
https://ystms3071e.execute-api.us-east-2.amazonaws.com/dev/v1/stats

Response example:
{
  "statusCode": 200,
  "body": {
    "count_mutant_dna": 1,
      "count_human_dna": 1,
      "ratio": 0.5
  }
}
```

## FastAPI Implementation.

![AWS_lambda_architecture](./fast_api_meli_test.drawio.svg)

In order to execute the project locally:

Assuming you can setup your own Atlas cluster with the correspondinng Mongo DB, Set the configuration file ```config.ini``` in the root directory of the project. Such configuration file should have the following structure:

```
[MongoDB]
cluster_name = *db-cluster*
DB-user = *db-username*
DB-pass = *db-password*
DNA-Database = *db-name*
Collection = *db-collection-name*
```

```
python -m uvicorn main:app
```

The application is deployed in AWS infrastructure and the corresponding endpoints can be accessed via the following URLs:

### POST endpoint (/mutant)
```
http://54.226.126.225:8000/mutant

# Body request example:
{
  "dna": [
    "ATGCGA",
    "CAGTGC",
    "TTATGT",
    "AGATGG",
    "CCCCTA",
    "TCACTG"
  ]
}

Response examples:
Mutant case:
{
  "statusCode": 200,
  "body": "Mutant found."
}

Human case:
{
  "statusCode": 200,
  "body": "Mere Human found."
}

```

### GET endpoint (/stats)
```
http://54.226.126.225:8000/stats

Response example:
{
  "statusCode": 200,
  "body": {
    "count_mutant_dna": 1,
      "count_human_dna": 1,
      "ratio": 0.5
  }
}
```