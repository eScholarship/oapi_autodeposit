OAPI Auto deposit tool
======================
This repository contains a Python-based tool that automates the deposit of eligible publications from Elements into eScholarship, the University of California’s open access repository. It identifies publications covered under UC’s Open Access Policy that are claimed by UC authors and have publicly available PDFs, then deposits them using eScholarship’s GraphQL APIs.

Features
------------------------
* Retrieves metadata and file URLs for eligible publications from Elements
* Transforms publication data into eScholarship’s required format
* Deposits items via GraphQL API
* Logs deposit activity and errors
* Interfaces with multiple databases for reporting and control

Description of the files
------------------------
* autodeposit.py - Creates controller and executes auto deposit task
* controlIntf.py - Creates batches to deposit to eScholarship based on info from Elements
* depositFields.py - Transforms data from Elements to the format expected by eScholarship
* escholDBIntf.py - Obtains data from eScholarship database
* escholIntf.py - Despoits items in eScholaship using GraphQL APIs
* loggingIntf.py - Logs information about autodeposit activities in DB
* reportingdbIntf.py - Obtains information from Elements reporting database
