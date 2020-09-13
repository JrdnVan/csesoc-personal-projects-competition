import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import uuid
import boto3
import datetime
import uuid
from decouple import Config, RepositoryEnv

DOTENV_PATH = ".env"
env = Config(RepositoryEnv(DOTENV_PATH))

# Call user/event table from AWS
session = boto3.Session(
    aws_access_key_id=env.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=env.get('AWS_SECRET_ACCESS_KEY'),
)
s3 = session.client('s3')
dynamodb = session.resource('dynamodb', region_name='ap-southeast-2')

try:
    # Call dynamo API, open session
    dynamodb.create_table(
        TableName='meet_ball_user',

        AttributeDefinitions=[
            {
                "AttributeName": "User_ID",
                "AttributeType": "S"
            },
            {
                "AttributeName": "Event_ID",
                "AttributeType": "S"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "User_ID",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "Event_ID",
                "KeyType": "RANGE"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1 
        }
    )
    print("Table created successfully.")

    # If unsucessful
except Exception as e:
    print("Could not create table. Error:")
    print(e)