# Class Library containing various tools for Check Point Management.
# T. Lockman
# Last updated November 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from CP_Q_MGMT import CPQMGMT
from cp_q_mgmt_utils import CPQMGMTUTILS

class CPQMGMTTOOLS:
    """
    This is class containing tools I wrote to leverage the CPAPI class above.
    """
    def __init__(self, manager, api_key):
        self.manager = manager
        self.api_key = api_key
        self.cpapi = CPQMGMT(self.manager, self.api_key)
        self.cputils = CPQMGMTUTILS()

    def group_to_csv(self, group_name):
        """
        Parse a group in the Check Point manager
        and convert objects to CSV files.
        """
        member_list = None
        hosts_list = []
        networks_list = []
        domains_list = []
        ranges_list = []
        master_dict = {
            'hosts': hosts_list, 'networks': networks_list,
            'domains': domains_list, 'ranges': ranges_list
                       }
        static_filename = 'cpapi_tools_group_csv'

        # Fetching the group from the manager
        response = self.cpapi.show_group(group_name, details_level='full')
        
        # Parsing the JSON for the member list 
        for key, value in response.items():
            if key == 'members':
                member_list = value
        
        # Iterating through each member, and storing in memory
        for member in member_list:
            # Extracting the useful information for each member
            name = member['name']
            object_type = member['type']
            meta_data = member['meta-info']
            meta_dict ={
                    'date_created': meta_data['creation-time']['iso-8601'],
                    'date_modified': meta_data['last-modify-time']['iso-8601'],
                    'created_by': meta_data['creator']
                        }
            if object_type == 'host': 
                host = {
                    'name': name, 'ipv4': member['ipv4-address'], **meta_dict
                        }
                hosts_list.append(host)
            elif object_type == 'network':
                network = {
                    'name': name, 'network': member['subnet4'],
                    'mask': member['subnet-mask'],
                    'mask_length': member['mask-length4'], **meta_dict
                          }
                networks_list.append(network)
            elif object_type == 'dns-domain':
                domain = {
                    'name': name, 'domain': name, **meta_dict
                          }
                domains_list.append(domain)
            elif object_type == 'address-range':
                range = {
                    'name': name, 'start': member['ipv4-address-first'],
                    'end': member['ipv4-address-last']
                        }
                ranges_list.append(range)
        
        # Post-processing and CSV Writing
        for key, value in master_dict.items():
            if value:
                self.cputils.list_of_dict_to_csv(f'{static_filename}_{group_name}_{str(key)}.csv', value) 
        
        self.cpapi.logout()
        return member_list