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

add_star = cp.add_vpn_community_star(env['star_name'],
                                    center_gateways=[env['star_gateway_center']],
                                    satellite_gateways=[env['star_gateway_satellite']],
                                    encryption_method=env['star_encryption_method'],
                                    ike_phase_1={
                                    "data-integrity" : env['star_encryption_ike_phase_1_data_integrity'],
                                    "encryption-algorithm" : env['star_encryption_ike_phase_1_algo'],
                                    "diffie-hellman-group" : env['star_encryption_ike_phase_1_diffie_helman'],
                                    },
                                    ike_phase_2={
                                    "data-integrity" : env['star_encryption_ike_phase_2_data_integrity'],
                                    "encryption-algorithm" : env['star_encryption_ike_phase_2_algo'],
                                    "ike-p2-pfs-dh-grp" : env['star_encryption_ike_phase_1_diffie_helman'],
                                    "ike-p2-use-pfs" : env['star_encryption_ike_phase_2_perfect_forward_secrecy'] 
                                    },
                                    use_shared_secret=env['star_use_shared_secret'],
                                    shared_secrets=[{
                                    "external-gateway" : env['star_shared_secret_gateway'],
                                    "shared-secret" : env['star_shared_secret']
                                    }])

print(f'RESULT IS: {add_star}')
time.sleep(3)
print(f'PUBLISH:\n{cp.publish()}')
cp.logout()
