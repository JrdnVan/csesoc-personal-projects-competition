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



def accept_request(user_id, friend_id):
    try:
        if type(user_id) != str or type(friend_id) != str:
            print("User_id not correct format")
            return False
        
        # Get user_id
        get_user_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )

        # Get pending list 
        dict_resp = get_user_item["Item"]
        category_dict = dict_resp["category"]
        pending_list = category_dict["pending"]

        # Get friend_id
        get_friend_item = meet_ball_user.get_item(
            Key={
                "UID_User": friend_id,
                "UID_Event/User" : friend_id,
            }
        )
        dict_resp_friend = get_friend_item["Item"]
        category_dict_friend = dict_resp_friend["category"]
        sent_out_list = category_dict_friend["sent_out"]
        


        

        if friend_id in pending_list:
            print(pending_list)
            pending_list.remove(friend_id)
            #For the user

            #Update add the friend
            
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression ="SET category.#list_name = list_append( category.#list_name, :category_id), category.#pendingname = :list",
                ExpressionAttributeNames ={
                    "#list_name" : "friends", 
                    "#pendingname": "pending"
                },
                ExpressionAttributeValues ={
                     ":category_id" : [friend_id],
                     ":list": pending_list
                },
                ReturnValues = "UPDATED_NEW",
            )
            print(sent_out_list)
            sent_out_list.remove(user_id)
            # Update the friend for the user
            meet_ball_user.update_item(
                Key={"UID_User": friend_id,"UID_Event/User" : friend_id},          
                UpdateExpression ="SET category.#list_name = list_append( category.#list_name, :category_id), category.#pendingname = :list",
                ExpressionAttributeNames ={
                    "#list_name" : "friends", 
                    "#pendingname": "sent_out"
                },
                ExpressionAttributeValues ={
                     ":category_id" : [user_id],
                     ":list": sent_out_list
                },
                ReturnValues = "UPDATED_NEW",
            )
     
            
            return True

    except Exception as e:
        print(e)
        return False 

accept_request("urn:uuid:82ac1135-95a1-4503-b660-1e645351205f", "urn:uuid:35039454-4d10-4bb6-ab5d-0da3c9f5cfcb")