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
    ):
        self.target_table = target_table
        self.source_table = source_table
        self.transform_func = transform_func

    def load(
        self, target_conn: kuzu.Connection, source_conn: sqlite3.Connection
    ) -> None:
        df = pd.read_sql_query(f"SELECT * FROM {self.source_table}", source_conn)
        if self.transform_func:
            df = self.transform_func(df)

        if DEBUG_MODE:
            df = df.iloc[0:10]

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

# Transform Logic
def transform_care_provider_organizations(df: pd.DataFrame) -> pd.DataFrame:
    # assert no dups on enrollment_id
    assert df.duplicated(subset=["enrollment_id"]).sum() == 0, "Duplicate pecos_enrollment_id found"
    return df

# ETL mappings, commented out w/e you don't want to load
ETL_MAPPINGS = [
    KuzuObjectLoader(
        target_table="CareProviderOrganization",
        source_table="vw_enrolled_care_provider_organizations",
        transform_func=transform_care_provider_organizations,
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
    results = kuzu_conn.execute("MATCH (p:CareProviderOrganization) RETURN p.enrollment_id, p.associate_id, p.organization_name;").get_as_df()
    print(results.iloc[0:10])