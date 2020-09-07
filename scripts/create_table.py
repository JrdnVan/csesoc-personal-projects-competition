import boto3

dynamodb = boto3.client('dynamodb')

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