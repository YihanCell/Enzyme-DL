#!/usr/bin/python
################################################################################
# Process from BRENDA Download
# 这段代码的主要目的是从多个BRENDA文件中提取特定的酶信息，并为每个EC号组织并保存这些信息。

################################################################################

# Author: Yihan CHEN
# This code should be run under the Python 2.7 environment

#INPUTS:
#1) Path in which all BRENDA queries are (from script retrieveBRENDA.py):
input_path = '../../Data/database/brenda_ec'
#2) Path in which you wish to store all EC files:
output_path = '../../Data/database/Kcat_brenda'

################################################################################

import os

def get_variable_name_from_filename(filename):
    """Extracts EC number and variable name from a given filename."""
    sep_pos = filename.find('_')
    ec_number = filename[:sep_pos]
    var_name = filename[sep_pos+1:-4]
    return ec_number, var_name

def get_variable_from_name(var_name):
    """Returns the variable string based on the variable name."""
    variables = {
        'KM': '#kmValue*',
        'MW': '#molecularWeight*',
        'PATH': '#pathway*',
        'SEQ': '#sequence*',
        'SA': '#specificActivity*',
        'KCAT': '#turnoverNumber*'
    }
    return variables.get(var_name)

# Initialize
prev_path = os.getcwd()
previous_ec_number = ''
ec_table = []

dir_files = sorted([f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))])

# Main loop: Adds each BRENDA file's info to the corresponding EC file.
for filename in dir_files:
    ec_number, var_name = get_variable_name_from_filename(filename)
    filepath = os.path.join(input_path, filename)

    with open(filepath, 'r') as file:
        data = file.read()

    if ec_number != previous_ec_number and previous_ec_number:
        output_filepath = os.path.join(output_path, previous_ec_number + '.txt')
        with open(output_filepath, 'w') as file:
            file.write("".join(ec_table))
        print(f'Successfully constructed {previous_ec_number} file.')
        ec_table = []

    variable = get_variable_from_name(var_name)
    options = data.split(variable)

    for option in options:
        value_end_pos = option.find('#')
        if value_end_pos != -1:
            k_value = option[:value_end_pos]

            # Continue processing data using your original code
            k_split = option.split('#substrate*')
            if len(k_split) == 1:
                k_substrate = '*'
            else:
                k_substrate = k_split[1][:k_split[1].find('#')]
                if not k_substrate:
                    k_substrate = '*'

            k_split2 = k_split[0].split('#commentary')
            if len(k_split2) == 1:
                k_comment = '*'
            else:
                k_comment = k_split2[1][:k_split2[1].find('#')]

            k_split = option.split('#organism*')
            if len(k_split) == 1:
                k_org = '*'
            else:
                k_org = k_split[1][:k_split[1].find('#')]
                if not k_org:
                    k_org = '*'

            # Append data to ec_table
            ec_table.append(var_name + '\t' + k_org + '\t' + k_value + '\t' + k_substrate + '\t' + k_comment + '\n')

    previous_ec_number = ec_number

# Handle the last EC number
output_filepath = os.path.join(output_path, previous_ec_number + '.txt')
with open(output_filepath, 'w') as file:
    file.write("".join(ec_table))
print(f'Successfully constructed {previous_ec_number} file.')