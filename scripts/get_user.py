import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from decouple import Config, RepositoryEnv
import datetime as datetime1

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

# gets attributes of person

def get_user_item(user_id):
    try:
        if type(user_id) != str:
            raise TypeError 
    
        get_resp_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )
        # Dictionary of attributes    


        dict_resp = get_resp_item["Item"]
        category_dict = dict_resp["category"]
        friend_list = category_dict["friends"]
        block_list = category_dict["blocked"]

        dict_resp["category"]["friends"] = list( set(friend_list) - set(block_list))
        dict_resp.pop("password")
        dict_resp.pop("email")
        

        return dict_resp
    except Exception as e:
        return e



#Gets list of events person is attending
# append dictionary

def get_user_event(user_id):

    list_of_event = []

    try:
        if type(user_id) != str:
            raise TypeError 
        # Query database for the user_id
        get_resp_event = meet_ball_join.query(
            KeyConditionExpression=Key("guest").eq(user_id)
        )
    
        dict_resp = get_resp_event["Items"]
        
        # Add only event items into List
        # Could get events here
        for item in dict_resp:

            #query for time
            get_event_data = meet_ball_user.get_item(
                Key={
                    "UID_User": item["host_id"],
                    "UID_Event/User" : item["event"],
                }
            )
            

            event_dict_resp = get_event_data["Item"]

            try:
                if datetime.strptime(event_dict_resp["time_limit"], "%c") >  datetime1.datetime.now():
                    list_of_event.append(event_dict_resp)
            except Exception as e:
                print(e)
      
                

    # If fail return empty list
    except Exception as e:
        print(e)
        
    return list_of_event

#com
#sprint(get_user_event("urn:uuid:6080e716-6a17-40e3-9fee-33f336bbf7d7"))
