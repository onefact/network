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
from typing import Callable, Optional, Tuple
import kuzu
import sqlite3
import pandas as pd
from kuzu_rel_load_statements import STATEMENT_DICT

# Constants
DATA_PATH = Path("data/staging")
KUZU_DB_NAME = "pecos_plus.db"
SQLITE_DB_NAME = "cms_data_api_raw.db"
DEBUG_MODE = False

# ETL Object
class KuzuObjectLoader:
    def __init__(
        self,
        source_table: str,
        target_table: Optional[str],
        relation_triple: Optional[Tuple[str, str, str]] = None,
        transform_func: Optional[Callable] = None,
        validate_func: Optional[Callable] = None,
    ):
        self.target_table = target_table
        self.rel_triple = relation_triple
        self.source_table = source_table
        self.transform_func = transform_func
        self.validate_func = validate_func
        assert (target_table or relation_triple) and not (
            self.target_table and relation_triple
        ), "Must provide target_table or rel_pair"
        self.is_relation = True if relation_triple else False

    def load(
        self,
        target_conn: kuzu.Connection,
        source_conn: sqlite3.Connection
    ) -> None:
        print(f"Loading {self.source_table} into KùzuDB")
        df = pd.read_sql_query(f"SELECT * FROM {self.source_table}", source_conn)
        if self.transform_func:
            df = self.transform_func(df)

        if DEBUG_MODE:
            df = df.iloc[0:10]

        if self.validate_func:
            self.validate_func(df)

        CHUNK_SIZE = 2000
        if not self.is_relation:
            # chunk the pandas dataframe and iterate over chunks
            # loads with larger chunk size threw "segmentation fault"
            for i in range(0, len(df), CHUNK_SIZE):
                chunk = df[i : i + CHUNK_SIZE]
                print(f"Loading chunk ({i}, {i + CHUNK_SIZE})")
                target_conn.execute(
                    f"COPY {self.target_table} FROM (LOAD FROM chunk RETURN *)"
                )
            print(f"Loaded {len(df)} records to {self.target_table} into KùzuDB")
        elif self.is_relation:
            # I is Kuzu Noob, grugbrain. I no know best way.
            # https://grugbrain.dev
            print(f"Loading {df.shape[0]} records to {self.rel_triple} into KùzuDB")
            df.reset_index(drop=True, inplace=True)
            for i, row in df.iterrows():
                print(i)
                if i % CHUNK_SIZE == 0:
                    print(f"Loading chunk ({i}, {i + CHUNK_SIZE})")
                statement = STATEMENT_DICT[self.rel_triple]
                target_conn.execute(statement, parameters=row.to_dict())
            print(f"Loaded {len(df)} records to {self.rel_triple} into KùzuDB")


# Helper Functions
def initialize_tables(conn: kuzu.Connection, ddl_script: str) -> None:
    # print(ddl_script)
    conn.execute(ddl_script)


# Transform / Validation Logic
def validate_care_provider_organizations(df: pd.DataFrame) -> None:
    # assert no dups on enrollment_id
    assert (
        df.duplicated(subset=["enrollment_id"]).sum() == 0
    ), "Duplicate pecos_enrollment_id found"
    return None


def validate_person(df: pd.DataFrame) -> None:
    assert (
        df.duplicated(subset=["associate_id"]).sum() == 0
    ), "Duplicate associate_id found"
    return None


def transform_legal_entity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Many records have conflicting information, depending on which file the ownership record originated from.

    For example:
        - One record may indicate true for "created_for_acquisition" while another may show NULL, or false.
        - One record may indicate true for "created_for_acquisition" while another may show NULL, or false.

    To keep it simple (naive?) 'Y' trumps 'N' and populated trumps NULL.
    """
    df.drop("associate_id_care_organization", axis=1, inplace=True)
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
        "other_type",
    ]

    df_booleans = (
        df.groupby(group_cols)[fields]
        .apply(lambda x: x.ffill().bfill().max())
        .reset_index()
    )
    fields = ["organization_name", "doing_business_as_name", "other_type_text"]
    df_names = (
        df.groupby(group_cols)[fields]
        .apply(lambda x: x.ffill().bfill().max())
        .reset_index()
    )
    df = pd.merge(df_booleans, df_names, on=group_cols)
    assert dedup_count == df.shape[0], "Deduplication failed"
    df["legal_entity_id"] = None  # or populate it with appropriate values
    print(f"Transformed {count} records to {df.shape[0]} records")
    return df


def transform_person(df: pd.DataFrame) -> pd.DataFrame:
    """
    If there are duplicates on first_name, middle_name, or last_name
        Order by first_name, middle_name, last_name and choose the first record
    """
    df.drop("associate_id_care_organization", axis=1, inplace=True)
    df = df.drop_duplicates(
        subset=["associate_id", "first_name", "middle_name", "last_name"]
    )
    start_count = df.shape[0]
    df = df.sort_values(by=["associate_id", "first_name", "middle_name", "last_name"])
    df = df.drop_duplicates(subset=["associate_id"], keep="first")
    assert (
        (start_count - df.shape[0]) / start_count
    ) < 0.001, "More than 0.1% of records were affected"
    return df


def transform_person_ownership(df: pd.DataFrame) -> pd.DataFrame:
    # filter to ownership roles
    df = df.loc[df["role_code"].isin(["34", "35", "36", "37", "38", "39"])]
    return df


def validate_legal_entity(df: pd.DataFrame) -> None:
    assert (
        df.duplicated(subset=["associate_id"]).sum() == 0
    ), "Duplicate associate_id found"
    return None


# ETL mappings, commented out w/e you don't want to load
ETL_MAPPINGS = [
    KuzuObjectLoader(
        target_table="PECOSEnrolledCareProvider",
        source_table="vw_enrolled_care_provider_organizations",
        transform_func=None,
        validate_func=validate_care_provider_organizations,
    ),
    # KuzuObjectLoader(
    #     target_table="LegalEntity",
    #     source_table="vw_extract_organization_owners",
    #     transform_func=transform_legal_entity,
    #     validate_func=validate_legal_entity
    # ),
    KuzuObjectLoader(
        target_table="Person",
        source_table="vw_person",
        transform_func=transform_person,
        validate_func=validate_person,
    ),
    KuzuObjectLoader(
        source_table="vw_person_affiliations",
        target_table=None,
        relation_triple=("OwnedBy", "PECOSEnrolledCareProvider", "Person"),
        transform_func=transform_person_ownership,
        validate_func=None,
    ),
]


# Main function
def load_from_sqlite(
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
    with open("src/schema/pecos_plus/kuzu/cms_ownership_entities.cypher", "r") as f:
        ddl_script = f.read()
        initialize_tables(kuzu_conn, ddl_script)

    results = kuzu_conn.execute("CALL SHOW_TABLES() RETURN *;").get_as_df()
    print(results)

    # Source DB
    sqlite_conn = sqlite3.connect(f"{data_path}/{sqlite_db_name}")

    for item in etl_mappings:
        item.load(kuzu_conn, sqlite_conn)


if __name__ == "__main__":
    load_from_sqlite(DATA_PATH, KUZU_DB_NAME, SQLITE_DB_NAME, ETL_MAPPINGS)
    kuzu_db = kuzu.Database(os.path.join(DATA_PATH, KUZU_DB_NAME))
    kuzu_conn = kuzu.Connection(kuzu_db)
    results = kuzu_conn.execute(
        "MATCH (p:PECOSEnrolledCareProvider) RETURN p.enrollment_id, p.associate_id, p.organization_name;"
    ).get_as_df()
    print(results.iloc[0:10])
