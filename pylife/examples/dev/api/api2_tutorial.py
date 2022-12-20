# Path to pylife
path_root = 'C:/Users/MichelClet/Desktop/mcl/python/'

import sys
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()
import json
import requests

url_root = "https://prod.chronolife.net/api/2"
api_key = "f9VBqQoTiU0mnAKoXK1lkw"

# %% POST. Generate a TOKEN
username = 'Username'
password = 'oooooooo'
url = url_root + "/user/{userId}/token".format(userId=username)

str_otp_token = 123456
# Build the payload with the otp_token given by Google Authenticator.
request_body = {'otp_token': str_otp_token}

# Perform the POST request authenticated with the "Basic" authentication scheme. 
reply = requests.post(url, auth=(username, password), json=request_body)

print(reply.status_code)
if reply.status_code == 200: # We chose 200 OK for successful request instead of 201 Created!
    json_reply = json.loads(reply.text)
    print("API Key: ", json_reply['apiKey'])
elif reply.status_code == 400:
    print('Part of the request could not be parsed or is incorrect.')
elif reply.status_code == 401:
    print('Invalid authentication')
elif reply.status_code == 403:
    print('Not authorized.')
elif reply.status_code == 404:
    print('Invalid url')

# %% GET: Retrieve relevant properties of the specified user.
#  The returned properties depend on the account type. For a data manager account, the list sub-users id is returned. The requester should have admin privileges or the specified user should be the requester or a sub-user of the requester.
userId = 'XXXXXX'
url = url_root + "/user/{userId}".format(userId=userId)

reply = requests.get(url, headers={"X-API-Key": api_key})
print(reply.status_code)
if reply.status_code == 200:
    # Convert the reply content into a json object.
    json_list_of_records = json.loads(reply.text) 
    print(json_list_of_records)
elif reply.status_code == 400:
    print('Part of the request could not be parsed or is incorrect.')
elif reply.status_code == 401:
    print('Invalid authentication')
elif reply.status_code == 403:
    print('Not authorized.')
elif reply.status_code == 404:
    print('Invalid url')
elif reply.status_code == 500:
    print('Invalid user ID')


# %% CREATE USER ID
url     = url_root + "/user" 
# reply   = requests.post(url, headers={"X-API-Key": api_key})

print(reply.status_code)
if reply.status_code == 200:
    # Convert the reply content into a json object.
    json_list_of_records = json.loads(reply.text) 
    print('User created')
    print(json_list_of_records)
elif reply.status_code == 400:
    print('Part of the request could not be parsed or is incorrect.')
elif reply.status_code == 401:
    print('Invalid authentication')
elif reply.status_code == 403:
    print('Not authorized.')   
elif reply.status_code == 404:
    print('Invalid url')

# %% DELETE USER
userId = 'XXXXXX' 
url = url_root + "/user/{userId}".format(userId=userId)

reply = requests.delete(url, headers={"X-API-Key": api_key})
print(reply.status_code)
if reply.status_code == 200:
    # Convert the reply content into a json object.
    json_list_of_records = json.loads(reply.text) 
    print('User deleted')
    print(json_list_of_records)
elif reply.status_code == 400:
    print('Part of the request could not be parsed or is incorrect.')
elif reply.status_code == 401:
    print('Invalid authentication')
elif reply.status_code == 403:
    print('Not authorized.')    
elif reply.status_code == 404:
    print('Invalid url')

# %% PUT. Block a user

userId = 'XXXXX' 
url = url_root + "/user/{userId}/blocked".format(userId=userId)

request_body = {'blocked': False}

# Perform the POST request authenticated with the "Basic" authentication scheme. 
reply = requests.put(url, headers={"X-API-Key": api_key}, json=request_body)

print(reply.status_code)
if reply.status_code == 200:
    # Convert the reply content into a json object.
    json_list_of_records = json.loads(reply.text) 
    print('User block updated')
    print(json_list_of_records)
elif reply.status_code == 400:
    print('Part of the request could not be parsed or is incorrect.')
elif reply.status_code == 401:
    print('Invalid authentication')
elif reply.status_code == 403:
    print('Not authorized.') 
elif reply.status_code == 404:
    print('Invalid url')
    
# %% PUT. Change the email of the specified user.

userId = 'XXXXXX' 
url = url_root + "/user/{userId}/email".format(userId=userId)

# Build the payload with the otp_token given by Google Authenticator.
request_body = {'email': "XXXXXXXXX@chronolife.net"}

# Perform the POST request authenticated with the "Basic" authentication scheme. 
reply = requests.put(url, headers={"X-API-Key": api_key}, json=request_body)

print(reply.status_code)
if reply.status_code == 200:
    # Convert the reply content into a json object.
    json_list_of_records = json.loads(reply.text) 
    print('Email updated')
    print(json_list_of_records)
elif reply.status_code == 400:
    print('Part of the request could not be parsed or is incorrect.')
elif reply.status_code == 401:
    print('Invalid authentication')
elif reply.status_code == 403:
    print('Not authorized.')
elif reply.status_code == 404:
    print('Invalid url')   


# %% GET DATA
url = url_root + "/data"

# Build the query parameters object.
params = {
  'user':       'XXXXX', # sub-user username example : 4JusXu 
  'types':      'temp_1',
  'date':       '2022-05-13',
  'time_gte':   '17:15:00',
  'time_lt':    '17:15:01'
}

reply = requests.get(url, headers={"X-API-Key": api_key}, params=params)
print(reply.status_code)
datas = []
if reply.status_code == 200:
  # Convert the reply content into a json object.
  json_list_of_records = json.loads(reply.text) 
  for record in json_list_of_records:
      datas.append(record)
elif reply.status_code == 400:
    print('Part of the request could not be parsed or is incorrect.')
elif reply.status_code == 401:
    print('Invalid authentication')
elif reply.status_code == 403:
    print('Not authorized.')
elif reply.status_code == 404:
    print('Invalid url')
elif reply.status_code == 500:
    print('Invalid user ID')

if len(datas) == 0:
    print('No data found')


