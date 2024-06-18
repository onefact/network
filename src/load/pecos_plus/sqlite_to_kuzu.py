"""
%md

# Purpose
Load CMS ownership data from SQLite to Kuzu Graph Database

### Notes
In modeling, followed these guide:
- https://blog.kuzudb.com/post/transforming-your-data-to-graphs-1/
- https://blog.kuzudb.com/post/transforming-your-data-to-graphs-2/

### Resources
https://github.com/kuzudb/graphdb-demo/blob/main/src/python/transactions/load_data.py
"""

from __future__ import annotations
import os
import shutil
from pathlib import Path
from typing import Callable, Optional
import kuzu
import sqlite3
import pandas as pd

# Constants
DATA_PATH = Path("data/staging")
KUZU_DB_NAME = "pecos_plus.db"
SQLITE_DB_NAME = "cms_data_api_raw.db"
DEBUG_MODE = False

# ETL Object
class KuzuObjectLoader:
    def __init__(
        self,
        target_table: str,
        source_table: str,
        transform_func: Optional[Callable] = None,
        validate_func: Optional[Callable] = None,
    ):
        self.target_table = target_table
        self.source_table = source_table
        self.transform_func = transform_func
        self.validate_func = validate_func

    def load(
        self, target_conn: kuzu.Connection, source_conn: sqlite3.Connection
    ) -> None:
        print(f"Loading {self.source_table} to {self.target_table} into KùzuDB")
        df = pd.read_sql_query(f"SELECT * FROM {self.source_table}", source_conn)
        if self.transform_func:
            df = self.transform_func(df)

        if DEBUG_MODE:
            df = df.iloc[0:10]

        if self.validate_func:
            self.validate_func(df)

        # chunk the pandas dataframe and iterate over chunks
        # loads with larger chunk size threw "segmentation fault"
        CHUNK_SIZE = 2000
        for i in range(0, len(df), CHUNK_SIZE):
            chunk = df[i:i + CHUNK_SIZE]
            print(f"Loading chunk ({i}, {i + CHUNK_SIZE})")
            target_conn.execute(f"COPY {self.target_table} FROM (LOAD FROM chunk RETURN *)")
        print(f"Loaded {len(df)} records to {self.target_table} into KùzuDB")


# Helper Functions
def initialize_tables(conn: kuzu.Connection, ddl_script: str) -> None:
    #print(ddl_script)
    conn.execute(ddl_script)

# Transform / Validation Logic
def validate_care_provider_organizations(df: pd.DataFrame) -> None:
    # assert no dups on enrollment_id
    assert df.duplicated(subset=["enrollment_id"]).sum() == 0, "Duplicate pecos_enrollment_id found"
    return None

def validate_person(df: pd.DataFrame) -> None:
    assert df.duplicated(subset=["associate_id"]).sum() == 0, "Duplicate associate_id found"
    return None

def transform_legal_entity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Many records have conflicting information, depending on which file the ownership record originated from.

    For example:
        - One record may indicate true for "created_for_acquisition" while another may show NULL, or false.
        - One record may indicate true for "created_for_acquisition" while another may show NULL, or false.

    To keep it simple (naive?) 'Y' trumps 'N' and populated trumps NULL.  
    """
    count = df.shape[0]
    dedup_count = len(df["associate_id"].unique())
    group_cols = ["associate_id"]
    fields = [
        "created_for_acquisition",
        "is_corporation",
        "is_llc",
        "is_medical_provider_supplier",
        "is_management_services_company",
        "is_medical_staffing_company",
        "is_holding_company",
        "is_investment_firm",
        "is_financial_institution",
        "is_consulting_firm",
        "is_for_profit",
        "is_non_profit",
        "other_type"
    ]
    
    df_booleans = df.groupby(group_cols)[fields].apply(lambda x: x.ffill().bfill().max()).reset_index()
    fields = [
        "organization_name",
        "doing_business_as_name",
        "other_type_text"
    ]
    df_names = df.groupby(group_cols)[fields].apply(lambda x: x.ffill().bfill().max()).reset_index()
    df = pd.merge(df_booleans, df_names, on=group_cols)
    assert dedup_count == df.shape[0], "Deduplication failed"
    df['legal_entity_id'] = None  # or populate it with appropriate values
    print(f"Transformed {count} records to {df.shape[0]} records")
    return df

def validate_legal_entity(df: pd.DataFrame) -> None:
    assert df.duplicated(subset=["associate_id"]).sum() == 0, "Duplicate associate_id found"
    return None

# ETL mappings, commented out w/e you don't want to load
ETL_MAPPINGS = [
    # KuzuObjectLoader(
    #     target_table="PECOSEnrolledCareProvider",
    #     source_table="vw_enrolled_care_provider_organizations",
    #     transform_func=None,
    #     validate_func=validate_care_provider_organizations,
    # ),
    KuzuObjectLoader(
        target_table="LegalEntity",
        source_table="vw_extract_organization_owners",
        transform_func=transform_legal_entity,
        validate_func=validate_legal_entity
    ),
    KuzuObjectLoader(
        target_table="Person",
        source_table="vw_person",
        transform_func=None,
        validate_func=validate_person
    )
]

# Main function
def reload_from_scratch(
    data_path: str,
    kuzu_db_name: str,
    sqlite_db_name: str,
    etl_mappings: list[KuzuObjectLoader],
) -> None:
    """
    Delete existing Kuzu database and reload from scratch
    """

    DEST_PATH = os.path.join(data_path, kuzu_db_name)
    # Delete directory each time till we have MERGE FROM available in kuzu
    if os.path.exists(DEST_PATH):
        shutil.rmtree(DEST_PATH)

    # Create database
    kuzu_db = kuzu.Database(DEST_PATH)
    kuzu_conn = kuzu.Connection(kuzu_db)

    # Initialize tables
    with open("src/schema/kuzu/cms_ownership_entities.cypher", "r") as f:
        ddl_script = f.read()
        initialize_tables(kuzu_conn, ddl_script)

    results = kuzu_conn.execute("CALL SHOW_TABLES() RETURN *;").get_as_df()
    print(results)

    # Source DB
    sqlite_conn = sqlite3.connect(f"{data_path}/{sqlite_db_name}")

    for item in etl_mappings:
        item.load(kuzu_conn, sqlite_conn)

if __name__ == "__main__":
    reload_from_scratch(DATA_PATH, KUZU_DB_NAME, SQLITE_DB_NAME, ETL_MAPPINGS)
    kuzu_db = kuzu.Database(os.path.join(DATA_PATH, KUZU_DB_NAME))
    kuzu_conn = kuzu.Connection(kuzu_db)
    results = kuzu_conn.execute("MATCH (p:PECOSEnrolledCareProvider) RETURN p.enrollment_id, p.associate_id, p.organization_name;").get_as_df()
    print(results.iloc[0:10])