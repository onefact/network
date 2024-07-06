STATEMENT_DICT = {
    ("OwnedBy", "PECOSEnrolledCareProvider", "Person"): """
        MATCH (p:PECOSEnrolledCareProvider), (o:Person)
        WHERE p.enrollment_id = $enrollment_id AND o.associate_id = $associate_id
        CREATE (p)-[:OwnedBy {role_code $role_code, role_text $role_text, title $title, association_date $association_date, percentage_ownership $percentage_ownership}]->(o);
    """,
}