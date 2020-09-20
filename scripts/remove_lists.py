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


def remove_item(user_id, category_name, category_id):

    try:
        if type(user_id) != str:
            print("User_id not correct format")
            return False

        if type(category_id) != str or type(category_name) != str:
            print("Not correct format")

        if category_name == "self":
            return False

        # get original object
        get_resp_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )
        dict_resp = get_resp_item["Item"]
        category_dict = dict_resp["category"]
        
        if category_dict.get(category_name, -1) == -1:
            return True

        category_list = category_dict.get(category_name, -1)

 
        
        try:
            category_list.remove(category_id)
        except Exception as e:
            return "Category_id wasnt avaliable"


        meet_ball_user.update_item(
            Key={"UID_User": user_id,"UID_Event/User" : user_id},          
            UpdateExpression ="SET category.#list_name = :category_list",
            ExpressionAttributeNames ={"#list_name" : category_name },
            ExpressionAttributeValues ={ ":category_list" : category_list},
            ReturnValues = "UPDATED_NEW",
        )     

        return True 
        

    except Exception as e:
        print(e)
        return False 





#remove_item("urn:uuid:82ac1135-95a1-4503-b660-1e645351205f","friends", "urn:uuid:35039454-4d10-4bb6-ab5d-0da3c9f5cfcb")