import pyodbc
import creds

########################################
#
# Connects to Elements reporting DB
# provides functionality to query for ID
# and related information
#
########################################
class reportingdb:

    def __init__(self):
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+creds.repDb.server+';DATABASE='+creds.repDb.database+';UID='+creds.repDb.username+';PWD='+ creds.repDb.password + ';TrustServerCertificate=yes;')
        self.cursor = self.cnxn.cursor()


    def getAllPubIds(self, query):
        print("get the publication ids")
        self.cursor.execute(query)
        puburl = {}
        pubmedid = {}
        for row in self.cursor:
            puburl[row[0]] = row[1]
            pubmedid[row[0]] = row[2]
        return puburl, pubmedid

    def getPubMeta(self, query):
        print("get the publication ids")
        self.cursor.execute(query)
        pubmeta = {}
        for row in self.cursor:
            pubmeta[row[0]] = (row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12])

        return pubmeta;

    def getUserInfo(self, query, pubuser, userdept):
        print("get the user/publication ids and metadata")
        #print(query)
        self.cursor.execute(query)
        userinfo = {}
        for row in self.cursor:
            if row[0] not in pubuser:
                pubuser[row[0]] = [row[1]]
            else:
                pubuser[row[0]].append(row[1])

            if row[1] not in userdept and row[7] != 1:
                userdept[row[1]] = row[7]

            if row[1] not in userinfo:
                userinfo[row[1]] = (row[2],row[3],row[4],row[5],row[6])

        return userinfo;


    def getGrantInfo(self, query, pubgrant):
        print("get the grant/pub ids and metadata")
        self.cursor.execute(query)
        grantinfo = {}
        for row in self.cursor:
            if row[0] not in pubgrant:
                pubgrant[row[0]] = [row[1]]
            else:
                pubgrant[row[0]].append(row[1])

            if row[1] not in grantinfo:
                grantinfo[row[1]] = (row[2],row[3])

        return grantinfo;

    #peoplePath
    def getPeople(self, query):
        print("get the people for a publication")
        self.cursor.execute(query)
        peopleinfo = {}
        for row in self.cursor:
            item = (row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            if row[0] not in peopleinfo:
                peopleinfo[row[0]] = []

            peopleinfo[row[0]].append(item)

        return peopleinfo;
