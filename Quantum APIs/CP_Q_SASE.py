# Class Library to interact with CP Quantum SASE (formerly Perimeter81).
# T. Lockman
# Last updated December 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

import requests
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# API Version
api_version_1 = 'v1'
api_version_2 = 'v2'
# Endpoint URLs
ADDRESSES = '/objects/addresses'
ADDRESSES_BY_ID = '/objects/addresses/{}'
GROUPS = '/groups'
NETWORKS = '/networks'


class CPQS:
    def __init__(self, api_key):
        self.api_key = api_key
        self.auth_url = f'https://api.perimeter81.com/api/{api_version_1}/auth/authorize'
        self.main_url = f'https://api.perimeter81.com/api/rest/{api_version_2}'
        self.token = None
        self.token_timestamp = None
        self.token_session_timeout = 3000
        self.verify = False

    def token_expired(self, timestamp):
        now = datetime.now()
        time_difference = (now - timestamp).total_seconds()
        if time_difference > self.token_session_timeout:
            return True
        else:
            return False

    def build_headers(self, token_request=False, no_json=False):
        if token_request:
            headers = {'Content-Type': 'application/json'}
        elif no_json:
            headers = {'Authorization': f'Bearer {self.get_token()}'}
        else:
            headers = {'Content-Type': 'application/json',
                       'Authorization': f'Bearer {self.get_token()}'}
        return headers

    def build_url(self, endpoint):
        url = f'{self.main_url}{endpoint}'
        print(url)
        return url

    def get_full_request(self, full_url, headers):
        http_response = requests.get(url=full_url, headers=headers,
                                      verify=self.verify)
        return http_response
    
    def post_full_request(self, full_url, headers, **kwargs):
        http_response = requests.post(url=full_url, headers=headers,
                                      json=kwargs, verify=self.verify)
        return http_response
    
    def put_full_request(self, full_url, headers, **kwargs):
        http_response = requests.put(url=full_url, headers=headers,
                                      json=kwargs, verify=self.verify)
        return http_response
    
    def delete_full_request(self, full_url, headers):
        http_response = requests.delete(url=full_url, headers=headers,
                                      verify=self.verify)
        return http_response

    def get_token(self):
        if not self.token or self.token_expired(self.token_timestamp):
            parameters = {'grantType': 'api_key', "apiKey": self.api_key}
            try:
                http_response = self.post_full_request(self.auth_url,
                                                    self.build_headers
                                                    (token_request=True),
                                                    **parameters)
                json_response = http_response.json()
                self.token = json_response['data']['accessToken']
            except KeyError as e:
                print(f'\n\n***ERROR IN TOKEN RETRIEVAL***\n\n')
                if http_response.status_code != 200:
                    print(f'HTTP STATUS CODE: {http_response.status_code}\n\n')
                    print(f'***Please check your API key***\n\n')
            self.token_timestamp = datetime.now()
            return self.token
        else:
            return self.token

    def create_group(self, name, **kwargs):
        parameters = {'name': name}
        parameters.update(kwargs)
        http_response = self.post_full_request(self.build_url(GROUPS),
                                                self.build_headers(),
                                                **parameters)
        json_response = http_response.json()
        return json_response
    
    def create_addresses(self, name, **kwargs):
        '''
        valuetype can be any of: ip, list(a list of ip), cidr(only one)
        '''
        parameters = {'name': name}
        parameters.update(kwargs)
        print(f'PARAMETERS: {parameters}')
        http_response = self.post_full_request(self.build_url(ADDRESSES),
                                                self.build_headers(),
                                                **parameters)
        json_response = http_response.json()
        print(json_response)
        return json_response
    
    def update_addresses(self, id, **kwargs):
        '''
        valuetype can be any of: ip, list(a list of ip), cidr(only one)
        '''
        parameters = kwargs
        http_response = self.put_full_request(self.build_url(
                                              ADDRESSES_BY_ID.format(id)),
                                                self.build_headers(),
                                                **parameters)
        json_response = http_response.json()
        print(json_response)
        return json_response
    
    def get_all_addresses(self):
        http_response = self.get_full_request(self.build_url(ADDRESSES),
                                              self.build_headers())
        json_response = http_response.json()
        print(http_response)
        print(json_response)
        return json_response
    
    def get_all_networks(self):
        http_response = self.get_full_request(self.build_url(NETWORKS),
                                              self.build_headers())
        json_response = http_response.json()
        return json_response
    
    def delete_address(self, id):
        http_response = self.delete_full_request(self.build_url(
                                              ADDRESSES_BY_ID.format(id)),
                                              self.build_headers(False, True))
        return http_response