OAPI Auto deposit tool
======================
This tool obtains metadata and file url for eligible publications from Elements and deposits in eScholarship. The eligible publications are the ones covered under Open Access Policy that are claimed by UC author and where open access public pdf is available. 

Description of the files
------------------------
* autodeposit.py - Creates controller and executes auto deposit task
* controlIntf.py - Creates batches to deposit to eScholarship based on info from Elements
* depositFields.py - Transforms data from Elements to the format expected by eScholarship
* escholDBIntf.py - Obtains data from eScholarship database
* escholIntf.py - Despoits items in eScholaship using GraphQL APIs
* loggingIntf.py - Logs information about autodeposit activities in DB
* reportingdbIntf.py - Obtains information from Elements reporting database
