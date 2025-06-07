import hashlib
import time
import os
import urllib3 

from deutschland import dip_bundestag
from pprint import pprint


from deutschland.dip_bundestag.api.plenarprotokolle_api import PlenarprotokolleApi


def md5hash(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class BTP_XML_Crawler:

    def __init__(self, api_key=None):
        super(BTP_XML_Crawler, self)
        if api_key is None:
            # Public API key, valid through 5/2026
            api_key = 'OSOegLs.PR2lwJ1dwCeje9vTj7FPOt3hvpYKtwKkhw'

        self.configuration = dip_bundestag.Configuration(
            host = "https://search.dip.bundestag.de/api/v1"
        )
        self.configuration.api_key['ApiKeyHeader'] = api_key
        self.configuration.api_key['ApiKeyQuery'] = api_key



    def __iter__(self):
        http = urllib3.PoolManager()
        with dip_bundestag.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            api_instance = PlenarprotokolleApi(api_client)
            id = 1 # int | 
            format = "json" # str | Steuert das Datenformat der Antwort, möglich sind JSON (voreingestellt) oder XML. (optional) (default to "json")

            cursor = None
            try:
                # Liefert Metadaten zu einer Aktivität
                while True:
                    if cursor:
                        api_response = api_instance.get_plenarprotokoll_list(cursor = cursor)
                    else:
                        api_response = api_instance.get_plenarprotokoll_list()
                
                    for d in api_response.documents:
                        if 'xml_url' in d.fundstelle:
                            url = d.fundstelle.xml_url
                            dir = os.path.join("data", *url.split('/')[-2:-1])
                            file = os.path.join("data", *url.split('/')[-2:])
                            os.makedirs(dir, exist_ok=True)
                            if not os.path.exists(file) or d.xml_hash != md5hash(file):
                                response = http.request("GET", url)
                                if response.status != 200:
                                    print(f"error downloading %s", url)
                                
                                out = open(file, "wb")
                                out.write(response.data)
                                out.close()
                            yield file
                    
                    if cursor == api_response.cursor:
                        break
                    cursor = api_response.cursor
                    
            except dip_bundestag.ApiException as e:        
                print("Exception when calling PlenarprotokolleApi->get_plenarprotokoll_list: %s\n" % e)

if __name__ == "__main__":
    for u in BTP_XML_Crawler():
        print(u)

