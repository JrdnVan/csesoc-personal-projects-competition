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


# Note compulsory attributes name, host_id, location 
# Attributes without values will use default vaues


# If creating new event attributes can be empty
# if person_limit, time_limit and radius are empty enter default values

def add_event_to_table ( host_id,name,  place , description, photo ,time,  person_limit, time_limit, radius):
    
    if type(name) == str and type(place) == str and type(host_id) == str and type(time) == str:
        if name == "" or place =="" or host_id == "":
            print("Event not added")
            return False
    
    # use current time if no time is provided
    if time == "":
        time = datetime.datetime.now().isoformat()
   
 
   
   # set default values if no provided values
    if person_limit == "":
        person_limit = "10"



    if radius == "":
        radius = "100"
   
    if time_limit == "":
        time_limit = "30"
    
   
    # generate randon event ID
    event_id = uuid.uuid4().urn

    try:
        # Create transaction
        meet_ball_user.put_item(
            Item = {
                    "UID_User": host_id,
                    "UID_Event/User": event_id,
                    "full_name" : name,
                    "place": place,
                    "description" : description,
                    "photo": photo,
                    "person_limit" :  person_limit,
                    "time_limit": time_limit,
                    "radius": radius,
                    # Attain time event it made
                    "time_stamp" :  time,
                    "no_guest_attending" : 0,
            },
            ConditionExpression = "attribute_not_exists(UID_User)",
        )
        print("Event is now added")
        return True
    except Exception as e:
        print(e)
        print("Could not adds event to database")
        

add_event_to_table("urn:uuid:8a272d73-2bd3-497e-acfe-6e2fa3152c72","event","place","desc","photo", "time", "4", "5","9")