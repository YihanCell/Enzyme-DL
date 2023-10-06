#!/usr/bin/python

################################################################################

# retrieveBRENDA
# Acces the web client and retrieves all EC data from BRENDA. Creates files with
# BRENDA output for all organisms and EC numbers for which there is data.

################################################################################

# Updated by:
# Author: Yihan CHEN
# This code should be run under the Python 2.7 environment because of the usage of SOAP.

# Main script
output_path = "./data_download/raw_data"  # Change this to your desired output path
email = "Y.Chen323@liverpool.ac.uk"  # Change this to your BRENDA account email
password = "BcQLASvQufLLhm6"  # Change this to your BRENDA account password

################################################################################

import os
import string
import hashlib
import time
from SOAPpy import SOAPProxy

class BrendaClient:
    def __init__(self, email, password):
        self.endpointURL = "https://www.brenda-enzymes.org/soap/brenda_server.php"
        self.client = SOAPProxy(self.endpointURL)
        self.credentials = email + ',' + hashlib.sha256(password).hexdigest()

    # Generate the query for search
    def _make_query(self, ECnumber):
        return self.credentials + ',ecNumber*' + ECnumber + '#organism*'

    # Fetch the related data
    def fetch_data(self, field, ECnumber):
        query = self._make_query(ECnumber)
        if field == 'KM':
            return self.client.getKmValue(query)
        elif field == 'MW':
            return self.client.getMolecularWeight(query)
        elif field == 'PATH':
            return self.client.getPathway(query)
        elif field == 'SEQ':
            return self.client.getSequence(query)
        elif field == 'SA':
            return self.client.getSpecificActivity(query)
        elif field == 'KCAT':
            return self.client.getTurnoverNumber(query)
        else:
            return None

    # Get the ec number had the related data
    def get_ec_numbers(self, field):
        if field == 'KM':
            return self.client.getEcNumbersFromKmValue(self.credentials)
        elif field == 'MW':
            return self.client.getEcNumbersFromMolecularWeight(self.credentials)
        elif field == 'PATH':
            return self.client.getEcNumbersFromPathway(self.credentials)
        elif field == 'SEQ':
            return self.client.getEcNumbersFromSequence(self.credentials)
        elif field == 'SA':
            return self.client.getEcNumbersFromSpecificActivity(self.credentials)
        elif field == 'KCAT':
            return self.client.getEcNumbersFromTurnoverNumber(self.credentials)
        else:
            return None


def extract_field(client, field, last):
    ECstring = client.get_ec_numbers(field)
    EClist = ECstring.split('!')

    start = False
    for ECnumber in EClist:
        if not start and (ECnumber == last or not last):
            start = True

        if start:
            data = client.fetch_data(field, ECnumber)
            if data:
                file_name = 'EC' + ECnumber + '_' + field
                with open(file_name + '.txt', 'w') as fid:
                    fid.write(data.decode('ascii', 'ignore'))

        time.sleep(1)  # delay to avoid overloading the server


prev_path = os.getcwd()
os.chdir(output_path)

client = BrendaClient(email, password)

# Information to retrieve: km, M.W., pathway, sequence, specific activity and kcat.
# fields = ['KM','MW','PATH','SA','KCAT']
fields = ['KCAT']  # Update this if you want other fields

# Last EC number processed (if the program was interrupted), e.g. '1.2.3.4'.
last_EC = ''  # Last EC number queried. Can be updated if needed.

for field in fields:
    extract_field(client, field, last_EC)

os.chdir(prev_path)