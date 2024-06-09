-- Working here: https://chatgpt.com/c/4c8204c3-1785-4211-a9a3-e5f11312c51a
-- Define Person node
CREATE NODE TABLE Person (
    associate_id STRING PRIMARY KEY,
    first_name STRING,
    middle_name STRING,
    last_name STRING,
    title STRING
);

-- Define Address node
CREATE NODE TABLE Address (
    address_id STRING PRIMARY KEY, -- hash after trim...
    address_line_1 STRING,
    address_line_2 STRING,
    city STRING,
    state STRING,
    zip_code STRING
);

-- Define CareProviderOrganization node
CREATE NODE TABLE CareProviderOrganization (
    enrollment_id STRING PRIMARY KEY,
    enrollment_state STRING,
    provider_type_code STRING,
    provider_type_text STRING,
    npi STRING,
    multiple_npi_flag STRING,
    ccn STRING,
    organization_name STRING,
    doing_business_as_name STRING,
    incorporation_date STRING,
    incorporation_state STRING,
    organization_type_structure STRING,
    organization_other_type_text STRING,
    proprietary_nonprofit STRING,
    practice_location_type STRING,
    location_other_type_text STRING,
    distro_access_url STRING,
    distro_title STRING,
    distro_modified STRING,
    _load_ts TIMESTAMP
);

-- Define LegalEntity node
CREATE NODE TABLE LegalEntity (
    legal_entity_id STRING PRIMARY KEY,
    organization_name STRING,
    doing_business_as_name STRING,
    percentage_ownership STRING,
    created_for_acquisition STRING,
    corporation STRING,
    llc STRING,
    medical_provider_supplier STRING,
    management_services_company STRING,
    medical_staffing_company STRING,
    holding_company STRING,
    investment_firm STRING,
    financial_institution STRING,
    consulting_firm STRING,
    for_profit STRING,
    non_profit STRING,
    other_type STRING,
    other_type_text STRING
);

-- Define LocatedAt relationship between Person and Address
CREATE REL TABLE LocatedAt (
    FROM Person TO Address
);

-- Define LocatedAt relationship between CareProviderOrganization and Address
CREATE REL TABLE LocatedAt (
    FROM CareProviderOrganization TO Address
);

-- Define OwnedBy relationship between CareProviderOrganization and LegalEntity
CREATE REL TABLE OwnedBy (
    FROM CareProviderOrganization TO LegalEntity,
    role_code STRING,
    role_text STRING,
    association_date STRING
);
