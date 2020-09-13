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
dynamodb = session.resource('dynamodb', region_name='ap-southeast-2')
meet_ball_user = dynamodb.Table('meet_ball_user')


# If name, email, password are empty replace with old entires

def edit_user(user_id, name, email , password, pending, muted, blocked, friends, category):

    try:
        if type(user_id) != str:
            print("User_id not correct format")
            return False

        if type(name) != str or type(email) != str or type(password) != str:
            print("Not correct format")
            return False

        if type(pending) != list or type(muted) != list or type(blocked) != list or type(friends) != list or type(category) != dict:
            print("Not correct format")
            return False

        # Get original user entry
        get_resp = meet_ball_user.get_item(
            Key={
            "UID_User": user_id,
            "UID_Event/User" : user_id,
            }
        )
    
        dict_resp = get_resp["Item"]

        # Check if entries are empty
        if name == "":
            name = dict_resp["name"]
        if email == "":
            email = dict_resp["email"]
        if password == "":
            password = dict_resp["password"]
    

        # Update entries
        meet_ball_user.update_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            },

            # Update expressions
            UpdateExpression = "SET full_name = :name , email = :email , password = :password ",
            ExpressionAttributeValues ={
                ":name" : name,
                ":email": email,
                ":password": password,
            },
            ReturnValues = "UPDATED_NEW",
        )

        print("Event Successfully Editted")


    except Exception as e:
        print(e)
        print("Can not edit user")
#edit_user("urn:uuid:d27825a3-f93b-4090-853a-6c39cc6ca460", "str", "str","str", ["str", "str"], ["str", "str"], ["str", "str"],["str", "str"], {"str":"str"})

def update_user_photo(user_id, photo):
    try:
        if type(user_id) != str or type(photo) != str:
            print("User_id not correct format")
            return False

        meet_ball_user.update_item(
            Key={
                "UID_User": user_id,
                "UID_Event/User" : user_id,
            },

            # Update expressions
            UpdateExpression = "SET photo = :photo ",
            ExpressionAttributeValues ={
                ":photo" : photo,
            },
            ReturnValues = "UPDATED_NEW",
        )

        print("Updated Photo")

    except Exception as e:
        print(e)
        print("Can not update photo")
        return False


