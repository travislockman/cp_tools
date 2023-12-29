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
            reader = csv.DictReader(file, delimiter=',')  # assuming comma-delimited file
            for row in reader:
                # Assigning variables
                k =row['key']
                v = row['value']
                t = row['type']
                # Boolean Conversion
                if t == 'bool':
                    if v.lower() == 'true':
                        v = True
                    else:
                        v = False
                # Integer Conversion
                elif t == 'int':
                    try:
                        v = int(v)
                    except ValueError:
                        print('Check the CSV field, I dont think this is int')
                        exit()
                
                # Store the key, value pair into the dictionary
                data[k] = v
        
        return data

    def edit_csv(file_path, target_key, new_value):
        # Read the CSV file and store the data
        rows = []
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')  # assuming comma-delimited file
            for row in reader:
                # Check if this row contains the target key
                if row['key'] == target_key:
                    row['value'] = new_value
                rows.append(row)

        # Write the updated data back to the CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['key', 'value', 'type'])
            writer.writeheader()
            writer.writerows(rows)

if __name__ == '__main__':

    # Usage
    file_name = 'env.csv'  # Replace with your CSV file name
    parsed_data = CSVENV.read_csv(file_name)