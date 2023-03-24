-- Common Table Expression to store relevant user data

SET TRANSACTION ISOLATION LEVEL SNAPSHOT
COMMIT TRANSACTION
BEGIN TRANSACTION

;WITH u as (
	SELECT	[User].[ID],
			[User].[Last Name],
			[User].[First Name],
			[User].[Email],
			[User].[Position],
			[User].[Primary Group Descriptor],
			-- which OA Policy applies to the user?
			[Group].[OA Policy ID],
			-- get the OA Policy name
			(	SELECT	[Name]
				FROM	[OA Policy] oap
				WHERE	oap.[ID] = [Group].[OA Policy ID]
			) as [OA Policy Name]
	FROM	[User]
			JOIN [Group] ON [Group].[Primary Group Descriptor] = [User].[Primary Group Descriptor]
						 OR ([User].[Primary Group Descriptor] IS NULL AND [Group].[ID] = 1) -- Users without a primary group descriptor are assigned to the top-level group
	WHERE	-- limit to current, active, academic users
			[User].[Is Current Staff] = 1
			AND [User].[Is Login Allowed] = 1
			AND [User].[Is Academic] = 1
			-- exclude the anonymous and system users
			AND [User].[ID] NOT IN (0,1)
),
puroa as (
	SELECT	pur.[Publication ID],
			pur.[User ID],
			poap.[OA Policy ID] as [OA Policy ID],
			poap.[Compliance Status]
	FROM	[Publication OA Policy] poap
			JOIN [Publication User Relationship] pur
				ON pur.[Publication ID] = poap.[Publication ID]
	WHERE	pur.[Type] = 'Authored by'	-- limit to authorship links (optional)
),
pubmed as (
  select [ID], [Publication ID], prf.[File URL]
  FROM [elements-cdl2-reporting].[dbo].[Publication Record] pr, [elements-cdl2-reporting].[dbo].[Publication Record File] prf
  where pr.[Data Source]='Europe PubMed Central' and prf.[Publication Record ID] = pr.[ID] and prf.[Data Source] = 'Europe PubMed Central' and prf.[File URL Accessibility]='Public'
  and prf.[File URL] like  'https://europepmc.org/articles/PMC%' and pr.[Publication ID] not in
  (select [Publication ID] from [elements-cdl2-reporting].[dbo].[Publication Record] where [Data Source]='eScholarship')
  and pr.[Publication ID] in
  (SELECT	pur.[Publication ID] FROM [Publication User Relationship] pur WHERE	pur.[Type] = 'Authored by') 
)
SELECT		u.[ID],
			u.[Last Name],
			u.[First Name],
			u.[Email],
			u.[Primary Group Descriptor] AS "Primary Group",
			u.[Position],
			u.[OA Policy ID],
			u.[OA Policy Name],
			puroa.[Publication ID],
			pubmed.[ID] as "Record ID",
			pubmed.[File URL]
FROM		u, puroa, pubmed
WHERE		u.ID = puroa.[User ID] and puroa.[Publication ID] = pubmed.[Publication ID]
ORDER BY	u.[ID]
;

COMMIT TRANSACTION


