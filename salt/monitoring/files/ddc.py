import requests
import time
import xml.etree.ElementTree as ET
import requests.auth
from requests_ntlm import HttpNtlmAuth
import getpass
import sys
#use this for username\password

if (len(sys.argv) != 6):
    print "Usage: ddc.py username password ddchost warning critical"
    quit()

username = sys.argv[1]
password = sys.argv[2]
warning = int(sys.argv[4])
critical = int(sys.argv[5])

#xml namespaces
ns = {'default': "http://www.w3.org/2005/Atom",
    'base': "http://vdiddc-1/Citrix/Monitor/OData/v2/Data/",
    'd': "http://schemas.microsoft.com/ado/2007/08/dataservices",
    'm': "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"}

class DdcMonitor:
    def main(self):
    #opens the file with the list of DDCs
        ddcFile = []
        ddcFile.append(sys.argv[3])
        for ddcFQDN in ddcFile:
            #uses HTTP. HTTPS could be added if needed.
            directorURL = "http://" + ddcFQDN.rstrip("\n") + "/Citrix/Monitor/OData/v2/Data/FailureLogSummaries"
            #print("Now probing : " + str(directorURL))
            #Connection information
            #here is an example of a constructed query
            #directorURL = "http://192.168.0.112/Citrix/Monitor/OData/v2/Data/FailureLogSummaries"
            directorSession = requests.session()
            directorSession.auth = HttpNtlmAuth(username,password)
            directorReqData = directorSession.get(directorURL)

            #XML information
            root = ET.fromstring(directorReqData._content)
            entry = root.find('default:entry', ns)
            sub_1 = entry.find("default:content", ns)
            for sub_2 in sub_1.find("m:properties", ns):
                if "FailureCount" in str(sub_2.tag):
                        if int(sub_2.text) < warning:
                            print("OK: The Failure Count at " + directorURL + " is " + sub_2.text)
                            return 0
                        elif int(sub_2.text) > critical:
                            print("CRITICAL: The Failure Count at " + directorURL + " is " + sub_2.text)
                            return 2
                        elif (int(sub2.text) > warning): 
                            print("WARNING: The Failure Count at " + directorURL + " is " + sub_2.text)
                            return 1
                        else:
                            pass


DdcMonitor().main()
