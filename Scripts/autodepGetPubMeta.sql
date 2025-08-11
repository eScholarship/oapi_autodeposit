SET TRANSACTION ISOLATION LEVEL SNAPSHOT
COMMIT TRANSACTION
BEGIN TRANSACTION
SELECT		pub.ID as id,
			pub.abstract,
			pub.[Type ID],
			pub.[Canonical journal title] as journal,
			pub.[Computed Title] as title,
			pub.[doi],
			pub.[issn],
			pub.[issue],
			pub.[keywords],
			pub.[publication-date]  as pubdate,
			pub.[Type],
			pub.[volume],
            pub.[publisher-licence] as lic
FROM		[Publication] pub
WHERE		pub.[publication-date] is not null and
			pub.[types] not like '%Retracted%' and
			pub.abstract is not null and
			pub.authors is not null and
			pub.ID in (  select distinct(pur.[Publication ID])
						  from  [Publication User Relationship] pur, [User] u, [Group] g, [Publication OA Scheme State] poss
						  where pur.[Publication ID] in (PUB_IDs) and
								pur.[User ID] = u.ID and
								u.[Primary Group Descriptor] is not null and
								u.[Primary Group Descriptor] != 'uc-admin' and
								u.[Primary Group Descriptor] not like '%nonuc%' and
								u.[Primary Group Descriptor] = g.[Primary Group Descriptor] and
								poss.[Publication ID] = pur.[Publication ID] and
								poss.[OA Scheme ID] = g.[OA Policy ID])

;

COMMIT TRANSACTION
