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



def add_categories(user_id, category_name):

    # get original object
    get_resp_item = meet_ball_user.get_item(
        Key={
            "UID_User": user_id,
            "UID_Event/User" : user_id,
        }
    )
 
    item = get_resp_item["Item"]
    category_dict =  item["category"]

    
    if category_dict.get(category_name, -1) != -1:
        return True

    
    meet_ball_user.update_item(
        Key={"UID_User": user_id,"UID_Event/User" : user_id,},          
        UpdateExpression ="SET category.#list_name = :category_value", 
        ExpressionAttributeNames ={"#list_name" : category_name },
        ExpressionAttributeValues ={ ":category_value" : []},
        ReturnValues = "UPDATED_NEW",
    )

#comm
add_categories("urn:uuid:82ac1135-95a1-4503-b660-1e645351205f","bad")