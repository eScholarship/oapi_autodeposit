import creds
import sys
import traceback
from urllib import request
from urllib import error
import json
import time
########################################
#
# Interfaces with escholarship graphQL 
#
########################################
class graphClient:
    def __init__(self, ep):
        self.endpoint = ep
        self.headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'Privileged':creds.eschol.privKey
                   }
        if creds.eschol.cookie:
            self.headers['Cookie'] = creds.eschol.cookie

    def execute(self, query):
        return self._send(query)

    def _send(self, query):
        data = {'query': query}
        time.sleep(10)
        req = request.Request(self.endpoint, json.dumps(data).encode('utf-8'), self.headers)
        try:
            response = request.urlopen(req, timeout=1800)
            return response.read().decode('utf-8')
        except error.HTTPError as e:
            print(e.read())
            print(e.msg)
            raise e


########################################
#
# Uses escholClient to connect with eschol
# Provides functionality for id minting and deposit 
#
########################################
class eschol:
    """Interface to connect to eschol"""

    mintMutation = '''
                mutation{
                    mintProvisionalID(input:{sourceName: "oa_harvester", sourceID: "PUB_ID" })
                    {
                    id
                    }
                }
                '''


    depositMutation = '''
            mutation{
              depositItem(input:{DEP_INPUT})
              {
                id
                message
              }
            }
            '''

    def __init__(self):
        self.client = graphClient(creds.eschol.url)


    def testConnection(self):
        try:
            result = self.client.execute('''
            mutation{
              mintProvisionalID(input:{sourceName: "oa_harvester", sourceID: "18" })
              {
                id
              }
            }
            ''')

            print(result)
            res = json.loads(result)

            return res['data']['mintProvisionalID']['id']
        except error.HTTPError as e:
            print(e.read())
        except: 
            print("Exception Info")
            print(str(sys.exc_info()[1]))
            print(traceback.format_exc())
            raise 


    def createItem(self, pubId):
        mintquery = self.mintMutation.replace("PUB_ID",str(pubId))
        try:
           result = self.client.execute(mintquery)

           print(result)
           res = json.loads(result)

           return res['data']['mintProvisionalID']['id']
        except: 
            print("Exception Info")
            print(str(sys.exc_info()[1]))
            print(traceback.format_exc())
            raise

    def depositItem(self, depositInput):
        depositquery = self.depositMutation.replace("DEP_INPUT",depositInput)
        try:
           result = self.client.execute(depositquery)

           print(result)
           #return just the id
           return result
        except: 
            print("Exception Info")
            print(str(sys.exc_info()[1]))
            print(traceback.format_exc())
            raise


