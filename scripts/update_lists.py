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





def update_list(user_id, category_name, category_id):

    try:
        if type(user_id) != str:
            print("User_id not correct format")
            return False

        if type(category_id) != str or type(category_name) != str:
            print("Not correct format")
        
        # get original object
        get_resp_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )


        # Dictionary of attributes 
        dict_resp = get_resp_item["Item"]
        category_dict = dict_resp["category"]

        if category_dict.get(category_name, -1) == -1:
            return False

        category_list = category_dict.get(category_name, -1)


        if check_duplicate(category_list,category_id) == True:
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression ="SET category.#list_name = list_append( category.#list_name, :category_id)",
                ExpressionAttributeNames ={"#list_name" : category_name },
                ExpressionAttributeValues ={ ":category_id" : [category_id]},
                ReturnValues = "UPDATED_NEW",
            )       

        return True 
        
    except Exception as e:
        print(e)
        return False 



def check_duplicate(list, UID):
    if UID == None:
        return False
    
    for item in list:
        if item == UID:
            return False
    return True

update_list("urn:uuid:9e80d83f-c38a-44ca-885c-f00be4201443","friends", "4")





