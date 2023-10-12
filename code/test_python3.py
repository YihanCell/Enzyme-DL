from zeep import Client
import hashlib

wsdl = "https://www.brenda-enzymes.org/soap/brenda_zeep.wsdl"
password = hashlib.sha256("BcQLASvQufLLhm6".encode("utf-8")).hexdigest()
client = Client(wsdl)
parameters = ("Y.Chen323@liverpool.ac.uk", password, "ecNumber*1.1.1.1", "organism*Homo sapiens", "kmValue*",
              "kmValueMaximum*", "substrate*", "commentary*", "ligandStructureId*", "literature*")
resultString = client.service.getKmValue(*parameters)
print(resultString)

#%%
