-- TODO
-- extract ownership associate_id pairs for orgs and persons
-- extract affiliations / works at relationships
-- extract SNF affiliations and model in affiliated network
-- normalize addresses?

DROP VIEW IF EXISTS vw_enrolled_care_provider_organizations;
CREATE VIEW vw_enrolled_care_provider_organizations AS
SELECT 
    associate_id,
    enrollment_id,
    enrollment_state,
    provider_type_code,
    provider_type_text,
    npi,
    multiple_npi_flag,
    ccn,
    organization_name,
    doing_business_as_name,
    incorporation_date,
    incorporation_state,
    organization_type_structure,
    organization_other_type_text,
    proprietary_nonprofit,
    practice_location_type,
    location_other_type_text
FROM hospital_enrollments
UNION ALL
SELECT 
    associate_id,
    enrollment_id,
    enrollment_state,
    provider_type_code,
    provider_type_text,
    npi,
    multiple_npi_flag,
    ccn,
    organization_name,
    doing_business_as_name,
    incorporation_date,
    incorporation_state,
    organization_type_structure,
    organization_other_type_text,
    proprietary_nonprofit,
    practice_location_type,
    location_other_type_text
FROM hha_enrollments
UNION ALL
SELECT 
    associate_id,
    enrollment_id,
    enrollment_state,
    provider_type_code,
    provider_type_text,
    npi,
    multiple_npi_flag,
    ccn,
    organization_name,
    doing_business_as_name,
    incorporation_date,
    incorporation_state,
    organization_type_structure,
    organization_other_type_text,
    proprietary_nonprofit,
    NULL AS practice_location_type,
    NULL AS location_other_type_text
FROM hospice_enrollments
UNION ALL
SELECT 
    associate_id,
    enrollment_id,
    enrollment_state,
    provider_type_code,
    provider_type_text,
    npi,
    multiple_npi_flag,
    ccn,
    organization_name,
    doing_business_as_name,
    incorporation_date,
    incorporation_state,
    organization_type_structure,
    organization_other_type_text,
    proprietary_nonprofit,
    NULL AS practice_location_type,
    NULL AS location_other_type_text
FROM snf_enrollments
UNION ALL
SELECT 
    associate_id,
    enrollment_id,
    enrollment_state,
    provider_type_code,
    provider_type_text,
    npi,
    multiple_npi_flag,
    ccn,
    organization_name,
    doing_business_as_name,
    incorporation_date,
    incorporation_state,
    organization_type_structure,
    organization_other_type_text,
    proprietary_nonprofit,
    NULL AS practice_location_type,
    NULL AS location_other_type_text
FROM fqhc_enrollments
UNION ALL
SELECT 
    associate_id,
    enrollment_id,
    enrollment_state,
    provider_type_code,
    provider_type_text,
    npi,
    multiple_npi_flag,
    ccn,
    organization_name,
    doing_business_as_name,
    incorporation_date,
    incorporation_state,
    organization_type_structure,
    organization_other_type_text,
    proprietary_nonprofit,
    NULL AS practice_location_type,
    NULL AS location_other_type_text
FROM rhc_enrollments;

-- addresses
DROP VIEW IF EXISTS vw_addresses_with_associate;
CREATE VIEW vw_addresses_with_associate AS
SELECT "address_line_1_owner" AS "address_line_1",
    "address_line_2_owner" AS "address_line_2",
    "city_owner" AS "city",
    "state_owner" AS "state",
    "zip_code_owner" AS "zip_code",
    "associate_id_owner" AS "associate_id"
FROM hospital_all_owners
WHERE type_owner = 'O'
UNION ALL
SELECT "address_line_1_owner" AS "address_line_1",
    "address_line_2_owner" AS "address_line_2",
    "city_owner" AS "city",
    "state_owner" AS "state",
    "zip_code_owner" AS "zip_code",
    "associate_id_owner" AS "associate_id"
FROM hha_all_owners
WHERE type_owner = 'O'
UNION ALL
SELECT "address_line_1_owner" AS "address_line_1",
    "address_line_2_owner" AS "address_line_2",
    "city_owner" AS "city",
    "state_owner" AS "state",
    "zip_code_owner" AS "zip_code",
    "associate_id_owner" AS "associate_id"
FROM hospice_all_owners
WHERE type_owner = 'O'
UNION ALL
SELECT "address_line_1_owner" AS "address_line_1",
    "address_line_2_owner" AS "address_line_2",
    "city_owner" AS "city",
    "state_owner" AS "state",
    "zip_code_owner" AS "zip_code",
    "associate_id_owner" AS "associate_id"
FROM snf_all_owners
WHERE type_owner = 'O'
UNION ALL
SELECT "address_line_1_owner" AS "address_line_1",
    "address_line_2_owner" AS "address_line_2",
    "city_owner" AS "city",
    "state_owner" AS "state",
    "zip_code_owner" AS "zip_code",
    "associate_id_owner" AS "associate_id"
FROM fqhc_all_owners
WHERE type_owner = 'O'
UNION ALL
SELECT "address_line_1_owner" AS "address_line_1",
    "address_line_2_owner" AS "address_line_2",
    "city_owner" AS "city",
    "state_owner" AS "state",
    "zip_code_owner" AS "zip_code",
    "associate_id_owner" AS "associate_id"
FROM rhc_all_owners
WHERE type_owner = 'O'
UNION ALL
SELECT "address_line_1",
    "address_line_2",
    "city",
    "state",
    "zip_code",
    "associate_id"
FROM hospital_enrollments
UNION ALL
SELECT "address_line_1",
    "address_line_2",
    "city",
    "state",
    "zip_code",
    "associate_id"
FROM hha_enrollments
UNION ALL
SELECT "address_line_1",
    "address_line_2",
    "city",
    "state",
    "zip_code",
    "associate_id"
FROM hospice_enrollments
UNION ALL
SELECT "address_line_1",
    "address_line_2",
    "city",
    "state",
    "zip_code",
    "associate_id"
FROM snf_enrollments
UNION ALL
SELECT "address_line_1",
    "address_line_2",
    "city",
    "state",
    "zip_code",
    "associate_id"
FROM fqhc_enrollments
UNION ALL
SELECT "address_line_1",
    "address_line_2",
    "city",
    "state",
    "zip_code",
    "associate_id"
FROM rhc_enrollments;

DROP VIEW IF EXISTS vw_person;
CREATE VIEW vw_person AS
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    first_name_owner AS first_name,
    middle_name_owner AS middle_name,
    last_name_owner AS last_name
FROM hospital_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    first_name_owner AS first_name,
    middle_name_owner AS middle_name,
    last_name_owner AS last_name
FROM hha_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    first_name_owner AS first_name,
    middle_name_owner AS middle_name,
    last_name_owner AS last_name
FROM hospice_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    first_name_owner AS first_name,
    middle_name_owner AS middle_name,
    last_name_owner AS last_name
FROM snf_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    first_name_owner AS first_name,
    middle_name_owner AS middle_name,
    last_name_owner AS last_name
FROM fqhc_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    first_name_owner AS first_name,
    middle_name_owner AS middle_name,
    last_name_owner AS last_name
FROM rhc_all_owners
WHERE type_owner = 'I';

-- Note this includes both ownership relationships as well as employment relationships
DROP VIEW IF EXISTS vw_person_affiliations;
CREATE VIEW vw_person_affiliations AS
WITH union_all AS (
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM hospital_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM hha_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM hospice_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM snf_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM fqhc_all_owners
WHERE type_owner = 'I'
UNION
SELECT associate_id_owner AS associate_id,
    associate_id AS associate_id_care_organization,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM rhc_all_owners
WHERE type_owner = 'I'
)
SELECT 
    DISTINCT 
    e.enrollment_id,
    u.associate_id,
    u.role_code,
    u.role_text,
    u.title,
    u.association_date,
    u.percentage_ownership
FROM union_all u
INNER JOIN vw_enrolled_care_provider_organizations e
ON u.associate_id_care_organization = e.associate_id;

DROP VIEW IF EXISTS vw_extract_organization_owners;
CREATE VIEW vw_extract_organization_owners AS
SELECT
  associate_id AS associate_id_care_organization,
  associate_id_owner AS associate_id,
  organization_name_owner AS organization_name,
  doing_business_as_name_owner AS doing_business_as_name,
  created_for_acquisition_owner AS created_for_acquisition,
  corporation_owner AS is_corporation,
  llc_owner AS is_llc,
  medical_provider_supplier_owner AS is_medical_provider_supplier,
  management_services_company_owner AS is_management_services_company,
  medical_staffing_company_owner AS is_medical_staffing_company,
  holding_company_owner AS is_holding_company,
  investment_firm_owner AS is_investment_firm,
  financial_institution_owner AS is_financial_institution,
  consulting_firm_owner AS is_consulting_firm,
  for_profit_owner AS is_for_profit,
  non_profit_owner AS is_non_profit,
  other_type_owner AS other_type,
  other_type_text_owner AS other_type_text
FROM hospital_all_owners
WHERE type_owner = 'O'
UNION
SELECT
  associate_id AS associate_id_care_organization,
  associate_id_owner AS associate_id,
  organization_name_owner AS organization_name,
  doing_business_as_name_owner AS doing_business_as_name,
  created_for_acquisition_owner AS created_for_acquisition,
  corporation_owner AS is_corporation,
  llc_owner AS is_llc,
  medical_provider_supplier_owner AS is_medical_provider_supplier,
  management_services_company_owner AS is_management_services_company,
  medical_staffing_company_owner AS is_medical_staffing_company,
  holding_company_owner AS is_holding_company,
  investment_firm_owner AS is_investment_firm,
  financial_institution_owner AS is_financial_institution,
  consulting_firm_owner AS is_consulting_firm,
  for_profit_owner AS is_for_profit,
  non_profit_owner AS is_non_profit,
  other_type_owner AS other_type,
  other_type_text_owner AS other_type_text
FROM hha_all_owners
WHERE type_owner = 'O'
UNION
SELECT
  associate_id AS associate_id_care_organization,
  associate_id_owner AS associate_id,
  organization_name_owner AS organization_name,
  doing_business_as_name_owner AS doing_business_as_name,
  created_for_acquisition_owner AS created_for_acquisition,
  corporation_owner AS is_corporation,
  llc_owner AS is_llc,
  medical_provider_supplier_owner AS is_medical_provider_supplier,
  management_services_company_owner AS is_management_services_company,
  medical_staffing_company_owner AS is_medical_staffing_company,
  holding_company_owner AS is_holding_company,
  investment_firm_owner AS is_investment_firm,
  financial_institution_owner AS is_financial_institution,
  consulting_firm_owner AS is_consulting_firm,
  for_profit_owner AS is_for_profit,
  non_profit_owner AS is_non_profit,
  other_type_owner AS other_type,
  other_type_text_owner AS other_type_text
FROM hospice_all_owners
WHERE type_owner = 'O'
UNION
SELECT
  associate_id AS associate_id_care_organization,
  associate_id_owner AS associate_id,
  organization_name_owner AS organization_name,
  doing_business_as_name_owner AS doing_business_as_name,
  created_for_acquisition_owner AS created_for_acquisition,
  corporation_owner AS is_corporation,
  llc_owner AS is_llc,
  medical_provider_supplier_owner AS is_medical_provider_supplier,
  management_services_company_owner AS is_management_services_company,
  medical_staffing_company_owner AS is_medical_staffing_company,
  holding_company_owner AS is_holding_company,
  investment_firm_owner AS is_investment_firm,
  financial_institution_owner AS is_financial_institution,
  consulting_firm_owner AS is_consulting_firm,
  for_profit_owner AS is_for_profit,
  non_profit_owner AS is_non_profit,
  other_type_owner AS other_type,
  other_type_text_owner AS other_type_text
FROM snf_all_owners
WHERE type_owner = 'O'
UNION
SELECT
  associate_id AS associate_id_care_organization,
  associate_id_owner AS associate_id,
  organization_name_owner AS organization_name,
  doing_business_as_name_owner AS doing_business_as_name,
  created_for_acquisition_owner AS created_for_acquisition,
  corporation_owner AS is_corporation,
  llc_owner AS is_llc,
  medical_provider_supplier_owner AS is_medical_provider_supplier,
  management_services_company_owner AS is_management_services_company,
  medical_staffing_company_owner AS is_medical_staffing_company,
  holding_company_owner AS is_holding_company,
  investment_firm_owner AS is_investment_firm,
  financial_institution_owner AS is_financial_institution,
  consulting_firm_owner AS is_consulting_firm,
  for_profit_owner AS is_for_profit,
  non_profit_owner AS is_non_profit,
  other_type_owner AS other_type,
  other_type_text_owner AS other_type_text
FROM fqhc_all_owners
WHERE type_owner = 'O'
UNION
SELECT
  associate_id AS associate_id_care_organization,
  associate_id_owner AS associate_id,
  organization_name_owner AS organization_name,
  doing_business_as_name_owner AS doing_business_as_name,
  created_for_acquisition_owner AS created_for_acquisition,
  corporation_owner AS is_corporation,
  llc_owner AS is_llc,
  medical_provider_supplier_owner AS is_medical_provider_supplier,
  management_services_company_owner AS is_management_services_company,
  medical_staffing_company_owner AS is_medical_staffing_company,
  holding_company_owner AS is_holding_company,
  investment_firm_owner AS is_investment_firm,
  financial_institution_owner AS is_financial_institution,
  consulting_firm_owner AS is_consulting_firm,
  for_profit_owner AS is_for_profit,
  non_profit_owner AS is_non_profit,
  other_type_owner AS other_type,
  other_type_text_owner AS other_type_text
FROM rhc_all_owners
WHERE type_owner = 'O';


DROP VIEW IF EXISTS vw_extract_organization_owner_relationships;
CREATE VIEW vw_extract_organization_owner_relationships AS
WITH union_all AS (
SELECT
    associate_id AS associate_id_care_organization,
    associate_id_owner AS associate_id,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM hospital_all_owners
WHERE type_owner = 'O'
UNION
SELECT
    associate_id AS associate_id_care_organization,
    associate_id_owner AS associate_id,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM hha_all_owners
WHERE type_owner = 'O'
UNION
SELECT
    associate_id AS associate_id_care_organization,
    associate_id_owner AS associate_id,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM hospice_all_owners
WHERE type_owner = 'O'
UNION
SELECT
    associate_id AS associate_id_care_organization,
    associate_id_owner AS associate_id,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,   
    association_date_owner AS association_date,
    percentage_ownership
FROM snf_all_owners
WHERE type_owner = 'O'
UNION
SELECT
    associate_id AS associate_id_care_organization,
    associate_id_owner AS associate_id,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM fqhc_all_owners
WHERE type_owner = 'O'
UNION
SELECT
    associate_id AS associate_id_care_organization,
    associate_id_owner AS associate_id,
    role_code_owner AS role_code,
    role_text_owner AS role_text,
    title_owner AS title,
    association_date_owner AS association_date,
    percentage_ownership
FROM rhc_all_owners
WHERE type_owner = 'O'
)
SELECT 
    DISTINCT 
    e.enrollment_id,
    u.associate_id,
    u.role_code,
    u.role_text,
    u.title,
    u.association_date,
    u.percentage_ownership
FROM union_all u
INNER JOIN vw_enrolled_care_provider_organizations e
ON u.associate_id_care_organization = e.associate_id;

