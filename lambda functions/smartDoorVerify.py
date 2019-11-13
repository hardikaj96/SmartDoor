import json
import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    print(event)
    otp = event['otp']
    valvisitor = check_otp(otp)
    visitor_info = None
    if valvisitor:
        visitor_info = retrieve_info(valvisitor['faceId'])
    if valvisitor:
        message = 'Welcome '
    else:    
        message = 'Permission Denied'
        
    if visitor_info:
        name = visitor_info['name']
        message += name + ' !!!! You have been authorized'
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }

    
def check_otp(otp):
    table = dynamodb.Table('passcodes')
    response = table.query(
        KeyConditionExpression=Key('tempAccessCode').eq(otp)
    )
    print(response)
    if response['Count']>0:
        return response['Items'][0]
    return None
        
def retrieve_info(faceId):
    table = dynamodb.Table('visitors')
    response = table.query(
        KeyConditionExpression=Key('faceId').eq(faceId)
    )
    if response['Count']>0:
        return response['Items'][0]
    return None