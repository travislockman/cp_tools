# Class Library for Check Point API.
# T. Lockman
# February 2023
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
SHOW_GROUP = '/show-group'
SHOW_GROUPS = '/show-groups'
SHOW_PACKAGES = '/show-packages'
SHOW_SIMPLE_GATEWAYS = '/show-simple-gateways'
SHOW_NAT_RULEBASE = '/show-nat-rulebase'
SHOW_TASK = '/show-task'
TOKEN = '/login'

class CPAPI:
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
        print(f'TIMESTAMP IS {timestamp}')
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
            headers = {'Content-Type': 'application/json', 'X-chkp-sid': self.get_token()}
        return headers

    def build_url(self, endpoint):
        url = f'{self.main_url}{endpoint}'
        return url

    def post_full_request(self, full_url, headers, **kwargs):
        http_response = requests.post(url=full_url, headers=headers, json=kwargs, verify=self.verify)
        return http_response

    def get_token(self):
        if not self.token or self.token_expired(self.token_timestamp):
            print('IF TRIGGERED')
            print(f'TOKEN at start of IF IS: {self.token}')
            parameters = {'api-key': self.api_key}
            http_response = self.post_full_request(self.build_url(TOKEN),
                                                   self.build_headers(token_request=True), **parameters)
            json_response = http_response.json()
            self.token = json_response['sid']
            self.token_timestamp = datetime.now()
            print(f'TOKEN at end of IF IS: {self.token}')
            return self.token
        else:
            print('ELSE TRIGGERED')
            print(f'TOKEN IS: {self.token}')
            return self.token

    def publish(self):
        http_response = self.post_full_request(self.build_url(PUBLISH), self.build_headers())
        json_response = http_response.json()
        return json_response

    def install_policy(self, policy_package, access='true', threat_prevention='false'):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(INSTALL_POLICY), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def add_host(self, name, ip_address, groups=None, color=None, comments=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(ADD_HOST), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def add_range(self, name, ip_address_first, ip_address_last, groups=None, color=None, comments=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(ADD_RANGE), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def add_network(self, name, subnet, mask_length, groups=None, color=None, comments=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(ADD_NETWORK), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def show_packages(self, limit=None, offset=None, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_PACKAGES), self.build_headers(), **parameters)
        json_response = http_response.json()
        policypull = json_response['packages']
        policydict = {}
        for package in policypull:
            name = package['name']
            uid = package['uid']
            policydict[name] = uid
        return policydict

    def show_group(self, name, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_GROUP), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def show_groups(self, filter=None, limit=None, offset=None, order=None, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_GROUPS), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def show_task(self, task_id, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_TASK), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def show_nat_rulebase(self, package, filter=None, limit=None, offset=None, order=None, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_NAT_RULEBASE), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def show_simple_gateways(self):
        http_response = self.post_full_request(self.build_url(SHOW_SIMPLE_GATEWAYS), self.build_headers())
        json_response = http_response.json()
        return json_response

    def show_dynamic_object(self, name, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(SHOW_DYNAMIC_OBJECT), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def logout(self):
        http_response = self.post_full_request(self.build_url(LOGOUT), self.build_headers())
        json_response = http_response.json()
        return json_response

    def generic_object_query(self, name, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(GENERIC_OBJECT_QUERY), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    def generic_object_set(self, name, details_level=None):
        parameters = self.convert_dashes({key: value for key, value in locals().items()
                                          if key != 'self' and value is not None})
        http_response = self.post_full_request(self.build_url(GENERIC_OBJECT_QUERY), self.build_headers(), **parameters)
        json_response = http_response.json()
        return json_response

    # For additional generic object reference old Check Point file.


class CPAPI_TOOLS():  # Work in progress
    def __init__(self, manager, api_key):
        self.manager = manager
        self.api_key = api_key
        self.cpapi = CPAPI(self.manager, self.api_key)

    def group_to_csv(self, group_name):
        member_list = None
        response = self.cpapi.show_group(group_name, details_level='full')
        for key, value in response.items():
            if key == 'members':
                member_list = value
        for member in member_list:
            name = member['name']
            if 'ipv4-address' in member:
                print('FOUND AN IP')

        self.cpapi.logout()
        return member_list



if __name__ == '__main__':
    manager = 'manager info here'
    api_key = 'api key here'

    cp = CPAPI(manager, api_key)
    cputils = CPAPI_TOOLS(manager, api_key)

    # EXAMPLE USAGES

    # group_json = cputils.group_to_csv('TEST_GROUP')
    # print(group_json)

    # Token Demo
    # import time
    # token = cp.get_token()
    # token = cp.get_token()
    # token = cp.get_token()
    # time.sleep(60)
    # token = cp.get_token()

    # print(cp.show_packages())
    #print(cp.show_group('Admin_machines', details_level='full'))
    # print(cp.show_groups())
    # print(cp.show_nat_rulebase('AntaeusLab_ESXi_Main'))
    # print(cp.show_simple_gateways())
    # print(cp.generic_object_query('AntaeusLab_ESXi_External', details_level='full'))

    # print(cp.add_host('Pizza', '10.10.33.37'))
    # print(cp.publish())

    # print(cp.show_task('41e821a0-3720-11e3-aa6e-0800200c9fde', details_level='full'))

    #print(cp.logout())
