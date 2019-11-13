import json
import boto3
import base64
import logging
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from random import randint
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
s3 = boto3.client('s3')
rek = boto3.client('rekognition')

def lambda_handler(event, context):
    name = event['name']
    name = name.replace(" ", "")
    phoneNumber = event['phone']
    imageId = event['faceId']
    print('imageId: '+imageId)
    if imageId != "":
        response = rek.index_faces(
            CollectionId='col1',
            Image={
                'S3Object': {
                    'Bucket': 'ccassignment002',
                    'Name': imageId
                }
            },
            ExternalImageId=name,
            DetectionAttributes=[
                'DEFAULT',
            ],
            MaxFaces=1,
            QualityFilter='AUTO'
        )
        faceId = (((response['FaceRecords'])[0])['Face'])['FaceId']
        print(faceId)
        print(imageId)
        put_visitor(faceId, name, phoneNumber, imageId)
        otp = randint(100000, 999999)
        insert_passcode(faceId, otp)
        send_sms_to_visitor(phoneNumber, str(otp))
        
        return {
            'statusCode': 200,
            'body': json.dumps('OTP sent to Visitor!')
        }
    else:
        send_sms_to_visitor(phoneNumber, "")
        return {
            'statusCode': 200,
            'body': json.dumps('Visitor rejected!')
        }
    
def insert_passcode(faceId, otp):
    table = dynamodb.Table('passcodes')
    result = table.put_item(
        Item = {
                'tempAccessCode': str(otp),
                'faceId':faceId,
                'current_time':int(time.time()),
                'expiration_time':int(time.time() + 300)

        })
    return None
    
def send_sms_to_visitor(phoneNumber, otp):
    url = 'https://smartdoorverify.s3.amazonaws.com/index.html'
    if otp != "":
        message = 'Your Smart Door verification code is ' + otp + '  \n It will expire in 5 minutes.\n Enter the door by entering the otp in '+ url
    else:
        message = 'Sorry, but the owner has denied your entry to the door.' 
    sns.publish(
        PhoneNumber='+1'+str(phoneNumber),
        Message=message
    )
    return None
    
def put_visitor(faceId, name, phoneNumber, imageId):
    table = dynamodb.Table('visitors')
    result = table.put_item(
        Item = {
                'faceId': faceId,
                'name':name,
                'phoneNumber': phoneNumber,
                'photos': [
                    {
                        'objectKey': imageId,
                        'bucket': 'ccassignment002',
                        'createdTimestamp':time.strftime("%Y%m%d-%H%M%S")
                    }    
                ]

        })
    logger.info(name + ' with ' + faceId + ' inserted into table visitors')
    return result