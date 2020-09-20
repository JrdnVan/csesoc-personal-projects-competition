import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime as datetime1
from decouple import Config, RepositoryEnv
from datetime import datetime
from get_user import get_user_event



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


def search_event(user_id, category_name):
    try:
        
        possible_event = []
        
        if type(user_id) != str:
            raise TypeError 
        
        get_resp_item = meet_ball_user.get_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            }
        )

        dict_resp = get_resp_item["Item"]
        category_dict = dict_resp["category"]
        block_list = category_dict["blocked"]
        mute_list = category_dict["muted"]
        
        # Get list to remove user from list 
        
        set1 = set(mute_list)
        set2 = set(block_list)
        difference = list(set2 - set1)
        no_show = difference + mute_list
        
        
        if category_dict.get(category_name, -1) == -1:
            return False

        category_list = category_dict.get(category_name, -1)
    
        for person in category_list:
           
            get_person_event = meet_ball_user.scan(
                FilterExpression=Attr("UID_User").eq(person) 
            )
         
            for person_entity in get_person_event["Items"]:

                # check not in block or mute list 
                person_event = person_entity["UID_Event/User"] 
                person_id = person_entity["UID_User"]
        
                if person_id in no_show:
                    print("no show")
                else:
                    try:
                        if datetime.strptime(person_entity["time_limit"], "%c") >  datetime1.datetime.now():
                            possible_event.append(person_event)
                        
                    except Exception as e:
                        print(e)
                
        
        # remove events user is attending
        for item in get_user_event(user_id):
            try:
                possible_event.remove(item["UID_Event/User"])
            except Exception as e:
                print("")
  

        return possible_event

    except Exception as e:
        return e

print(search_event("urn:uuid:82ac1135-95a1-4503-b660-1e645351205f", "friends"))