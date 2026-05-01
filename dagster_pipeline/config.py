from dotenv import load_dotenv
import os

load_dotenv()


SNCF_API_URL = "https://api.sncf.com/v1/coverage/sncf/disruptions"
SNCF_TOKEN = os.getenv("SNCF_TOKEN")