# Example usages of my Check Point Quantum Management Libraries
# T. Lockman
# Last updated December 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

from CP_Q_MGMT import CPQMGMT
from cp_q_mgmt_tools import CPQMGMTTOOLS
from csv_env import CSVENV # Remove this if you have your own env

'''
Environment variables so you don't see my unmentionables.
You can remove this whole section and put your own envs in.
'''
file_name = 'env.csv'  # Replace with your CSV file name
env_vars = CSVENV.read_csv(file_name)
smart1_manager = env_vars['smart1_manager'] # Add your own env variable here.
smart1_api_key = env_vars['smart1_api_key'] # Add your own env variable here.

# Assigning classes
cp = CPQMGMT(smart1_manager, smart1_api_key)
cptools = CPQMGMTTOOLS(smart1_manager, smart1_api_key)

# Parse a group name in a CP manager and break it into CSVs
group_json = cptools.group_to_csv('TEST_GROUP')

# Testing a bunch of the API functions
print(cp.show_packages())
print(cp.show_group('Admin_machines', details_level='full'))
print(cp.show_groups())
print(cp.show_nat_rulebase('AntaeusLab_ESXi_Main'))
print(cp.show_simple_gateways())
print(cp.generic_object_query('AntaeusLab_ESXi_External', details_level='full'))

# Adding a host and publishing
print(cp.add_host('PoopTaco7', '10.10.33.37'))
print(cp.publish())

# Shows unused objects in the manager
print(cp.show_unused_objects())

# Showing details for a specific task
print(cp.show_task('41e821a0-3720-11e3-aa6e-0800200c9fde', details_level='full'))

# Logging out
print(cp.logout())