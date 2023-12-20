# Class Library containing utilities to work with CP Quantum SASE.
# T. Lockman
# Last updated December 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

from CP_Q_SASE import CPQS
import csv

class CPQSASEUTILS:
    def __init__(self, api_key):
        self.api_key = api_key
        self.cpqs = CPQS(self.api_key)
        self.ip_list = []

    def build_address_list_from_csv(self, filename):
        with open(filename, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader, None)
            for row in csvreader:
                self.ip_list.append(row[1])
        return self.ip_list