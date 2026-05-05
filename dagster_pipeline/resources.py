import duckdb
import requests
from pathlib import Path
from dagster import ConfigurableResource
from .config import DB_PATH
 
 
class SNCFResource(ConfigurableResource):
    sncf_token: str | None
 
    def connect(self, api_url: str):
        """Establishes a connection to the SNCF API and returns the response data."""
        resp = requests.get(
            api_url,
            headers={"Authorization": self.sncf_token},
            params={"count": 100}
        )
        resp.raise_for_status()
        return resp.json()
 
 
class DuckDBResource(ConfigurableResource):
    database_path: str = DB_PATH
 
    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """Returns a DuckDB connection to the configured database."""
        return duckdb.connect(self.database_path)