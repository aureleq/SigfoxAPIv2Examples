# create a new subgroup/device type/device in your Sigfox backend group
# typically useful to create users free accounts

import requests

API_URL = "https://api.sigfox.com/v2/"
API_USER = "YOUR API USER"
API_PWD = "YOUR API PASSWORD"
GROUP_ID = "YOUR GROUP ID"


# function to retrieve list of subgroups
def getGroups(groupId=GROUP_ID):
    groupsList = requests.get(API_URL + "groups/?parentIds=" + groupId, auth=(API_USER, API_PWD)).json()
    groups = []
    for g in groupsList['data']:
        groups += [{"name": g['name'], "id": g['id']}] # store group name and ID
    return groups


# function to get user's group selection
def getUserSelection(inputData, displayKey):
    while(1):
        for i in range(len(inputData)): # print list of groups
            print(str(i) + ". " + inputData[i][displayKey])
        if len(inputData) == 0: #no subgroups
            sel = input("Press enter to select this group or type NEW to create a new one: ")
            return sel
        sel = input("Select a Group or type NEW to create a new one in this list: ")
        if sel == "NEW" or int(sel) in range(len(inputData)):
            return sel
        else:
            print("Invalid Selection")


# function to create group
# group type: BasicCreateInfo (2), timezone: UTC
# in: parentGroup, groupName, email
def createGroup(parentGroup, groupName, email):
    body_content = {
      "name": groupName,
      "description": groupName,
      "type": 2,
      "timezone": "UTC",
      "parentId": parentGroup,
      "billable": False,
      "technicalEmail": email,
    }

    groupCreation = requests.post(API_URL + "groups/", json=body_content, auth=(API_USER, API_PWD))
    if groupCreation.status_code == 200 or groupCreation.status_code == 201:
        print("Group created successfully!")
        return groupCreation.json()["id"]
    else:
        print("Cannot Create Group, error:")
        print(groupCreation.text)
        return False


# loop into subgroups to create new group, returns selected or new created groupID
def selectGroup():
    currentGroupId = GROUP_ID
    while(1):
        print("groupID:" + currentGroupId)
        groups = getGroups(currentGroupId)
        sel = getUserSelection(groups, "name")
        if sel == "": # no new group creation
            return currentGroupId
        elif sel =="NEW": # call createGroup function
            groupName = input("Please enter the group's name (ie: First & Last Name for individuals, University Name...): ")
            email = input("Please enter users's email: ")
            return createGroup(currentGroupId, groupName, email)
        else:
            print("Group " + groups[int(sel)]["name"] + " selected")
            currentGroupId = groups[int(sel)]["id"]


# display list of available contracts and returns selected one
def selectContract(groupId=GROUP_ID):
    contractsList = requests.get(API_URL + "contract-infos?groupId=" + groupId, auth=(API_USER, API_PWD)).json()
    while(1):
        for c_i, c in enumerate(contractsList['data']):
            print(str(c_i) + ". " + c['name'] + " (tokens left: " + str(c["maxTokens"]-c["tokensInUse"]-c["tokensUsed"]) + ")")
        sel = input("Select contract: ")
        if int(sel) in range(len(contractsList['data'])):
            return contractsList['data'][int(sel)]['id']
        else:
            print("Invalid Selection")


# function to create device type
# in: groupId, contractId, name
def createDeviceType(groupId, contractId, name):
    body_content = {
      "name": name,
      "keepAlive": 0,
      "payloadType": 2,
      "downlinkMode": 2,
      "description": name,
      "groupId": groupId,
      "contractId": contractId,
      "automaticRenewal": True
    }

    devtypeCreation = requests.post(API_URL + "device-types/", json=body_content, auth=(API_USER, API_PWD))

    if devtypeCreation.status_code == 200 or devtypeCreation.status_code == 201:
        print("Device Type created successfully!")
        return devtypeCreation.json()["id"]
    else:
        print("Cannot Create Device Type, error:")
        print(devtypeCreation.text)
        return False


# No API to retrieve list of certificates, to be entered manually
def selectPCertificate():
    print("Refer to https://partners.sigfox.com if you don't know your product certificate")
    sel = input("Product Certificate? (ie Arduino MKRFox: P_00C1_1366_01) ")
    return sel


# create device
def createDevice(id, pac, deviceTypeId, pCertificate, prototype=False):
    body_content = {
      "id": id,
      "name": id,
      "pac":pac,
      "deviceTypeId": deviceTypeId,
      "productCertificate": { "key": pCertificate },
      "prototype": prototype,
      "automaticRenewal": False,
      "activable": True
    }

    devCreation = requests.post(API_URL + "devices/", json=body_content, auth=(API_USER, API_PWD))

    if devCreation.status_code == 200 or devCreation.status_code == 201:
        print("Device created successfully!")
        print("Link to new device: https://backend.sigfox.com/device/" + str(int(devCreation.json()["id"], 16)))
        return True
    else:
        print("Cannot Create Device Type, error:")
        print(devCreation.text)
        return False


# select or create group if needed
selectedGroup = selectGroup()

# create device type
contract = selectContract()
devtypeName = input("Please enter the Device Type Name (ie: Arduino_DevKit): ")
devtypeId = createDeviceType(selectedGroup, contract, devtypeName)

# create device
pCertificate = selectPCertificate()
id = input("Please enter the Device ID: ")
pac = input("Please enter the Device PAC: ")
createDevice(id, pac, devtypeId, pCertificate)
