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
import kuzu


def initialize_tables(conn: kuzu.Connection, ddl_script: str) -> None:
    conn.execute(ddl_script)

def create_transaction_edge_file(conn: kuzu.Connection) -> None:
    """
    Create a new file `transacted_with.csv` that stores the
    edges between clients and merchants, with metadata.
    No headers are written
    """
    conn.execute(
    f"""
    COPY (
        LOAD FROM '{DATA_PATH}/transaction.csv' (header=true)
        RETURN
            client_id,
            merchant_id,
            amount_usd,
            timestamp
    )
    TO '{DATA_PATH}/transacted_with.csv';
    """
    )

def main(conn: kuzu.Connection, DATA_PATH: Path) -> None:
    # Initialize tables
    with open("src/schema/kuzu/cms_ownership_entities.cypher", "r") as f:
        ddl_script = f.read()
        initialize_tables(conn, ddl_script)
    
    # Ingest nodes
    # conn.execute(f"COPY Client FROM '{DATA_PATH}/client.csv' (header=true);")
    # conn.execute(f"COPY City FROM '{DATA_PATH}/city.csv' (header=true);")
    # conn.execute(f"COPY Company FROM '{DATA_PATH}/company.csv' (header=true);")
    # conn.execute(f"COPY Merchant FROM '{DATA_PATH}/merchant.csv' (header=true);")
    # print("Loaded nodes into KùzuDB")

    # Ingest edges
    # conn.execute(f"COPY TransactedWith FROM '{DATA_PATH}/transacted_with.csv';")
    # conn.execute(f"COPY BelongsTo FROM '{DATA_PATH}/belongs_to.csv';")
    # conn.execute(f"COPY LocatedIn FROM '{DATA_PATH}/located_in.csv';")
    # print("Loaded edges into KùzuDB")

if __name__ == "__main__":
    DATA_PATH = Path("data/staging")
    DB_NAME = "pecos_plus.db"
    DEST_PATH = os.path.join(DATA_PATH, DB_NAME)
    # Delete directory each time till we have MERGE FROM available in kuzu
    if os.path.exists(DEST_PATH):
        shutil.rmtree(DEST_PATH)
    
    # Create database
    db = kuzu.Database(f"{DATA_PATH}/{DB_NAME}")
    conn = kuzu.Connection(db)
    main(conn, DATA_PATH)
