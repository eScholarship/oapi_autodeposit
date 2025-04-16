SET TRANSACTION ISOLATION LEVEL SNAPSHOT
COMMIT TRANSACTION
BEGIN TRANSACTION
SELECT		pr.[Publication ID],
		    prf.[File URL],
		    pr.[Data Source Proprietary ID] as med_id
FROM		[Publication Record] pr, [Publication Record File] prf
WHERE		prf.[Publication Record ID] = pr.[ID] and 
			pr.[Data Source] = 'Europe PubMed Central' and 
			prf.[Data Source] = 'Europe PubMed Central' and prf.[File URL] like  'https://europepmc.org/articles/PMC%' and 
			pr.[Publication ID] in (PUB_IDs)

COMMIT TRANSACTION


