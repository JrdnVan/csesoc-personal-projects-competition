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






def add_user_to_table (name, email , password, photo, pending, muted, blocked, friends, category):

    # Check if essential strings are empty 
    if type(name) == str and type(email) == str and type(password) == str:
        if name == "" or email =="" or password == "":
            print("User not added, Please check entries")
            raise ValueError

    # If entries arent empty generate UID
    user_id = event_id = uuid.uuid4().urn

    try:

        # Check if email exist
        get_resp_people = meet_ball_user.scan(
            FilterExpression=Attr("email").eq(email) 
        )

        if get_resp_people["Count"] != 0:
            raise ValueError 
        

        #attempt to add items
        meet_ball_user.put_item(
            Item = {
                "UID_User": user_id,
                "UID_Event/User": user_id,
                "full_name": name,
                "email" : email,
                "password": password,
                "photo": photo,
                "pending": pending,
                "muted" : muted,
                "blocked": blocked,
                "friends": friends,
                "category": category,
            },
            ConditionExpression = "attribute_not_exists(UID_User)",

        )
        print("User added to database!")

    except Exception as e:
        print(e)
        print("Could not add user to database")
 

add_user_to_table("neil", "neil1", "neil1","neil", ["1","2"], ["3"],[],[],{})