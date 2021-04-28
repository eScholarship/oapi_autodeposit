-- Common Table Expression to store relevant user data

SET TRANSACTION ISOLATION LEVEL SNAPSHOT
COMMIT TRANSACTION
BEGIN TRANSACTION

;WITH pubmed as (
  SELECT [ID], 
		 [Publication ID], 
		 prf.[File URL]
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
)
SELECT	    pur.[Publication ID] as id,
			pubmed.[File URL] as url

FROM		[User], pubmed, [Publication User Relationship] pur
WHERE		[User].ID = pur.[User ID] and 
			pur.[Publication ID] = pubmed.[Publication ID] and 
			pur.[Type] = 'Authored by' and
			[User].[Primary Group Descriptor] like 'ucm-%' 

;

COMMIT TRANSACTION
