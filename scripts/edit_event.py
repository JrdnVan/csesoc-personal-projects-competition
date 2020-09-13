import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import uuid
import boto3
import datetime
import uuid
from decouple import Config, RepositoryEnv


#Note: When calling function provide all values, empty values = empty entries

DOTENV_PATH = ".env"
env = Config(RepositoryEnv(DOTENV_PATH))

# Call user/event table from AWS
session = boto3.Session(
    aws_access_key_id=env.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=env.get('AWS_SECRET_ACCESS_KEY'),
)
s3 = session.client('s3')
dynamodb = session.resource('dynamodb', region_name='us-east-2')
meet_ball_user = dynamodb.Table('meet_ball_user')



# If place, description, person_limit, time_limit, radius are empty it would be replaced by old entries 

def edit_event(host_id, event_id, place ,description, person_limit, time_limit, radius):
    try:
        if type(host_id) != str or type(event_id) != str:
            print("Incorrect format")
            return False

        # Get original item
        get_resp = meet_ball_user.get_item(
            Key={
            "UID_User": host_id,
            "UID_Event/User" : event_id,
            }
        )
        dict_resp = get_resp["Item"]

        # Check for empty entries
        if place == "":
            place = dict_resp["place"]
        if description == "":
            description = dict_resp["description"]
        if person_limit == "":
            person_limit = dict_resp["person_limit"]
        if time_limit == "":
            time_limit = dict_resp["time_limit"]
        if radius == "":
            radius = dict_resp["radius"]


        meet_ball_user.update_item(
            Key={
                "UID_User": host_id,
                "UID_Event/User" : event_id,
            },

            # Update expressions
            UpdateExpression = "SET place = :place , description = :descp , person_limit = :no_people , time_limit = :time_limit , radius = :radius",
            ExpressionAttributeValues ={
                ":place" : place,
                ":descp": description,
                ":no_people": person_limit,
                ":time_limit" : time_limit,
                ":radius": radius,
            },
            ReturnValues = "UPDATED_NEW",
        )

        print("Event Successfully Editted")

    except Exception as e:
        print("Could not edit Event")
        return False


def edit_event_photo(host_id, event_id, photo):
    try:
        if type(host_id) != str or type(event_id) != str or type(photo) != str:
            print("Incorrect Format")
            return False

        meet_ball_user.update_item(
            Key={
                "UID_User": host_id,
                "UID_Event/User" : event_id,
            },UpdateExpression = "SET photo = :photo",
            ExpressionAttributeValues ={
                ":photo" : photo,
            },
            ReturnValues = "UPDATED_NEW",
        )
        print("Photo Updated")

    except Exception as e:
        print(e)
        return False

edit_event_photo("1", "	urn:uuid:51661c2a-eb07-4b2a-9a0d-86c1eff0fbfc", "pho")