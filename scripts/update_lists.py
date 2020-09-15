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





def update_list(user_id, pending, muted, blocked, friends, category_name, category):

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

        # Dictionary of attributes 
        dict_resp = get_resp_item["Item"]
        pend_list = dict_resp["pending"]
        muted_list = dict_resp["muted"]
        friend_list = dict_resp["friends"]
        block_list = dict_resp["blocked"]

        if check_duplicate(pend_list,pending) == True:
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression ="SET pending = list_append( if_not_exists(pending, :pend), :pend)",
                ExpressionAttributeValues ={ ":pend" : [pending]},
                ReturnValues = "UPDATED_NEW",
            )       
        
        if check_duplicate(friend_list, friends) == True:
                meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id,},          
                UpdateExpression ="SET friends = list_append( if_not_exists(friends, :friend), :friend)",
                ExpressionAttributeValues ={ ":friend" : [friends]},
                ReturnValues = "UPDATED_NEW",
            )    
        
        if check_duplicate(muted_list, muted) == True:
                meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id,},          
                UpdateExpression ="SET muted = list_append( if_not_exists(muted, :mute), :mute)",
                ExpressionAttributeValues ={ ":mute" : [muted]},
                ReturnValues = "UPDATED_NEW",
            )    

        if check_duplicate(block_list, blocked) == True:
                meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id,},          
                UpdateExpression ="SET blocked = list_append( if_not_exists(blocked, :block), :block)",
                ExpressionAttributeValues ={ ":block" : [blocked]},
                ReturnValues = "UPDATED_NEW",
            ) 


        try:
            category_list = dict_resp["category"][category_name] 
                if check_duplicate(category_list, category == True:
                    meet_ball_user.update_item(
                    Key={"UID_User": user_id,"UID_Event/User" : user_id,},          
                    UpdateExpression ="SET category = list_append( if_not_exists(category, :category), :category)",
                    ExpressionAttributeValues ={ ":category" : [category]},
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

update_list("urn:uuid:ec8be737-dddd-4251-ac05-85bde3d49737","5", "9", "10", "11", "7")





