"""
Generate a token (API key) for API v2
"""

import json
import requests

web_env     = input('prod or preprod? ').lower()
if web_env not in ['prod', 'preprod']:
    raise NameError('Please choose prod or preprod')

username    = input('username: ')
password    = input('password: ')
otp_token   = input('double authentification (otp token): ')

# URL
url = "https://" + web_env + ".chronolife.net/api/2/user/{userId}/token".format(userId=username)

# Build the payload with the otp_token given by Google Authenticator.
request_body = {'otp_token': int(otp_token)}

# Perform the POST request authenticated with the "Basic" authentication scheme. 
reply = requests.post(url, auth=(username, password), json=request_body)

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