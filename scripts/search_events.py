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


def search_event(user_id, category_name):
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
        category_dict = dict_resp["category"]
        
        if category_dict.get(category_name, -1) == -1:
            return False

        category_list = category_dict.get(category_name, -1)
    
        for person in category_list:
            get_person_event = meet_ball_user.scan(
                FilterExpression=Attr("UID_User").eq(person) 
            )
            for person_entity in get_person_event["Items"]:
                person_event = person_entity["UID_Event/User"] 

                if person_event != person:
                    possible_event.append(person_event)

        return possible_event

    except Exception as e:
        return e

print(search_event("urn:uuid:bac625b8-b6e1-4522-82e3-46c48e88bab3", "bad"))