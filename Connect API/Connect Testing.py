import requests

# API
clientid = "enter clientid here"
secretkey = "enter secret key here"

# Auth Params
auth_url = "https://cloudinfra-gw-us.portal.checkpoint.com/auth/external"
auth_headers = {"Content-Type": "application/json"}
auth_parameters = {"clientId": clientid, "accessKey": secretkey}
token = requests.post(url=auth_url, headers=auth_headers, json=auth_parameters).json()["data"]["token"]
print(token)
print(type(token))

# Endpoint Params
endpoint_url = "https://cloudinfra-gw-us.portal.checkpoint.com/app/harmonyconnect/v3"
authorization = f"Bearer {token}"
endpoint_header = {"Authorization": authorization}

# URLs
networkLists = "/networkLists"
publish = "/publishChanges"

# Network Lists
networkListsURL = f"{endpoint_url}{networkLists}"

# Get
get_url = f"{endpoint_url}{networkLists}?offset=0&limit=20"
http_response = requests.get(url=get_url, headers=endpoint_header)
json_response = http_response.json()
print(http_response)
print(json_response)


# Post
network_parameters = {"name": "Test_API3", "networks": ["10.10.9.0/24", "192.164.0.0/16"], "description": "TestAPI3"}
http_response = requests.post(url=networkListsURL, headers=endpoint_header, json=network_parameters)
json_response = http_response.json()
print(http_response)
print(json_response)
 
# Publish
publishURL = f"{endpoint_url}{publish}"
http_response = requests.post(url=publishURL, headers=endpoint_header)
json_response = http_response.json()
print(http_response)
print(json_response)




