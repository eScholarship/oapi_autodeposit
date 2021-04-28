SET TRANSACTION ISOLATION LEVEL SNAPSHOT
COMMIT TRANSACTION
BEGIN TRANSACTION

SELECT pr.[Publication ID] as id,
		 prf.[File URL] as url
FROM [Publication Record] pr, [Publication Record File] prf
WHERE pr.[Data Source]='Europe PubMed Central' and 
		prf.[Publication Record ID] = pr.[ID] and 
		prf.[Data Source] = 'Europe PubMed Central' and 
		prf.[File URL Accessibility]='Public' and 
		pr.[Publication ID] not in
		(SELECT [Publication ID] 
		 FROM [Publication Record] 
		 WHERE [Data Source]='eScholarship')
		 and pr.[Publication ID] in
			(SELECT	pur.[Publication ID] 
			 FROM [Publication User Relationship] pur 
			 WHERE	pur.[Type] = 'Authored by') 

;

COMMIT TRANSACTION

