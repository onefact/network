-- SQLite

-- SELECT * FROM vw_enrolled_care_provider_organizations
-- WHERE associate_id IN (
--     SELECT associate_id
--     FROM vw_enrolled_care_provider_organizations
--     GROUP BY associate_id
--     HAVING COUNT() > 1
-- )
-- ORDER BY associate_id



SELECT * FROM vw_enrolled_care_provider_organizations
WHERE enrollment_id IN (
    SELECT enrollment_id
    FROM vw_enrolled_care_provider_organizations
    GROUP BY enrollment_id
    HAVING COUNT() > 1
)
ORDER BY enrollment_id