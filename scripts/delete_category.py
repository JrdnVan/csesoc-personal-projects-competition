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




def delete_category(user_id, category_name):
    try:
        if type(user_id) != str or type(category_name) != str:
            raise TypeError 

        if category_name == "friends" or category_name == "pending" or category_name == "blocked" or category_name == "muted" or category_name == "self":
            raise ValueError


        # get original object
        get_resp_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )

        item = get_resp_item["Item"]
        category_dict =  item["category"]

        #Remove category
        if category_dict.get(category_name, -1) != -1:
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id,},          
                UpdateExpression ="REMOVE category.#list_name", 
                ExpressionAttributeNames ={"#list_name" : category_name },
                ReturnValues = "UPDATED_NEW",
            )


    except Exception as e:
        print(e)
        return False

delete_category("urn:uuid:6080e716-6a17-40e3-9fee-33f336bbf7d7", "bad")