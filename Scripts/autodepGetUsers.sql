SET TRANSACTION ISOLATION LEVEL SNAPSHOT
COMMIT TRANSACTION
BEGIN TRANSACTION
SELECT		pur.[Publication ID] as pubId,
			u.ID as userId,
			u.[Last Name] as lname,
			u.[First Name] as fname,
			u.Email as email,
			u.Initials as initial,
			u.[Primary Group Descriptor] as pgd,
			g.ID as groupId

FROM		[User] u, [Publication User Relationship] pur, [Group] g, [Group User Membership] gum
WHERE		u.ID = pur.[User ID] and 
			gum.[Group ID] = g.ID and
			gum.[User ID] = u.ID and
			pur.[Type] = 'Authored by' and
			pur.[Publication ID] in (PUB_IDs) and
			g.ID in (GROUP_IDs)

;

COMMIT TRANSACTION