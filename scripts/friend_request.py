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

def friend_request(user_id, friend_id):

    try:
        if type(user_id) != str or type(friend_id) != str:
            print("User_id not correct format")
            return False


        # Check if user_id is in DB 
        get_user_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )
        
        if get_user_item["Item"] == []:
            raise ValueError 


        # CHeck friend is in DB
        get_friend_item = meet_ball_user.get_item(
            Key={
                "UID_User": friend_id,
                "UID_Event/User" : friend_id,
            }
        )
        
        dict_resp = get_friend_item["Item"]
        category_dict = dict_resp["category"]

        # Get list of the friend
        curr_friend_list = category_dict["friends"]
        curr_pending_list = category_dict["pending"]
        curr_block_list = category_dict["blocked"]

        # Check user isnt in friend list 
        if user_id in curr_friend_list or user_id in curr_pending_list or user_id in curr_block_list:
            return False

        else:
            # Add to the pending list
            meet_ball_user.update_item(
                Key={"UID_User": friend_id,"UID_Event/User" : friend_id},          
                UpdateExpression ="SET category.#list_name = list_append( category.#list_name, :category_id)",
                ExpressionAttributeNames ={"#list_name" : "pending" },
                ExpressionAttributeValues ={ ":category_id" : [user_id]},
                ReturnValues = "UPDATED_NEW",
            ) 
            # Update sent out
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression ="SET category.#list_name = list_append( category.#list_name, :category_id)",
                ExpressionAttributeNames ={"#list_name" : "sent_out" },
                ExpressionAttributeValues ={ ":category_id" : [friend_id]},
                ReturnValues = "UPDATED_NEW",
            ) 

            return True 


    except Exception as e:
        print(e)
        return False 

        

print(friend_request("urn:uuid:35039454-4d10-4bb6-ab5d-0da3c9f5cfcb", "urn:uuid:82ac1135-95a1-4503-b660-1e645351205f"))