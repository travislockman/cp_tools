# Class Library containing tools to work with CP Quantum SASE.
# T. Lockman
# Last updated December 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

from CP_Q_SASE import CPQS
from cp_q_sase_utils import CPQSASEUTILS

class CPQSASETOOLS:
    def __init__(self, api_key):
        self.saseapi = CPQS(api_key)
        self.saseutils = CPQSASEUTILS(api_key)

    def mgmt_group_to_sase(self, csv_file, object_name, object_description,
                           object_type='list'):   
        ip_list = self.saseutils.build_address_list_from_csv(csv_file)

        self.saseapi.create_addresses(object_name,
                                description=object_description,
                                valueType=object_type,
                                value=ip_list)