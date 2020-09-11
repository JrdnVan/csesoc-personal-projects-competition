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
dynamodb = session.resource('dynamodb', region_name='us-east-2')
meet_ball_user = dynamodb.Table('meet_ball_user')
meet_ball_join = dynamodb.Table('meet_ball_join')


# pass in host, event and guess ID 

def add_event_to_table (guest_id,  host_id , event_id ):
  
    if type(guest_id) != str or type(event_id) != str:
        print("ID in wrong format")
        return False
    else:
        if guest_id == "" or event_id == "":
            print("Empty IDs")
            return False


    # create transaction Id
    transaction_id = uuid.uuid4().urn


    try:
        # Get event details 
        get_resp = meet_ball_user.get_item(
            Key={
            "UID_User": host_id,
            "UID_Event/User" : event_id,
            }
        )
            
        
        dict_resp = get_resp["Item"]
        limit = dict_resp["person_limit"]
        attending = dict_resp["no_guest_attending"]

        if int(attending) <= int(limit):
            # process event guest transaction
            print("ok")
            # put Item and update previous table 

            #put Item
            meet_ball_join.put_item(
                Item = {
                        "UID": transaction_id,
                        "Event": event_id,
                        "Person": host_id,
    
                },
                ConditionExpression = "attribute_not_exists(UID)",
            )

            # Need to add checks to see if it works
            print("middle")
            # Update number of people attending event 
            meet_ball_user.update_item(
                Key={
                    "UID_User": host_id,
                    "UID_Event/User" : event_id,
                },UpdateExpression = "SET no_guest_attending = :var",
                ExpressionAttributeValues ={
                    ":var" : attending + 1
                },
                ReturnValues = "UPDATED_NEW",
            )

            print("done")

    except Exception as e:
        print("Guest could not be added to event")
        return False
        
        
add_event_to_table("1", "123123123", "urn:uuid:8c7e501a-63dc-4a41-8e0d-2913959a1291")