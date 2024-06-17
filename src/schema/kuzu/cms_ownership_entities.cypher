// Working here: https://chatgpt.com/c/4c8204c3-1785-4211-a9a3-e5f11312c51a
// Define Person node
CREATE NODE TABLE Person (
    associate_id STRING,
    first_name STRING,
    middle_name STRING,
    last_name STRING,
    // title STRING, moved to associated relation, Person 1:M Titles
    PRIMARY KEY (associate_id)
);

CREATE NODE TABLE Address (
    address_id STRING, // hash after trim...
    normalized_address_string STRING,
    address_line_1 STRING,
    address_line_2 STRING,
    city STRING,
    state STRING,
    zip_code STRING,
    PRIMARY KEY (address_id)
    // TODO geocodes
);

// Define CareProviderOrganization node
CREATE NODE TABLE CareProviderOrganization (
    associate_id STRING,
    enrollment_id STRING,
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
    PRIMARY KEY (enrollment_id)
);

// Define LegalEntity node
CREATE NODE TABLE LegalEntity (
    associate_id STRING,
    legal_entity_id STRING, // TIN if available?
    organization_name STRING,
    doing_business_as_name STRING,
    created_for_acquisition STRING,
    is_corporation STRING,
    is_llc STRING,
    is_medical_provider_supplier STRING,
    is_management_services_company STRING,
    is_medical_staffing_company STRING,
    is_holding_company STRING,
    is_investment_firm STRING,
    is_financial_institution STRING,
    is_consulting_firm STRING,
    is_for_profit STRING,
    is_non_profit STRING,
    other_type STRING,
    other_type_text STRING,
    PRIMARY KEY (associate_id)
);


// Use edge groups when multiple entities share the same type of relationship
CREATE REL TABLE GROUP LocatedAt (
    FROM CareProviderOrganization TO Address,
    FROM Person TO Address
);

CREATE REL TABLE GROUP OwnedBy (
    FROM CareProviderOrganization TO LegalEntity,
    FROM Person TO LegalEntity,
    role_code STRING,
    role_text STRING,
    title STRING,
    association_date STRING,
    percentage_ownership STRING
);

CREATE REL TABLE EmployedBy (
    FROM Person TO CareProviderOrganization,
    role_code STRING,
    role_text STRING,
    title STRING,
    association_date STRING
);


CREATE REL TABLE GROUP AffiliatedWith (
    FROM LegalEntity TO CareProviderOrganization,
    FROM Person TO CareProviderOrganization,
    FROM Person TO LegalEntity,
    proposing_entity STRING, // Who, or what is proposing the affiliation exists?
    methodology_name STRING, // What methodology is used to infer the relationship?
    methodology_detail_url STRING, // What methodology are they using?
    evidence_url STRING, // Link to evidence, this may be a json document, a .zip file, or a internet archive link
    effective_date DATE,
    end_date DATE
);