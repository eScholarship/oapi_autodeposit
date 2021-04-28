SET TRANSACTION ISOLATION LEVEL SNAPSHOT
COMMIT TRANSACTION
BEGIN TRANSACTION
SELECT		gpr.[Publication ID] as pubId,
			g.ID as grantId,
			g.[funder-name] as fname,
			g.[funder-reference] as fref

FROM		[Grant] g, [Grant Publication Relationship] gpr
WHERE		g.ID = gpr.[Grant ID] and 
			gpr.[Publication ID] in (PUB_IDs)

;

COMMIT TRANSACTION


