import boto3
from boto3.dynamodb.conditions import Key
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
table = dynamodb.Table('meet_ball_user')


# Requires Host and Event_id 
def delete_event (host_id, event_id):
    
    # Verify fields are not empty 
    if type(host_id) == str and type(event_id):
        if host_id == "" or event_id =="" :
            print("One of the UID is empty")
            return False
    
    
    # Delete event from table 
    try:
        table.delete_item(
            Key = {
                "UID_User": host_id,
                "UID_Event/User" : event_id,
            }
        )
        print("Event is deleted!")
        return True 
        
    except Exception as e:
        print("Could not delete_event")
        return False
        
        
    
delete_event("123123123", "urn:uui:3108698e-e4dc-444f-b6d5-a47d61341d60")