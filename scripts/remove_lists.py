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


def remove_item(user_id, pending, muted, blocked, friends, category):

    try:
        if type(user_id) != str:
            print("User_id not correct format")
            return False

        if type(pending) != str or type(muted) != str or type(blocked) != str or type(friends) != str:
            print("Not correct format")

        # get original object
        get_resp_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )
        dict_resp = get_resp_item["Item"]
        pend_list = dict_resp["pending"]
        muted_list = dict_resp["muted"]
        friend_list = dict_resp["friends"]
        block_list = dict_resp["blocked"]

        friend_index = search_list(friend_list,friends) 
        if friend_index != -1:
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression = "SET friends =:friend",
                ExpressionAttributeValues ={ ":friend" : friend_index},
                ReturnValues = "UPDATED_NEW",
            )    

        pend_index = search_list(pend_list, pending)
        if pend_index != -1:
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression = "SET pending =:pend",
                ExpressionAttributeValues ={ ":pend" : pend_index},
                ReturnValues = "UPDATED_NEW",
            )    

        block_index = search_list(block_list, blocked)
        if block_index != -1:
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression = "SET blocked =:block",
                ExpressionAttributeValues ={ ":block" : block_index},
                ReturnValues = "UPDATED_NEW",
            )     

        mute_index = search_list(muted_list, muted)
        if mute_index != -1:
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression = "SET muted =:mute",
                ExpressionAttributeValues ={ ":mute" : mute_index},
                ReturnValues = "UPDATED_NEW",
            )          

        return True 


    except Exception as e:
        print(e)
        return False 


def search_list(list,UID):
    if UID == None:
        return -1

    for item in list:
        if item == UID:
            list.remove(item)
            return list
        
    return -1


remove_item("urn:uuid:ec8be737-dddd-4251-ac05-85bde3d49737","5", "9", "10", "11", "7")