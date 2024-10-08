SELECT role_text, role_code, COUNT(1) FROM vw_extract_organization_owner_relationships
GROUP BY role_text, role_code


/*
role_text	COUNT(1)
5% OR GREATER DIRECT OWNERSHIP INTEREST	85425
5% OR GREATER INDIRECT OWNERSHIP INTEREST	78567
5% OR GREATER MORTGAGE INTEREST	1886
5% OR GREATER SECURITY INTEREST	2821
GENERAL PARTNERSHIP INTEREST	1578
LIMITED PARTNERSHIP INTEREST	1624
OPERATIONAL/MANAGERIAL CONTROL	97864
OTHER	9450
*/