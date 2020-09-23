import boto3
from boto3.dynamodb.conditions import Key, Attr
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



# Requires Host and Event_id 
def delete_event (host_id, event_id):
    
    # Verify fields are not empty 
    if type(host_id) == str and type(event_id):
        if host_id == "" or event_id =="" :
            print("One of the UID is empty")
            return False
    
    # Delete event from table 
    try:
        meet_ball_user.delete_item(
            Key = {
                "UID_User": host_id,
                "UID_Event/User" : event_id,
            }
        )

    # Delete guess-event relationship
    get_resp_event = meet_ball_join.scan(
        FilterExpression=Attr("event").eq(event_id) 
    )
    event_dict =  get_resp_event["Items"]

    for item in event_dict:
        meet_ball_join.delete_item(
            Key = {
                "guest": item["guest"],
                "event" : item["event"],
            }
        )
    print("Event is deleted!")

        
    except Exception as e:
        print("Could not delete_event")
        return False
        
    
#comm