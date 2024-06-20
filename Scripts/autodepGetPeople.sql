SET TRANSACTION ISOLATION LEVEL SNAPSHOT
COMMIT TRANSACTION
BEGIN TRANSACTION

SELECT pr.[Publication ID] as pubId
      ,p.[Index] as seq
      ,p.[First Name] as fname
      ,p.[Last Name] as lname
      ,p.[Resolved User ID] as userid
	  ,u.Email as email
	  ,u.[First Name] as ufname
	  ,u.[Last Name] as ulname
  FROM [Publication Record Person] p
  left join [User] u on u.ID = p.[Resolved User ID]
  join [Publication Record] pr on pr.ID = p.[Publication Record ID]
  where p.[Property] = 'authors' and [Publication Record ID] in (
		  SELECT [ID]
		  FROM [Publication Record] pr
		  WHERE pr.[Data Source]='Europe PubMed Central'
				 and pr.[Publication ID] in
					(PUB_IDs) )
  order by seq
;

COMMIT TRANSACTION
