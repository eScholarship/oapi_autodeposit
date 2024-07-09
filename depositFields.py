########################################
#
#   Process metadata and format for API
#   determine units based on authors
#   claimed list
#
########################################

import os
import re
from urllib.parse import urlparse


########################################
#
# Constant info in deposits plus pubId 
#
########################################
class sourceInfo:
    #sourceName: "oa_harvester", sourceID: "1801972", submitterEmail: "auto@EuroPMC.uc", type: ARTICLE, isPeerReviewed: true
    #ucpmsPubType:"journal-article",
    baseStr = "sourceName: \"oa_harvester\", sourceID: \"{param}\", submitterEmail: \"auto@EuroPMC.uc\", type: ARTICLE, isPeerReviewed: true"
    def __init__(self, pubId):
        self.outstr = self.baseStr.format(param = pubId )

########################################
#
# Provides publically available url for escholarship to download 
#
########################################
class content:
    #contentLink: "https://europepmc.org/articles/PMC5234440?pdf=render",id: "ark:/13030/qtttsk9dh5", contentFileName:"PMC5234440.pdf"
    baseStr = "contentLink: \"{param1}\",id: \"{param2}\", contentFileName:\"{param3}\", ucpmsPubType:\"journal-article\""
    def __init__(self, arkId, url):
        a = urlparse(url)
        filename = os.path.basename(a.path) + '.pdf'
        self.outstr = self.baseStr.format(param1 = url, param2 = arkId, param3 = filename )

########################################
#
# Add abstract, process to make it suitable for DB entry 
#
########################################
class abstract:
    #abstract:"INTRODUCTION: Although evidence-based"
    baseStr = "abstract:\"{param}\""
    def __init__(self, abs):
        self.outstr = self.baseStr.format(param = abs.replace("'","").replace("\"",""))

########################################
#
# title from Elements for deposit 
#
########################################
class title:
    #title:"Using School Staff Members to Implement"
    baseStr = "title:\"{param}\""
    def __init__(self, name):
        self.outstr = self.baseStr.format(param = name.replace("'","").replace("\"",""))

########################################
#
# Note - this needs to be revisited when Elements upgrades 
#
########################################
class pubdate:
    #published: "2017-01-12"
    baseStr = "published:\"{param}\""
    def __init__(self, date):
        if date and len(date) == 10:
            #str = date[0:4] + "-" + date[4:6] + "-" + date[6:8]
            self.outstr = self.baseStr.format(param = date )
        else:
            self.outstr = ""

########################################
#
# includes journel info 
#
########################################
class journal:
    #journal:"Prev Chronic Dis"
    baseStr = "journal:\"{param}\""
    def __init__(self, name):
        self.outstr = self.baseStr.format(param = name.replace("'","").replace("\"","") )

########################################
#
# Adds DOI and Elements Pub Id 
#
########################################
class identity:
    #localIDs:[{id:"10.5888/pcd14.160381",scheme:DOI},{id:"1801972",scheme:OA_PUB_ID}],
    baseStr1 = "id:\"{param}\",scheme:OA_PUB_ID"
    baseStr2 = "id:\"{param}\",scheme:DOI"
    baseStr = "localIDs:[{param}]"
    def __init__(self, doi, pubId):
        idstr = '{' + self.baseStr1.format(param = pubId) + '}'
        if doi and len(doi) > 0:
            idstr += ',' + '{' +self.baseStr2.format(param = doi) + '}'
        self.outstr = self.baseStr.format(param = idstr)

########################################
#
# include additial journal metadata if present 
#
########################################
class journalMeta:
    #volume:"14", issue:"", issn:""
    def __init__(self, issn, issue, volume):
        self.outstr = ""
        if issn:
            self.outstr += "issn:\"{param}\", ".format(param=issn)
        if volume:
            self.outstr += "volume:\"{param}\", ".format(param=volume)
        if issue:
            self.outstr += "issue:\"{param}\", ".format(param=issue)
        self.outstr = self.outstr[:-1]


########################################
#
# Include grant info if linked 
#
########################################
class grants:
    #grants: [{name:'funder-name', reference:'funder-ref'}]
    baseStr = "name:\"{param1}\", reference:\"{param2}\""
    baseStr2 = "grants: [{param}]"
    def __init__(self, grants, grantInfo):
        self.outstr = ""
        for g in grants:
            if grantInfo[g][0] and grantInfo[g][1]:
                self.outstr += '{' + self.baseStr.format(param1 = grantInfo[g][0].replace("'",""), param2 = grantInfo[g][1].replace("'","")) + '},'

        self.outstr = self.outstr[:-1]
        if len(self.outstr) > 1:
            self.outstr = self.baseStr2.format(param = self.outstr)

########################################
#
# Provide a list of keyword terms applicable to publication 
#
########################################
class keywords:   
    baseStr = "keywords:[{param}]"
    baseStr2 = "\"{param}\","
    def __init__(self, names):
        words = names.replace('\r','').replace('\n','').replace("'","").replace("\"","").split(", ")
        self.outstr = ''
        for w in words:
            self.outstr += self.baseStr2.format(param = w)
        self.outstr = self.baseStr.format(param = self.outstr[:-1] )

########################################
#
# Use the people infomation associated with publication
# record and include email address if user is resolved to
# a user in Elements 
#
########################################
class authors:
    #authors:[{nameParts:{fname:"RE",lname:"Blaine"}},
    baseStr = "authors:[{param}]"
    def __init__(self, people):
        items = []
        self.outstr = ""

        # in case publication records are merged on Elements side, 
        # take one set of authors
        # the author list from query is sorted by order
        lastorder = -1
        for p in people:
            if p[0] != lastorder:
                items.append(user(p))
            lastorder = p[0]

        for i in items:
            self.outstr += i.outstr

        self.outstr = self.outstr[:-1]
        self.outstr = self.baseStr.format(param=self.outstr)

########################################
#
# Prepare input for one author 
#
########################################
class user:
    #{nameParts:{fname:"RE",lname:"Blaine"}}
    # depositFields.authors(meta[1], self.pub_userdict[pubId], self.user_infodict)
    nameparts = "fname:\"{param1}\",lname:\"{param2}\""
    baseStr1 = "nameParts:{param}"
    baseStr2 = "nameParts:{param1}, email:\"{param2}\""
    def __init__(self, person):
        self.outstr = ""
        if person[3]:
            fname = person[5]
            lname = person[6]
        else:
            fname = person[1]
            lname = person[2]

        if fname and lname:
            name = '{' + self.nameparts.format(param1=fname.replace("'","").replace("\"",""), param2=lname.replace("'","").replace("\"","")) + '}'
            if person[4]:
                self.outstr = '{' + self.baseStr2.format(param1 = name, param2 = person[4].replace("'","").replace("\"","")) + '},'
            else:
                self.outstr = '{' + self.baseStr1.format(param = name) + '},'

########################################
#
# Determine all the unit/series the publication should be placed
# based on group association of authors who claimed 
#
########################################
class units:
    # (self.pub_userdict[pubId], self.user_infodict, self.user_deptdict)
    #units: ["uci_postprints"]
    baseStr = "units:[{param}]"
    baseStr2 = "\"{param}\","
    campuses = ['ucb','ucd','uci','ucm','ucr','ucsb','ucsc','ucsd','ucsf','ucla']
    rgpo = ['cbcrp','chrp','trdrp','ucri']
    rgposeries = ['cbcrp_rw','chrp_rw','trdrp_rw','ucri_rw']
    def __init__(self, userslist, userinfodict, userdepdict, groupToUnit, isFunded, grants, grantInfo):
        self.outstr = ""
        pdgs = []
        series = []
        for userids in userslist:
            if userinfodict[userids][4] not in pdgs:
                pdgs.append(userinfodict[userids][4])

        #add campus postprints as needed
        for pdg in pdgs:                    
            for campus in self.campuses:
                if campus in pdg:
                    series.append(campus + '_postprints') 
        #add lbl
        for pdg in pdgs:
            if 'lbl' in pdg:
                series.append('lbnl_rw')


        # add rgpo unit and save funding info
        rgpoFunds = []
        if isFunded:
            for pdg in pdgs:
                if 'rgpo' in pdg and 'nonuc' not in pdg:
                    self.addRgpo(series, grants, grantInfo, rgpoFunds)

        # add department series
        if len(userdepdict) > 0:
            self.adddeptseries(series, userslist, userdepdict, groupToUnit)
        
        # add rgpo funding units
        for unit in rgpoFunds:
            series.append(unit)

        #remove dups
        series = list(dict.fromkeys(series))

        #build the units list now
        for s in series:
            self.outstr += self.baseStr2.format(param=s)

        #remove last comma
        self.outstr = self.outstr[:-1]

        #finally
        self.outstr = self.baseStr.format(param=self.outstr)

    def addRgpo(self, series, grants, grantInfo, rgpoFunds):
        #see if rgpo is mentioned and if so what suffix is added
        isFunded = False
        for g in grants:
            if grantInfo[g][0] and grantInfo[g][1]:
                for i in range(len(self.rgpo)):
                    if re.search(self.rgpo[i], grantInfo[g][0], re.IGNORECASE):
                        rgpoFunds.append(self.rgposeries[i])
                        isFunded = True
        if isFunded:
            series.append('rgpo_rw')
        return


    def adddeptseries(self, series, userslist, userdepdict,groupToUnit):
        for u in userslist:
            if u in userdepdict:
                dept = str(userdepdict[u])
                if dept in groupToUnit:
                    series.append(groupToUnit[dept])
                series.append(groupToUnit[dept])


