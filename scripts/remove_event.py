import boto3
from boto3.dynamodb.conditions import Key

# boto3 is the AWS SDK library for Python.
# The "resources" interface allows for a higher-level abstraction than the low-level client interface.
# For more details, go to http://boto3.readthedocs.io/en/latest/guide/resources.html
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('meet_ball_user')


#delete_event("1009", "1089")



# Requires Host and Event_id 
def delete_event (host_id, event_id):
    
    # Verify fields are not empty 
    if type(host_id) == str and type(event_id):
        if host_id == "" or event_id =="" :
            print("One of the UID is empty")
            return False
    
    
    # Delete event from table 
    try:
        table.delete_item(
            Key = {
                "UID_User": host_id,
                "UID_Event/User" : event_id,
            }
        )
        print("Event is deleted!")
        return True 
        
    except Exception as e:
        print("Could not delete_event")
        return False
        
        
    
    