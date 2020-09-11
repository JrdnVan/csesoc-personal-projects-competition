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


def edit_event(host_id, event_id, place ,description, photo, person_limit, time_limit, radius):
    try:
        print(meet_ball_user.scan())
        meet_ball_user.update_item(
            Key={
                "UID_User": host_id,
                "UID_Event/User" : event_id,
            },

            # Update expressions
            UpdateExpression = "SET place = :place , description = :descp , photo = :photo , person_limit = :no_people , time_limit = :time_limit , radius = :radius",
            ExpressionAttributeValues ={
                ":place" : place,
                ":descp": description,
                ":photo": photo,
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


#edit_event("1", "urn:uuid:51661c2a-eb07-4b2a-9a0d-86c1eff0fbfc", "check", "check" , "check" , "check", "check", "check")