
import creds
import mysql.connector

########################################
#
# Gets the series, group info from eschol DB 
#
########################################
class escholDB:
    queryUnits = "SELECT attrs->>'$.elements_id', id elements_id FROM units WHERE attrs->>'$.elements_id' is not null"


    def __init__(self):
        print("connect to eschol DB here")

        self.cnxn = mysql.connector.connect(user=creds.escholDB.username, 
                              password=creds.escholDB.password,
                              host=creds.escholDB.server,
                              database=creds.escholDB.database,
                              port=creds.escholDB.port,
                              auth_plugin='mysql_native_password')

        self.cursor = self.cnxn.cursor()


    def getUnits(self):
        print("read all the Elements related groups")
        self.cursor.execute(self.queryUnits)
        groupSeries = {}
        for row in self.cursor:
            groupSeries[str(row[0],'utf-8')] = row[1]

        return groupSeries

