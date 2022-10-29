import requests
import time
import base64
import hashlib
import hmac
import secrets

server_ip = secrets.SERVER_IP
server_port = secrets.SERVER_PORT
sms_access_key = secrets.SMS_ACCESS_KEY
sms_secret_key = secrets.SMS_SECRET_KEY
sms_uri = secrets.SMS_URI
sms_url = secrets.SMS_URL
sms_type = secrets.SMS_TYPE
sms_from_countryCode = secrets.SMS_FROM_COUNTRYCODE
sms_from_number = secrets.SMS_FROM_NUMBER
sms_to_number = secrets.SMS_TO_NUMBER

def make_signature(access_key, secret_key, method, uri, timestmap):
    timestamp = str(int(time.time() * 1000))
    secret_key = bytes(secret_key, 'UTF-8')

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

def send_sms(phone_number, subject, message):
    #  URL
    url = sms_url
    # access key
    access_key = sms_access_key
    # secret key
    secret_key = sms_secret_key
    # uri
    uri = sms_uri
    timestamp = str(int(time.time() * 1000))

    body = {
        "type": sms_type,
        "contentType": "COMM",
        "countryCode": sms_from_countryCode,
        "from": sms_from_number,
        "content": message,
        "messages": [
            {
                "to": phone_number,
                "subject": subject,
                "content": message
            }
        ]
    }

    key = make_signature(access_key, secret_key, 'POST', uri, timestamp)
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': key
    }

    res = requests.post(url, json=body, headers=headers)
    print(res.json())
    return res.json()

text = "[띠리링] 피보호자의 움직임이 없어 위험합니다. 연락주세요."
send_sms(sms_to_number, sms_from_number, text)
