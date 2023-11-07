# Utility to pull your public IP and add it to a group.
# Can be used for quick remote administration.
# T. Lockman, CP SE
# June 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

"""
Please note you must also use the CHECKPOINT.py and TIME_UTILS.py files in the same directory
"""

from CHECKPOINT import CPAPI
from TIME_UTILS import Time_Utils
import requests
import time
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class IP_Allow:

    def __init__(self):
        self.manager = 'Enter management ip or Smart-1 Cloud Tenant here'
        self.api_key = 'Enter API token here'
        self.firewall_api = CPAPI(self.manager, self.api_key)  # Change this if you change firewalls!
        self.time_utils = Time_Utils()
        self.firewall_policy = 'Enter policy name here'
        self.group_name = 'Group name'
        self.hostname = 'Title of object here'
        self.color = 'firebrick'  # feel free to change color
        self.comments = 'Comment to add, timestamp will also be added'

        # Don't change this, it will pull your public IP
        self.IP_URL = 'http://ip-api.com/json'
        # self.IP_URL = 'https://api.ipify.org?format=json'  # Alternate


    def get_public_ip(self):
        print('Acquiring your Public IP...')
        data = requests.get(self.IP_URL).json()['query']
        #data = requests.get(self.IP_URL).json()['ip'] # Alternate
        print(f'Your public IP is {data}')
        return data

    def allow_ip_admin(self):
        datestamp = self.time_utils.iso8601_utc()
        self.comments = f'{datestamp} {self.comments}'
        ip = IP_Allow().get_public_ip()
        hostname = f'{self.hostname}{ip}'
        print('Adding IP to group and publishing changes...')
        response = self.firewall_api.add_host(hostname, ip, groups=self.group_name, color=self.color, comments=self.comments)
        print(f'\nResult of adding host is: {response}\n')
        time.sleep(10)
        if '_err' in str(response):
            print('ERROR DETECTED, EXITING!')
        else:
            response = self.firewall_api.publish()
            time.sleep(10)
            print(f'\nResult of publishing is: {response}\n')
            print(f'Now installing policy to firewall...')
            response = self.firewall_api.install_policy(self.firewall_policy)
            print(f'Result of policy install is: {response}\n')
            print("Pausing for 60 seconds to allow for policy push!")
            time.sleep(60)
            print('\nFinished!')
            return response

    def show_task(self, task_id):
        response = self.firewall_api.show_task(task_id)
        return response



if __name__ == '__main__':
    IP_Allow().allow_ip_admin()


    # Use this for troubleshooting, you can pull the task IDs from the printout and check them
    # task = '01234567-89ab-cdef-be46-bf8a342f02b4'
    # task_result = IP_Allow().show_task(task)
    # print(task_result)


