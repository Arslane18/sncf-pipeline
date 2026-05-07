from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

# SNCF API
SNCF_API_URL = "https://api.sncf.com/v1/coverage/sncf/disruptions"
SNCF_TOKEN = os.getenv("SNCF_TOKEN")

# Database
DB_PATH = "data/sncf.duckdb"

# DBT
DBT_PROJECT_DIR = Path(__file__).parent.parent / "dbt_scnf"
