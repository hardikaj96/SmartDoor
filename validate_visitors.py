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
    #record = {'kinesis': {'kinesisSchemaVersion': '1.0', 'partitionKey': 'ab1ca4a2-e42c-4206-80be-ee9251b9bd52', 'sequenceNumber': '49601089386756595653249534880211890627568915973756944386', 'data': 'eyJJbnB1dEluZm9ybWF0aW9uIjp7IktpbmVzaXNWaWRlbyI6eyJTdHJlYW1Bcm4iOiJhcm46YXdzOmtpbmVzaXN2aWRlbzp1cy1lYXN0LTE6Mzk3NTc3NjUxMjA3OnN0cmVhbS9rdnMxLzE1NzI3MzU5NDIxMTgiLCJGcmFnbWVudE51bWJlciI6IjkxMzQzODUyMzMzMTgxNDcyMDExNzE1MDc5OTEzNDc2NzM2Njg1NTk4OTE3NjYxIiwiU2VydmVyVGltZXN0YW1wIjoxLjU3MzAzMDY4NDA5RTksIlByb2R1Y2VyVGltZXN0YW1wIjoxLjU3MzAzMDY4MjMzM0U5LCJGcmFtZU9mZnNldEluU2Vjb25kcyI6MC40OTU5OTk5OTE4OTM3NjgzfX0sIlN0cmVhbVByb2Nlc3NvckluZm9ybWF0aW9uIjp7IlN0YXR1cyI6IlJVTk5JTkcifSwiRmFjZVNlYXJjaFJlc3BvbnNlIjpbeyJEZXRlY3RlZEZhY2UiOnsiQm91bmRpbmdCb3giOnsiSGVpZ2h0IjowLjMyMjY0NjQsIldpZHRoIjowLjE4NjExODI3LCJMZWZ0IjowLjQ2OTE2NDUyLCJUb3AiOjAuNDY2NzMwMjR9LCJDb25maWRlbmNlIjoxMDAuMCwiTGFuZG1hcmtzIjpbeyJYIjowLjUxMjk5OTUsIlkiOjAuNTg1NDExMiwiVHlwZSI6ImV5ZUxlZnQifSx7IlgiOjAuNTk4MDAyNTUsIlkiOjAuNTgxOTY3LCJUeXBlIjoiZXllUmlnaHQifSx7IlgiOjAuNTIzMTMyMSwiWSI6MC43MDcxOTg2LCJUeXBlIjoibW91dGhMZWZ0In0seyJYIjowLjU5MzUyMTgzLCJZIjowLjcwNDIzNzgsIlR5cGUiOiJtb3V0aFJpZ2h0In0seyJYIjowLjU1ODc5NzYsIlkiOjAuNjQ5NjI5MiwiVHlwZSI6Im5vc2UifV0sIlBvc2UiOnsiUGl0Y2giOi0wLjY5OTMwOTk1LCJSb2xsIjotMy4wOTYzODAyLCJZYXciOi0zLjUyMDMzMTZ9LCJRdWFsaXR5Ijp7IkJyaWdodG5lc3MiOjQ0Ljg4MjQ4NCwiU2hhcnBuZXNzIjo2Ny4yMjczMX19LCJNYXRjaGVkRmFjZXMiOlt7IlNpbWlsYXJpdHkiOjk5Ljk4OTk2LCJGYWNlIjp7IkJvdW5kaW5nQm94Ijp7IkhlaWdodCI6MC4zOTQ2OTgsIldpZHRoIjowLjE2NDk3NiwiTGVmdCI6MC40NTEwOTksIlRvcCI6MC40MDAzNDl9LCJGYWNlSWQiOiI4MTdkZDFhZi1mZGI4LTRmZmMtYjQ5Mi1jOWY5ZmU4MTkyYTgiLCJDb25maWRlbmNlIjoxMDAuMCwiSW1hZ2VJZCI6ImQ2ZDc2NjRiLTE5MjItMzViYi1hMDkzLTIzZTBlZjA0MWY4NSIsIkV4dGVybmFsSW1hZ2VJZCI6InNhdGlzaDAxIn19XX1dfQ==', 'approximateArrivalTimestamp': 1573030687.219}, 'eventSource': 'aws:kinesis', 'eventVersion': '1.0', 'eventID': 'shardId-000000000000:49601089386756595653249534880211890627568915973756944386', 'eventName': 'aws:kinesis:record', 'invokeIdentityArn': 'arn:aws:iam::397577651207:role/service-role/smsdynamo-role-yf6jxfmo', 'awsRegion': 'us-east-1', 'eventSourceARN': 'arn:aws:kinesis:us-east-1:397577651207:stream/kds1'}
    #record = {'kinesis': {'kinesisSchemaVersion': '1.0', 'partitionKey': 'adb59f87-adc6-409f-911e-e0e79f1580c9', 'sequenceNumber': '49601089386756595653249533358378592196264337316778082306', 'data': 'eyJJbnB1dEluZm9ybWF0aW9uIjp7IktpbmVzaXNWaWRlbyI6eyJTdHJlYW1Bcm4iOiJhcm46YXdzOmtpbmVzaXN2aWRlbzp1cy1lYXN0LTE6Mzk3NTc3NjUxMjA3OnN0cmVhbS9rdnMxLzE1NzI3MzU5NDIxMTgiLCJGcmFnbWVudE51bWJlciI6IjkxMzQzODUyMzMzMTgxNDYyMTA4MTk0NzY1NjMwNDI5MzgxMzE2MzkzOTEzNTQxIiwiU2VydmVyVGltZXN0YW1wIjoxLjU3MzAxMTQ3NTgzN0U5LCJQcm9kdWNlclRpbWVzdGFtcCI6MS41NzMwMTE0NzUwMUU5LCJGcmFtZU9mZnNldEluU2Vjb25kcyI6MC40MzIwMDAwMTEyMDU2NzMyfX0sIlN0cmVhbVByb2Nlc3NvckluZm9ybWF0aW9uIjp7IlN0YXR1cyI6IlJVTk5JTkcifSwiRmFjZVNlYXJjaFJlc3BvbnNlIjpbeyJEZXRlY3RlZEZhY2UiOnsiQm91bmRpbmdCb3giOnsiSGVpZ2h0IjowLjM1NzU5ODkzLCJXaWR0aCI6MC4xOTg3NzcsIkxlZnQiOjAuNDUwNzQ5NSwiVG9wIjowLjQ4MDU4ODE0fSwiQ29uZmlkZW5jZSI6MTAwLjAsIkxhbmRtYXJrcyI6W3siWCI6MC40ODgzMDYwNSwiWSI6MC42MDUyMzcwNywiVHlwZSI6ImV5ZUxlZnQifSx7IlgiOjAuNTc2ODI1NzQsIlkiOjAuNTk1ODU1MywiVHlwZSI6ImV5ZVJpZ2h0In0seyJYIjowLjUwNTUxNTY0LCJZIjowLjczNzQ5OTUsIlR5cGUiOiJtb3V0aExlZnQifSx7IlgiOjAuNTc4Njg0NzUsIlkiOjAuNzMwMDYyOTYsIlR5cGUiOiJtb3V0aFJpZ2h0In0seyJYIjowLjUzMjYwMTgzLCJZIjowLjY3MzU2ODU1LCJUeXBlIjoibm9zZSJ9XSwiUG9zZSI6eyJQaXRjaCI6LTYuMTUzNzg1NywiUm9sbCI6LTYuMDk2NTYyLCJZYXciOi0yMC44MzQzMDd9LCJRdWFsaXR5Ijp7IkJyaWdodG5lc3MiOjQyLjk3NTAwMiwiU2hhcnBuZXNzIjo2Ny4yMjczMX19LCJNYXRjaGVkRmFjZXMiOltdfV19', 'approximateArrivalTimestamp': 1573011478.081}, 'eventSource': 'aws:kinesis', 'eventVersion': '1.0', 'eventID': 'shardId-000000000000:49601089386756595653249533358378592196264337316778082306', 'eventName': 'aws:kinesis:record', 'invokeIdentityArn': 'arn:aws:iam::397577651207:role/service-role/smsdynamo-role-yf6jxfmo', 'awsRegion': 'us-east-1', 'eventSourceARN': 'arn:aws:kinesis:us-east-1:397577651207:stream/kds1'}
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
            while(True):
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

    if check_frame:
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
    owner_phone = '+13476519231'
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
    visitor_photos.append(photo)
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