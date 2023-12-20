# Simple Env Program Using CSV
# T. Lockman
# Last updated December 2023
# O_o tHe pAcKeTs nEvEr LiE o_O #

import csv

class CSVENV:

    def read_csv(file_name):
        # Dictionary to store the data
        data = {}

        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file, delimiter=',')  # assuming tab-delimited file
            for row in reader:
                # Assuming 'name' is the key and 'secret' is the value
                data[row['name']] = row['secret']
        
        return data

if __name__ == '__main__':

    # Usage
    file_name = 'env.csv'  # Replace with your CSV file name
    parsed_data = CSVENV.read_csv(file_name)