import requests

# API
clientid = "630f5b8817e24c78851c57c24d7a36c0"
secretkey = "c6716788751f471eb2ca9e79af8b7a1a"

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




