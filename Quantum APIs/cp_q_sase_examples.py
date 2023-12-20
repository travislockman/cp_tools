# Example usages of my Check Point Quantum SASE Libraries
# T. Lockman
# Last updated December 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

from CP_Q_MGMT import CPQMGMT
from cp_q_mgmt_tools import CPQMGMTTOOLS
from CP_Q_SASE import CPQS
from cp_q_sase_tools import CPQSASETOOLS
from cp_q_sase_utils import CPQSASEUTILS
from csv_env import CSVENV # Remove this if you have your own env

'''
Environment variables so you don't see my unmentionables.
You can remove this whole section and put your own envs in.
'''
env_file_name = 'env.csv'  # Replace with your CSV file name
env_vars = CSVENV.read_csv(env_file_name)
smart1_manager = env_vars['smart1_manager'] # Add your own env variable here.
smart1_api_key = env_vars['smart1_api_key'] # Add your own env variable here.
sase_api_key = env_vars['p81_api_key'] # Add your own env variable here.

# Assigning classes
cp = CPQMGMT(smart1_manager, smart1_api_key)
cptools = CPQMGMTTOOLS(smart1_manager, smart1_api_key)
sase = CPQS(sase_api_key)
sasetools= CPQSASETOOLS(sase_api_key)
saseutils = CPQSASEUTILS(sase_api_key)

# Sample scripts #

# CP Manager Group Converter
'''
Parse a group in a CP manager, break it into csvs and create address objects
in Quantum SASE.  For now only IP address groups are supported.
Also it cannot detect nested groups, this may be improved later.
'''
parse_group = cptools.group_to_csv('TEST_GROUP')
create_sase_object = sasetools.mgmt_group_to_sase(
    'cpapi_tools_group_csv_TEST_GROUP_hosts.csv','Antaeus_API_test',
    'Added by o_O Antaeus ')

# Retrieve a JSON object of all addresses
print(sase.get_all_addresses())

# Delete an address by ID
sase.delete_address('iCLYBw8Rfx')

# Overwrite an address object
sase.update_addresses('uC4g5gSn4R', name='Toaster',
                     valueType='list',
                     value=['10.44.44.44', '10.22.22.22'])