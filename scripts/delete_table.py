import boto3

client = boto3.client('dynamodb', region_name='us-east-1')

try:
    resp = client.delete_table(
        TableName='meet_ball_user',
    )
    print("Table deleted successfully!")
except Exception as e:
    print("Error deleting table:")
    print(e)
