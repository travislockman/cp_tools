import json
import time
from CP_Q_MGMT import CPQMGMT
from csv_env import CSVENV  # Remove this if you have your own env

# SETTING UP THE ENVIRONMENT #
'''
Environment variables so you don't see my unmentionables.
You can remove this whole section and put your own envs in.
'''
file_name = 'env.csv'  # Replace with your CSV file name
env = CSVENV.read_csv(file_name)
smart1_manager = env['smart1_manager']  # Add your own env variable here.
smart1_api_key = env['smart1_api_key']  # Add your own env variable here.

# SETTING UP THE CONSTRUCTOR
cp = CPQMGMT(smart1_manager, smart1_api_key)

add_interop = cp.add_interoperable_device(env['interop_name'],
                                          env['interop_ip'],
                                          env['interop_domain_type'], 
                                          env['interop_domain_name'])
time.sleep(3)
print(f'PUBLISH:\n{cp.publish()}')
cp.logout()