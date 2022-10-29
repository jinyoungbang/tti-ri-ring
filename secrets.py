from decouple import config

ETRI_ACCESS_KEY = config('etriAccessKey', default='')
SERVER_IP = config('serverIp', default='')
SERVER_PORT = config('serverPort', default='')
SMS_ACCESS_KEY = config('smsAccessKey', default='')
SMS_SECRET_KEY = config('smsSecretKey', default='')
SMS_URI = config('smsUri', default='')
SMS_URL = config('smsUrl', default='')
SMS_TYPE = config('smsType', default='')
SMS_FROM_COUNTRYCODE = config('smsFromCountryCode', default='')
SMS_FROM_NUMBER = config('smsFromNumber', default='')
SMS_TO_NUMBER = config('smsToNumber', default='')