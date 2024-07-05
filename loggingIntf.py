
import creds
import datetime
import mysql.connector

########################################
#
# Logs all the ids and deposit input 
#
########################################
class logger:
    x=datetime.datetime(2020,1,1).today()
    f="%Y-%m-%d %H:%M:%S"
    queryArk = "select ark from autodeposits where pubId = '{param}'"
    queryStatus = "select status from autodeposits where pubId = '{param}'"
    insertArk = "insert into autodeposits (pubId, ark, lastSent, status) values('{param1}','{param2}','{param3}',1)"
    updatedep = "update autodeposits set deposit='{param1}',status=2,lastSent='{param2}' where pubId='{param3}'"
    updateres = "update autodeposits set result='{param1}',status=3,lastSent='{param2}' where pubId='{param3}'"
    updateurl = "update autodeposits set url='{param1}' where pubId='{param2}'"


    def __init__(self):
        print("connect to DB here")

        self.cnxn = mysql.connector.connect(user=creds.loggingDb.username, 
                              password=creds.loggingDb.password,
                              host=creds.loggingDb.server,
                              database=creds.loggingDb.database,
                              port=creds.loggingDb.port)

        self.cursor = self.cnxn.cursor()


    def getArk(self, pubId):
        #print("read ark for this pubId")
        query = self.queryArk.format(param=pubId)
        #self.cursor.execute(self.queryArk,(str(pubId)))
        self.cursor.execute(query)
        ark = None
        for row in self.cursor:
            ark = row[0]

        return ark

    def getStatus(self, pubId):
        #print("read status for this pubId")
        query = self.queryStatus.format(param=pubId)
        self.cursor.execute(query)

        status = None
        for row in self.cursor:
            status = row[0]

        return status

    def saveArk(self, pubId, ark):
        #print("save ark for this pubId")
        lastSent = self.x.strftime(self.f)
        query = self.insertArk.format(param1=pubId, param2=ark, param3=lastSent)
        self.cursor.execute(query)
        self.cnxn.commit()

    def saveDepInput(self, pubId, input):
        #print("save input for this pubId")
        lastSent = self.x.strftime(self.f)
        query = self.updatedep.format(param1=input, param2=lastSent, param3=pubId)
        self.cursor.execute(query)
        self.cnxn.commit()

    def saveResult(self, pubId, result):
        print("save result for this pubId")
        lastSent = self.x.strftime(self.f)
        query = self.updateres.format(param1=result, param2=lastSent, param3=pubId)
        self.cursor.execute(query)
        self.cnxn.commit()


    def saveUrl(self, pubId, url):
        #print("save url for this pubId")
        query = self.updateurl.format(param1=url, param2=pubId)
        self.cursor.execute(query)
        self.cnxn.commit()
