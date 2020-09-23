import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import uuid
import boto3
import datetime
import uuid
from decouple import Config, RepositoryEnv
from remove_event_guest import remove_event_from_table

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
        

        # CHeck if category id is real   
                # get original object
        get_guest_item = meet_ball_user.get_item(
            Key={
                "UID_User": category_id,
                "UID_Event/User" : category_id,
            }
        )
        
        print(get_guest_item)
        if get_guest_item["Item"] == []:
            raise ValueError 


        # get original object
        # Check if user exists
        get_resp_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )


        # Dictionary of attributes 
        dict_resp = get_resp_item["Item"]
        category_dict = dict_resp["category"]
        friends_list = category_dict["friends"]

        if category_name == "blocked":

            try:
                # Update friends list
                friends_list.remove(category_id)
                meet_ball_user.update_item(
                    Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                    UpdateExpression ="SET category.#list_name = :category_list",
                    ExpressionAttributeNames ={"#list_name" : "friends" },
                    ExpressionAttributeValues ={ ":category_list" : friends_list},
                    ReturnValues = "UPDATED_NEW",
                )     

               # remove from events
                get_resp_event_delete_guest = meet_ball_user.scan(
                    FilterExpression=Attr("host_id").eq(category_id) & Attr("guest").eq(user_id) 
                )

                event_delete_guest = get_resp_event_delete_guest["Items"]

                for item in event_delete_guest:
                    remove_event_from_table(user_id, item["host_id"], item["event"])

                #remove as host
                get_resp_event_delete_host = meet_ball_user.scan(
                    FilterExpression=Attr("guest").eq(user_id) & Attr("host_id").eq(user_id) 
                )

                event_delete_host = get_resp_event_delete_host["Items"]

                for item in event_delete_host:
                    remove_event_from_table( item["host_id"],user_id, item["event"])

            


            except Exception as e:
                print("Block wasnt in friends")

            # Add to block list
            meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression ="SET category.#list_name = list_append( category.#list_name, :category_id)",
                ExpressionAttributeNames ={"#list_name" : category_name },
                ExpressionAttributeValues ={ ":category_id" : [category_id]},
                ReturnValues = "UPDATED_NEW",
            )  

        elif category_name != "pending" or category_name != "self":
            if category_dict.get(category_name, -1) == -1:
                return False

            # Adding friends to custom 
            if category_id in category_dict["friends"]:
                category_list = category_dict.get(category_name)
                # Place in category if it exists
                if check_duplicate(category_list,category_id) == True:
                    meet_ball_user.update_item(
                        Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                        UpdateExpression ="SET category.#list_name = list_append( category.#list_name, :category_id)",
                        ExpressionAttributeNames ={"#list_name" : category_name },
                        ExpressionAttributeValues ={ ":category_id" : [category_id]},
                        ReturnValues = "UPDATED_NEW",
                    )  
                    return True
        
        return False
        
    except Exception as e:
        print(e)
        return False 


        """

        # Add a user to pending list 
        # check if in friends list 
        if category_name == "pending":
            category_list = category_dict.get(category_name)

            if check_duplicate(category_list,category_id) == True:
                meet_ball_user.update_item(
                Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                UpdateExpression ="SET category.#list_name = list_append( category.#list_name, :category_id)",
                ExpressionAttributeNames ={"#list_name" : category_name },
                ExpressionAttributeValues ={ ":category_id" : [category_id]},
                ReturnValues = "UPDATED_NEW",
                )

        # check category
        # CHeck if in friends
        elif: 
            if category_dict.get(category_name, -1) == -1:
                return False

            if category_id in category_dict("friends"):
                category_list = category_dict.get(category_name):

                    # Place in category if it exists
                    if check_duplicate(category_list,category_id) == True:
                        meet_ball_user.update_item(
                            Key={"UID_User": user_id,"UID_Event/User" : user_id},          
                            UpdateExpression ="SET category.#list_name = list_append( category.#list_name, :category_id)",
                            ExpressionAttributeNames ={"#list_name" : category_name },
                            ExpressionAttributeValues ={ ":category_id" : [category_id]},
                            ReturnValues = "UPDATED_NEW",
                        )  
                        return True

            return False
        """




# Return True if no duplicate
# Return False if there are duplicate and show not procede 

def check_duplicate(list, UID):
    if UID == None:
        return False
    
    for item in list:
        if item == UID:
            return False
    return True

#update_list("urn:uuid:6080e716-6a17-40e3-9fee-33f336bbf7d7","bad", "4")


