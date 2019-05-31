# create callbacks for all device types in a same group
import requests

API_URL = "https://api.sigfox.com/v2/"
API_USER = "YOUR API USER" # Backend API USER for ST workshop group with Device Manager W rights
API_PWD = "YOUR API PASSWORD"

deviceTypes = requests.get(API_URL + "device-types/", auth=(API_USER, API_PWD)).json()

# Data Advanced callback content
body_content = {
  "channel": "URL",
  "callbackType": 1,
  "callbackSubtype": 6,
  "enabled": True,
  "sendDuplicate": False,
  "url": "http://test.test",
  "httpMethod": "POST",
  "downlinkHook": False,
  "headers": {
      "verification-code": "knowhowexchange",
      "device": "{device}"
      },
  "content-type": "application/json",
  "sendSni": True,
  "bodyTemplate": """[
    {
    \"variable\": \"device\",
    \"value\": \"{device}\",
    \"serie\": \"{time}\"
    },
    {
    \"variable\": \"data\",
    \"value\": \"{data}\",
    \"serie\": \"{time}\"
    },
    {
    \"variable\": \"seqNumber\",
    \"value\": \"{seqNumber}\",
    \"serie\": \"{time}\"
    },
    {
    \"variable\": \"location\",
    \"serie\": \"{time}\",
    \"location\": {computedLocation}
    }
]"""
}
# scan device types
for d in deviceTypes['data']:

    creation_response = requests.post(API_URL + "device-types/" + d['id'] + "/callbacks", json=body_content, auth=(API_USER, API_PWD))
    print("### callback creation for " + d['id'])
    print(creation_response)
    print(creation_response.text)
