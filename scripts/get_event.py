import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
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



def get_event_item(event_id):
    event_dict = {}

    #query using event_id
    try:
        if type(event_id) != str:
            raise TypeError 

        get_resp_event = meet_ball_user.scan(
            FilterExpression=Attr("UID_Event/User").eq(event_id) 
        )
        
        event_dict =  get_resp_event["Items"]
        
        #event_dict = get_resp_event
    except Exception as e:
        print(e)
        print("can not query event")
        
    # return dictionary of event if found
    return event_dict    


#print(get_event_item("urn:uuid:7c3db440-671f-46d5-977e-d45c8bc66a1b")[0])

def get_event_person_attending(event_id):
    person_list = []

    #query using event_id
    try:
        get_resp_people = meet_ball_join.scan(
            FilterExpression=Attr("event").eq(event_id) 
        )
       
        for item in get_resp_people["Items"]:
            person_list.append(item["guest"])

    except Exception as e:
        print(e)
        print("can not query event")
    
    # return dictionary of event if found
    return person_list


#coo
#get_event_item("urn:uuid:51661c2a-eb07-4b2a-9a0d-86c1eff0fbfc")
