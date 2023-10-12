import hashlib
from SOAPpy import SOAPProxy

endpointURL = "https://www.brenda-enzymes.org/soap/brenda_server.php"
password = hashlib.sha256("BcQLASvQufLLhm6").hexdigest()
parameters = "Y.Chen323@liverpool.ac.uk,"+password+",ecNumber*1.1.1.1#organism*Homo sapiens#"
client = SOAPProxy(endpointURL)
resultString = client.getKmValue(parameters)
print resultString

#%%
