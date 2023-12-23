# Class Library for Check Point API.
# T. Lockman
# Last updated December 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

import requests
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Endpoint URLs
ADD_HOST = '/add-host'
ADD_NETWORK = '/add-network'
ADD_RANGE = '/add-address-range'
INSTALL_POLICY = '/install-policy'
LOGOUT = '/logout'
GENERIC_OBJECT_QUERY = '//show-generic-objects'
GENERIC_OBJECT_SET = '//set-generic-object'
PUBLISH = '/publish'
SHOW_DYNAMIC_OBJECT = '/show-dynamic-object'
SHOW_DYNAMIC_OBJECTS = '/show-dynamic-objects'
SHOW_UNUSED_OBJECTS = '/show-unused-objects'
SHOW_GROUP = '/show-group'
SHOW_GROUPS = '/show-groups'
SHOW_PACKAGES = '/show-packages'
SHOW_SIMPLE_GATEWAYS = '/show-simple-gateways'
SHOW_NAT_RULEBASE = '/show-nat-rulebase'
SHOW_TASK = '/show-task'
TOKEN = '/login'

class CPQMGMT:
    def __init__(self, manager, api_key):
        self.manager = manager
        self.api_key = api_key
        self.main_url = f'https://{self.manager}/web_api/'
        self.token = None
        self.token_timestamp = None
        self.token_session_timeout = 500
        self.verify = False

    @staticmethod
    def convert_dashes(dictionary):
        for key in list(dictionary.keys()):
            new_key = key.replace("_", "-")
            if new_key != key:
                dictionary[new_key] = dictionary.pop(key)
        return dictionary

    @staticmethod
    def generate_timestamp():
        timestamp = datetime.now()
        return timestamp

    def token_expired(self, timestamp):
        now = datetime.now()
        time_difference = (now - timestamp).total_seconds()
        if time_difference > self.token_session_timeout:
            return True
        else:
            return False

    def build_headers(self, token_request=False):
        if token_request:
            headers = {'Content-Type': 'application/json'}
        else:
            headers = {'Content-Type': 'application/json',
                       'X-chkp-sid': self.get_token()}
        return headers

    def build_url(self, endpoint):
        url = f'{self.main_url}{endpoint}'
        return url

    def post_full_request(self, full_url, headers, **kwargs):
        http_response = requests.post(url=full_url, headers=headers,
                                      json=kwargs, verify=self.verify)
        return http_response

    def get_token(self):
        if not self.token or self.token_expired(self.token_timestamp):
            parameters = {'api-key': self.api_key}
            try:
                http_response = self.post_full_request(self.build_url(TOKEN),
                                                    self.build_headers
                                                    (token_request=True),
                                                    **parameters)
                json_response = http_response.json()
                self.token = json_response['sid']
            except KeyError as e:
                print(f'\n\n***ERROR IN TOKEN RETRIEVAL***\n\n')
                if http_response.status_code != 200:
                    print(f'HTTP STATUS CODE: {http_response.status_code}\n\n')
                    print(f'***Please check your API key and manager info***\n\n')
            self.token_timestamp = datetime.now()
            return self.token
        else:
            return self.token

    def publish(self):
        http_response = self.post_full_request(self.build_url(PUBLISH),
                                               self.build_headers())
        json_response = http_response.json()
        return json_response

    def install_policy(self, policy_package, access='true',
                       threat_prevention='false'):
        parameters = self.convert_dashes({key: value for key,
                                          value in locals().items()
                                          if key != 'self' and
                                          value is not None})
        http_response = self.post_full_request(self.build_url(INSTALL_POLICY),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def add_host(self, name, ip_address, groups=None, color=None,
                 comments=None):
        parameters = self.convert_dashes({key: value for key,
                                          value in locals().items()
                                          if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(ADD_HOST),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def add_range(self, name, ip_address_first, ip_address_last, groups=None,
                  color=None, comments=None):
        parameters = self.convert_dashes({key: value for key, value in
                                          locals().items() if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(ADD_RANGE),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def add_network(self, name, subnet, mask_length, groups=None, color=None,
                    comments=None):
        parameters = self.convert_dashes({key: value for key, value in
                                          locals().items() if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(ADD_NETWORK),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def show_packages(self, limit=None, offset=None, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in
                                          locals().items() if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_PACKAGES),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        policypull = json_response['packages']
        policydict = {}
        for package in policypull:
            name = package['name']
            uid = package['uid']
            policydict[name] = uid
        return policydict

    def show_group(self, name, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in
                                          locals().items() if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_GROUP),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def show_groups(self, filter=None, limit=None, offset=None, order=None,
                    details_level=None):
        parameters = self.convert_dashes({key: value for key, value in
                                          locals().items() if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_GROUPS),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def show_task(self, task_id, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in
                                          locals().items() if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_TASK),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def show_nat_rulebase(self, package, filter=None, limit=None, offset=None,
                          order=None, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in
                                          locals().items() if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_NAT_RULEBASE),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def show_simple_gateways(self):
        http_response = self.post_full_request(self.build_url(SHOW_SIMPLE_GATEWAYS),
                                               self.build_headers())
        json_response = http_response.json()
        return json_response

    def show_dynamic_object(self, name, details_level=None):
        parameters = self.convert_dashes({key: value for key,
                                          value in locals().items()
                                          if key != 'self' and
                                          value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_DYNAMIC_OBJECT),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def show_unused_objects(self, limit=500):
        http_response = self.post_full_request(self.build_url(SHOW_UNUSED_OBJECTS),
                                               self.build_headers())
        json_response = http_response.json()
        return json_response

    def logout(self):
        http_response = self.post_full_request(self.build_url(LOGOUT),
                                               self.build_headers())
        json_response = http_response.json()
        return json_response

    def generic_object_query(self, name, details_level=None):
        parameters = self.convert_dashes({key: value for key,
                                          value in locals().items()
                                          if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(GENERIC_OBJECT_QUERY),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    def generic_object_set(self, name, details_level=None):
        parameters = self.convert_dashes({key: value for key,
                                          value in locals().items()
                                          if key != 'self'
                                          and value is not None})
        http_response = self.post_full_request(self.build_url(GENERIC_OBJECT_SET),
                                               self.build_headers(),
                                               **parameters)
        json_response = http_response.json()
        return json_response

    # For additional generic object reference old Check Point file.



