# Class Library containing various utils for Check Point Management.
# T. Lockman
# Last updated November 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

import csv

class CPQMGMTUTILS:
    def list_of_dict_to_csv(self, filename, list):
        """
        Takes a list of dictionaries and converts it to a CSV.
        Requires column titles.
        """
        columns = list[0].keys()
        with open(filename, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
            csv_writer.writeheader()
            csv_writer.writerows(list)