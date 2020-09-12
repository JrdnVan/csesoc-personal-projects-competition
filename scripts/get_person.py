import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
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
meet_ball_join = dynamodb.Table('meet_ball_join_table')

# gets attributes of person

def get_person_item(user_id):
    get_resp_item = meet_ball_user.get_item(
        Key={
            "UID_User": user_id,
            "UID_Event/User" : user_id,
        }
    )
    # Dictionary of attributes    
    dict_resp = get_resp_item["Item"]
    return dict_resp



#Gets list of events person is attending

def get_person_event(user_id):

    list_of_event = []

    try:
        # Query database for the user_id
        get_resp_event = meet_ball_join.query(
            KeyConditionExpression=Key("guest").eq("1")
        )
    
        dict_resp = get_resp_event["Items"]
        
        # Add only event items into List
        for item in dict_resp:
            list_of_event.append(item["event"])

        
    # If fail return empty list
    except Exception as e:
        print(e)
        
    return list_of_event



