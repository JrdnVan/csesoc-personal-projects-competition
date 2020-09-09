import boto3
import datetime
import uuid

# Call user/event table from AWS

dynamodb = boto3.client ("dynamodb")


#Note: generate Randon ID
# add_event_to_table("neil", "1001", "location", "Desc", "phy", "5" , "6",  "7" )




# If creating new event attributes cant be empty
# if person_limit, time_limit and radius are empty enter default values




def add_event_to_table (name, host_id, location , description, photo , person_limit, time_limit, radius):
    
    if type(name) == str and type(location) and str and type(host_id) and str:
        if name == "" or location =="" or host_id == "":
            print("Event not added")
            return False
    
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
                            "time_stamp" : {"S" : datetime.datetime.now().isoformat()},
                            
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
        

