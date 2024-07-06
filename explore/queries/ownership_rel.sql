-- SQLite
SELECT * FROM vw_person_affiliations
WHERE role_code IN ('34', '35', '36', '37', '38', '39')
-- no nulls AND (enrollment_id IS NULL OR associate_id IS NULL)
