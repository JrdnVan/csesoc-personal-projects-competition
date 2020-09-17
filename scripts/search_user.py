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



def search_user(name, email):
    try:
        possible_user = []

        if type(name) != str or type(email) != str:
            raise TypeError 

        if name == "":
            name = []
        if email == "":
            email = []
    
        get_resp_event = meet_ball_user.scan(
            FilterExpression=Attr("full_name").contains(name) | Attr("email").contains(email) 

        )

        users = get_resp_event["Items"]

        for person in users:
            possible_user.append(person["UID_User"])



        return possible_user

    except Exception as e:
        return e

print(search_user("", ""))