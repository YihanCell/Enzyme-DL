#!/usr/bin/python

################################################################################

# retrieveBRENDA
# Acces the web client and retrieves all EC data from BRENDA. Creates files with
# BRENDA output for all organisms and EC numbers for which there is data.

################################################################################

# Author: Yihan CHEN

# Main script
output_path = "../data_download/raw_data"  # Change this to your desired output path
email = "Y.Chen323@liverpool.ac.uk"  # Change this to your BRENDA account email
password = "BcQLASvQufLLhm6"  # Change this to your BRENDA account password

# Information to retrieve: km, M.W., pathway, sequence, specific activity and kcat.
# fields = ['KM','MW','PATH','SA','KCAT']
fields = ['KCAT']  # Update this if you want other fields

# Last EC number processed (if the program was interrupted), e.g. '1.2.3.4'.
last_EC = ''  # Last EC number queried. Can be updated if needed.

################################################################################

import os
import hashlib
import time
from zeep import Client

class BrendaClient:
    def __init__(self, email, password):
        self.wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
        self.client = Client(self.wsdl)
        self.credentials = (email, hashlib.sha256(password.encode("utf-8")).hexdigest())

    # Generate the query for search
    def _make_query(self, ECnumber):
        return (
            *self.credentials,
            'ecNumber*' + ECnumber,
            'organism*',
            'turnoverNumber*',
            'turnoverNumberMaximum*',
            'substrate*',
            'commentary*',
            'ligandStructureId*',
            'literature*'
        )

# Fetch the related data
    def fetch_data(self, field, ECnumber):
        query = self._make_query(ECnumber)
        if field == 'KM':
            return self.client.service.getKmValue(*query)
        elif field == 'MW':
            return self.client.service.getMolecularWeight(*query)
        elif field == 'PATH':
            return self.client.service.getPathway(*query)
        elif field == 'SEQ':
            return self.client.service.getSequence(*query)
        elif field == 'SA':
            return self.client.service.getSpecificActivity(*query)
        elif field == 'KCAT':
            return self.client.service.getTurnoverNumber(*query)
        else:
            return None

    # Get the ec number had the related data
    def get_ec_numbers(self, field):
        if field == 'KM':
            return self.client.service.getEcNumbersFromKmValue(*self.credentials)
        elif field == 'MW':
            return self.client.service.getEcNumbersFromMolecularWeight(*self.credentials)
        elif field == 'PATH':
            return self.client.service.getEcNumbersFromPathway(*self.credentials)
        elif field == 'SEQ':
            return self.client.service.getEcNumbersFromSequence(*self.credentials)
        elif field == 'SA':
            return self.client.service.getEcNumbersFromSpecificActivity(*self.credentials)
        elif field == 'KCAT':
            return self.client.service.getEcNumbersFromTurnoverNumber(*self.credentials)
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
                    fid.write(data)

        time.sleep(1)  # delay to avoid overloading the server

client = BrendaClient(email, password)

prev_path = os.getcwd()
os.chdir(output_path)

for field in fields:
    extract_field(client, field, last_EC)

os.chdir(prev_path)
