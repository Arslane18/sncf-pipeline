import polars as pl


def get_row_count(conn, table_name: str) -> int:
    """Helper function to get the total row count of the specified table."""
    return conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]


def insert_or_replace(conn, df: pl.DataFrame, table_name: str):
    """Helper function to perform an upsert operation on the specified table."""

    conn.register("df_temp", df)

    # Create the target table if it doesn't exist (with the same schema as df)
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS raw_sncf_disruptions (
    id VARCHAR PRIMARY KEY,
    status VARCHAR,
    "severity.name" VARCHAR,
    updated_at VARCHAR,
    ingestion_ts TIMESTAMP WITH TIME ZONE,
    messages JSON
    )
    """)

    # Upsert data from df_temp into the target table, thanks to DuckDB's support for the "INSERT OR REPLACE" syntax.
    conn.execute(f"""
    INSERT OR REPLACE INTO {table_name}
    SELECT 
           id,
           status,
           "severity.name",
           updated_at,
           ingestion_ts,
           messages
    FROM df_temp
    """)
