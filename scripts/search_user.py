import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
from decouple import Config, RepositoryEnv
from get_user import get_user_item

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



def search_user(user_id, name, email):
    try:

        # Extract possible users 
        possible_user = []
        if type(name) != str or type(email) != str:
            raise TypeError 

        if name == "":
            name = []
        if email == "":
            email = []
    
        # Get user from db 
        get_resp_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )
        # Dictionary of attributes    
        dict_resp = get_resp_item["Item"]
        category_dict = dict_resp["category"]
        blocked = category_dict["blocked"]


        #scan table 
        get_resp_event = meet_ball_user.scan(
            FilterExpression=Attr("full_name").contains(name) | Attr("email").eq(email) 

        )

        users = get_resp_event["Items"]

        for person in users:
            if person["UID_User"] in blocked:
                print("")
            else:
                possible_user.append(get_user_item(person["UID_User"]))



        return possible_user


        #Make use of block or muted 

#com

    except Exception as e:
        return e

print(search_user("urn:uuid:35039454-4d10-4bb6-ab5d-0da3c9f5cfcb", "neil", ""))