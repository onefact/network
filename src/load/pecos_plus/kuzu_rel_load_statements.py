STATEMENT_DICT = {
    ("OwnedBy", "PECOSEnrolledCareProvider", "Person"): """
            MATCH (p1:PECOSEnrolledCareProvider), (p2:Person) 
            WHERE p1.enrollment_id = $enrollment_id AND p2.associate_id = $associate_id 
            CREATE (p1)-[:OwnedBy {
                role_text: $role_text,
                percentage_ownership: $percentage_ownership,
                association_date: $association_date,
                role_code: $role_code,
                title: $title
            }]->(p2);
    """,


    ("OwnedBy", "PECOSEnrolledCareProvider", "LegalEntity"): """
            MATCH (p1:PECOSEnrolledCareProvider), (l:LegalEntity) 
            WHERE p1.enrollment_id = $enrollment_id AND l.associate_id = $associate_id 
            CREATE (p1)-[:OwnedBy {
                role_text: $role_text,
                percentage_ownership: $percentage_ownership,
                association_date: $association_date,
                role_code: $role_code,
                title: $title
            }]->(l);
    """,
}

# STATEMENT_DICT = {
#     ("OwnedBy", "PECOSEnrolledCareProvider", "Person"): """
#         MATCH (p:PECOSEnrolledCareProvider), (o:Person)
#         WHERE p.enrollment_id = $enrollment_id AND o.associate_id = $associate_id
#         CREATE (p)-[:OwnedBy {role_code $role_code, role_text $role_text, title $title, association_date $association_date, percentage_ownership $percentage_ownership}]->(o);
#     """,
# }