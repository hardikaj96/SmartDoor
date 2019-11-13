import json
import boto3
import base64
import logging
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from random import randint
import time
import cv2

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
s3 = boto3.client('s3')
rek = boto3.client('rekognition')
kenvid = boto3.client('kinesisvideo')
kenvidmed = boto3.client('kinesis-video-media',endpoint_url='https://s-1e415f8b.kinesisvideo.us-east-1.amazonaws.com',region_name='us-east-1')

def lambda_handler(event, context):
    record = event['Records'][0]
    print(record)
    payload=base64.b64decode(record["kinesis"]["data"])
    #print('Decoded payload:', payload)
    faceinfo = json.loads(payload.decode('utf-8'))
    faces = faceinfo["FaceSearchResponse"]
    faceId = ''
    #name = ''
    check_frame = False
    final_key='kvs1_'
    for f in faces:
        for matchedFace in f["MatchedFaces"]:
            mf = matchedFace["Face"]
            faceId = mf["FaceId"]
            print(faceId)
            #name = mf["ExternalImageId"]
        # if len(f["MatchedFaces"]) == 0:
        if 'InputInformation' in faceinfo:
            x = faceinfo["InputInformation"]
            y = x["KinesisVideo"]
            fn = y["FragmentNumber"]
            print(x,y,fn)
            stream = kenvidmed.get_media(
                StreamARN='arn:aws:kinesisvideo:us-east-1:397577651207:stream/kvs1/1572735942118',
                StartSelector={
                    'StartSelectorType': 'FRAGMENT_NUMBER',
                    'AfterFragmentNumber': fn
                }
            )
            print('stream ')
            with open('/tmp/stream.mkv', 'wb') as f:
                streamBody = stream['Payload'].read(1024*16384)
                f.write(streamBody)
                vcap = cv2.VideoCapture('/tmp/stream.mkv')
            # while(True):
                # Capture frame-by-frame
                ret, frame = vcap.read()
                if frame is not None:
                    # Display the resulting frame
                    vcap.set(1, int(vcap.get(cv2.CAP_PROP_FRAME_COUNT)/2)-1)
                    final_key=final_key+time.strftime("%Y%m%d-%H%M%S")+'.jpg'
                    cv2.imwrite('/tmp/'+final_key,frame)
                    s3.upload_file('/tmp/'+final_key, 'ccassignment002', final_key)
                    print('final_key in s3 upload')
                    vcap.release()
                    print('Image uploaded :', final_key)
                    check_frame = True
                    break
                else:
                    print("Frame is None")
                    break
        break
    print('faceId', faceId)

    if check_frame or faceId:
        print('Frame processed!')
        if faceId != '':
            visitor = check_visitor(faceId)
            print(visitor)
            if visitor:
                otp = randint(100000, 999999)
                update_visitor(visitor, faceId, final_key)
                insert_passcode(faceId, otp)
                send_sms_to_visitor(phoneNumber, str(otp))
                print('sms sent to visitor',str(phoneNumber))
        else:
            print('sending sms to owner')
            send_sms_to_owner(final_key)
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully Completed')
    }
                
def check_visitor(faceId):
    table = dynamodb.Table('visitors')
    response = table.query(
        KeyConditionExpression=Key('faceId').eq(faceId)
    )
    print(response)
    if response['Count']>0:
        return response['Items'][0]
    return None
        
def send_sms_to_owner(final_key):
    owner_phone = '+15512288614'
    url = 'https://ccassignment002.s3.amazonaws.com/index.html?q='+final_key
    message = 'Please give access or deny the request for the visitor by visiting '+ url 
    sns.publish(
        PhoneNumber=owner_phone,
        Message=message
    )
    print('sms sent to owner', str(owner_phone))
    return
    
def insert_passcode(faceId, otp):
    table = dynamodb.Table('passcodes')
    print(int(time.time()))
    print(int(int(time.time())+300))
    result = table.put_item(
        Item = {
                'tempAccessCode': str(otp),
                'faceId':faceId,
                'current_time':int(time.time()),
                'expiration_time':int(time.time() + 10)

        })
    return None
    
def send_sms_to_visitor(phoneNumber, otp):
    message = 'Your Smart Door verification code is ' + otp + '  \n It will expire in 5 minutes.'
    sns.publish(
        PhoneNumber=phoneNumber,
        Message=message
    )
    return None

def update_visitor(visitor, faceId, photo):
    table = dynamodb.Table('visitors')
    visitor_photos = visitor['photos']
    photos = {
                'objectKey': photo,
                'bucket': 'ccassignment002',
                'createdTimestamp':time.strftime("%Y%m%d-%H%M%S")
            }
    visitor_photos.append(photos)
    table.delete_item(
        Key={
            'faceId' : faceId
        }
    )
    result = table.put_item(
        Item = {
                'faceId': faceId,
                'name':visitor['name'],
                'phoneNumber': visitor['phoneNumber'],
                'photos': visitor_photos

        })
    return None