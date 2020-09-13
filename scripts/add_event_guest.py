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
meet_ball_user = dynamodb.Table('meet_ball_user')
meet_ball_join = dynamodb.Table('meet_ball_join_table')


# pass in host, event and guess ID 
# have to check guest,hos,event are valid IDS

def add_event_to_table (guest_id,  host_id , event_id ):
  
    if type(guest_id) != str or type(event_id) != str:
        print("ID in wrong format")
        return False
    else:
        if guest_id == "" or event_id == "":
            print("Empty IDs")
            return False

    try:

        # Check if guest exists in database
        guest_resp = meet_ball_user.get_item(
            Key={
            "UID_User": guest_id,
            "UID_Event/User" : guest_id,
            }
        )
        if guest_resp["Item"] == NULL: print("Guest doesnt exist \n") 
        

        # Note Error would occur if guest (partition) and event(sort) arent unique preventing guest accepting multiple times 
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
  
            #put Item and update previous table 
            #put Item
            meet_ball_join.put_item(
                Item = {
                    "guest": guest_id,
                    "event": event_id,
                },
                ConditionExpression = "attribute_not_exists(guest_id)",
            )

            # Need to add checks to see if it works
           
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
            print("Relationship added")

    except Exception as e:
        print("Guest could not be added to event")
        return False
        
        
add_event_to_table("7", "urn:uuid:8a272d73-2bd3-497e-acfe-6e2fa3152c72", "urn:uuid:e97c1509-c12f-436f-9cae-e6d264cce329")