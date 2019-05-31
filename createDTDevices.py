# create unique device types / devices from a list of Sigfox ID/PAC stored in multiple csv files

import requests
import csv
from os import listdir

API_URL = "https://api.sigfox.com/v2/"
API_USER = "YOUR API USER"
API_PWD = "YOUR API PASSWORD"
GROUP_ID = "YOUR GROUP ID"
CONTRACT_ID = "YOUR CONTRACT ID"
PRODUCT_KEY = "P_0001_DEE3_01" # device product certificate

FILES_LOCATION = "C:/tmp/"

# retrieve list of csv files and save ID and PAC
id_pac = []
pac_files = listdir(FILES_LOCATION)
for pf in pac_files:
    with open(FILES_LOCATION + pf, newline='') as csvfile:
        pacreader = csv.reader(csvfile, delimiter=';')
        id_pac += [row for row in pacreader]

print(id_pac)

for i in range(0, len(id_pac)):

    # create device type
    body_content = {
      "name": "Akeru_" + id_pac[i][0],
      "keepAlive": 0,
      "payloadType": 2,
      "downlinkMode": 2,
      "description": "Akeru_" + id_pac[i][0],
      "groupId": GROUP_ID,
      "contractId": CONTRACT_ID,
      "automaticRenewal": True
    }

    devtype_creation = requests.post(API_URL + "device-types/", json=body_content, auth=(API_USER, API_PWD)).json()
    print(devtype_creation)

    # create device
    body_content = {
      "id": id_pac[i][0],
      "name": id_pac[i][0],
      "pac": id_pac[i][1],
      "deviceTypeId": devtype_creation['id'],
      "productCertificate": { "key": PRODUCT_KEY },
      "prototype":False,
      "automaticRenewal": True,
      "activable": True
    }

    dev_creation = requests.post(API_URL + "devices/", json=body_content, auth=(API_USER, API_PWD)).json()
    print(dev_creation)
