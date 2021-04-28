########################################
#
#   Controller manages information obtained
#   from reporting DB and formats it for
#   graphql API input
#
########################################
from creds import queryfiles
from reportingdbIntf import reportingdb
from loggingIntf import logger
from escholIntf import eschol
from escholDBIntf import escholDB
import depositFields

class repQueries:

    def __init__(self):
        queryf = open(queryfiles.pubIdPath, "r")
        self.pubIdquery = queryf.read()

        queryf = open(queryfiles.idByPgdPath, "r")
        self.idByPgdquery = queryf.read()

        queryf = open(queryfiles.pubMetaPath, "r")
        self.pubMetaquery = queryf.read()

        queryf = open(queryfiles.userPath, "r")
        self.userquery = queryf.read()

        queryf = open(queryfiles.grantPath, "r")
        self.grantquery = queryf.read()

        queryf = open(queryfiles.peoplePath, "r")
        self.peoplequery = queryf.read()

        queryf = open(queryfiles.tempPath, "r")
        self.tempquery = queryf.read()




class controller:
    BatchSize = 100
    def __init__(self):
        self.repq = repQueries()

        self.curstart = 0
        self.curend = 0
        self.pubIdCount = 0
        self.depositCount = 0

        self.repDB = reportingdb()
        self.escholQ = eschol()
        self.log = logger()

        # these two are for all the publications
        self.pub_urldict = {}
        self.allpubIds = {}

        # these are for the current set
        self.pub_metadict = {}
        self.pub_userdict = {}
        self.user_deptdict = {}
        self.user_infodict = {}
        self.pub_grantdict = {}
        self.grant_infodict = {}
        self.pub_arkdict = {}
        self.pub_depInputdict = {}
        self.pub_peopledict = {}
        self.curset = []

    def getEscholSeries(self):
        print("Start: getEscholSeries")
        db = escholDB()
        self.groupToSeries = db.getUnits()
        print(self.groupToSeries)
        groups=list(self.groupToSeries.keys())
        groupIds = ""
        for x in self.groupToSeries:
            groupIds += x + ','
        groupIds += "1"
        self.userquery = self.repq.userquery.replace("GROUP_IDs",groupIds)
        print("End: getEscholSeries")

    def performDeposits(self):
        print("Start: performDeposits")
        self.getEscholSeries()
        self.getAllPubIds()
        endIndex = len(self.allpubIds)
        print("pubIds retrieved: " + str(endIndex))
        while self.curend < endIndex:
            self.curstart = self.curend
            self.curend = self.curstart + self.BatchSize
            if self.curend > endIndex:
                self.curend = endIndex
            self.curset = self.allpubIds[self.curstart: self.curend]
            pubIds = ",".join(map(str, self.curset))
            self.getPubMeta(pubIds)
            self.getUserInfo(pubIds)
            self.getGrantInfo(pubIds)
            self.getPeople(pubIds)
            self.processCurrentBatch()
        print("End: performDeposits")

    def getAllPubIds(self):
        print("Start: getAllPubIds")
        self.pub_urldict = self.repDB.getAllPubIds(self.repq.pubIdquery)
        #self.pub_urldict = self.repDB.getAllPubIds(self.repq.idByPgdquery)
        #self.pub_urldict = self.repDB.getAllPubIds(self.repq.tempquery)
        self.allpubIds = list(self.pub_urldict.keys())
        print("End: getAllPubIds")

    def getPubMeta(self, pubIds):
        print("Start: getPubMeta")
        query = self.repq.pubMetaquery.replace("PUB_IDs",pubIds)
        self.pub_metadict = self.repDB.getPubMeta(query)
        print("End: getPubMeta")

    def getUserInfo(self, pubIds):
        print("Start: getUserInfo")
        # use the query with group ids filled in
        query = self.userquery.replace("PUB_IDs",pubIds)
        self.pub_userdict = {}
        self.user_deptdict = {}
        self.user_infodict = self.repDB.getUserInfo(query, self.pub_userdict, self.user_deptdict)
        print("End: getUserInfo")

    def getGrantInfo(self, pubIds):
        print("Start: getGrantInfo")
        query = self.repq.grantquery.replace("PUB_IDs",pubIds)
        self.pub_grantdict = {}
        self.grant_infodict = self.repDB.getGrantInfo(query,self.pub_grantdict)
        print("End: getGrantInfo")

    def getPeople(self, pubIds):
        print("Start: getPeople")
        query = self.repq.peoplequery.replace("PUB_IDs",pubIds)
        self.pub_peopledict = self.repDB.getPeople(query)
        print("End: getPeople")

    def processCurrentBatch(self):
        print("Start: processCurrentBatch")
        self.pub_arkdict = {}
        self.pub_depInputdict = {}
        # for each create id and save in dictionary
        for x in self.pub_metadict:
            self.pub_arkdict[x] = self.createIdIfNeeded(x)
            self.log.saveUrl(x, self.pub_urldict[x])

        # some of the publications may not qualify for autodeposit
        # based on metadata - such as ones missing pubdate
        # so use the metadata dict to determine what to deposit
        for x in self.pub_metadict:
            s = self.log.getStatus(x)
            if s != 3:
                self.pub_depInputdict[x] = self.buildDepositInput(x)
                self.log.saveDepInput(x, self.pub_depInputdict[x])
                res = self.escholQ.depositItem(self.pub_depInputdict[x])
                self.log.saveResult(x, res)
                self.depositCount += 1
        print("End: processCurrentBatch")

    def createIdIfNeeded(self, pubId):
        ark = self.log.getArk(pubId)
        if ark is None:
            ark = self.escholQ.createItem(pubId)
            self.log.saveArk(pubId, ark)
        return ark

    def buildDepositInput(self, pubId):
        print("build the deposit input")
        meta = self.pub_metadict[pubId]
        isFunding = pubId in self.pub_grantdict
        outstr = ''
        isAfterRgpoCutoff = meta[8] and str(meta[8]) > '2017-01-08' and isFunding

        outstr += depositFields.sourceInfo(pubId).outstr + ','
        outstr += depositFields.content(self.pub_arkdict[pubId], self.pub_urldict[pubId]).outstr + ','
        if meta[0]:
            outstr += depositFields.abstract(meta[0]).outstr + ','
        if meta[3]:
            outstr += depositFields.title(meta[3]).outstr + ','
        if meta[8]:
            outstr += depositFields.pubdate(str(meta[8])).outstr + ','
        if meta[2]:
            outstr += depositFields.journal(meta[2]).outstr + ','
        if meta[7]:
            outstr += depositFields.keywords(meta[7]).outstr + ','
        
        outstr += depositFields.identity(meta[4], pubId).outstr + ','
        outstr += depositFields.journalMeta(meta[5],meta[6],meta[10]).outstr + ','

        if isFunding is True:
            outstr += depositFields.grants(self.pub_grantdict[pubId], self.grant_infodict).outstr + ','

        # get author list for the pub. 
        if pubId in self.pub_peopledict:
            outstr += depositFields.authors(self.pub_peopledict[pubId]).outstr + ','
 
        # use pdg and then department if avaiable  
        outstr += depositFields.units(self.pub_userdict[pubId], self.user_infodict, self.user_deptdict, self.groupToSeries, isAfterRgpoCutoff).outstr + ','
        
        outstr = outstr.replace(",,",",")[:-1]
     
        print(outstr)
        return outstr
