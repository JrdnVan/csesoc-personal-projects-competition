import boto3
import datetime
import uuid

# Call user/event table from AWS

dynamodb = boto3.client ("dynamodb")


# Note compulsory attributes name, host_id, location 
# Attributes without values will use default vaues


# add_event_to_table("neil", "1001", "location", "Desc", "phy", "5" , "6",  "7" )


# If creating new event attributes can be empty
# if person_limit, time_limit and radius are empty enter default values






def add_event_to_table (name, host_id, location , description, photo ,time,  person_limit, time_limit, radius):
    
    if type(name) == str and type(location) == str and type(host_id) == str and type(time) == str:
        if name == "" or location =="" or host_id == "":
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
    
    print(time_limit)
    # generate randon event ID
    event_id = uuid.uuid4().urn
   
    try:
        # Create transaction
        resp = dynamodb.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": "meet_ball_user",
                        "Item": {

                            "UID_User": {"S": host_id},
                            "UID_Event/User": {"S": event_id},
                            "Name" : {"S": name},
                            "location": {"S": location},
                            "description" : {"S": description},
                            "photo": {"S": photo},
                            "person_limit" : {"N" : person_limit},
                            "time_limit": {"N": time_limit},
                            "radius": {"N": radius},
                            # Attain time event it made
                            "time_stamp" : {"S" : time},

                        },
                        "ConditionExpression": "attribute_not_exists(UID_User)",
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD",
                    }
                }
            ]
        )
        print("Event is now added")
        return True
    except Exception as e:
        print("Could not add event to database")
        

