# Sigfox API v2 examples

This repository contains some examples on how to use Sigfox API v2 in Python. It is simply based on `requests` package.

For more information on API v2 you can refer to: https://support.sigfox.com/apidocs

## Requirements

- Sigfox API credentials (https://support.sigfox.com/docs/api-credential-creation)
- `requests` package

## Scripts

- `createCallbacksInGroups.py`

Creates identical callbacks for all device types in a same group. It is particularly useful when each of your devices are in unique device types (ie: registered Dev Kits).

The script creates a Data Advanced Callback but you can easily adapt the content for any other type of callback.


- `createDTDevices.py`

Creates unique Device Types / Devices based on a list of Sigfox ID/PAC stored in multiple .csv files. This can be used to transfer a list of devices between different groups.

- `createFreeAccount.py`

Creates a new subgroup/device type/device in your Sigfox backend group using interactive mode. Typical use: you want to give a free account to a user without giving access to your whole group. A dedicated subgroup with the user's device will be created.