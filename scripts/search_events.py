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
dynamodb = session.resource('dynamodb', region_name='ap-southeast-2')
meet_ball_user = dynamodb.Table('meet_ball_user')
meet_ball_join = dynamodb.Table('meet_ball_join_table')




def search_event(user_id):
    try:

        possible_event = []

        if type(user_id) != str:
            raise TypeError 
    
        get_resp_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )

        dict_resp = get_resp_item["Item"]

        # Get friends list
        friend_list = dict_resp["friends"]
    
        for friend in friend_list:
            get_friend_event = meet_ball_user.scan(
                FilterExpression=Attr("UID_User").eq(friend) 
            )
    
            friend_dict = get_friend_event["Items"][0]
            friend_event = friend_dict["UID_Event/User"] 

            if friend_event != friend:
                possible_event.append(friend_event)

        return possible_event

    except Exception as e:
        return e

search_event("urn:uuid:ec8be737-dddd-4251-ac05-85bde3d49737")