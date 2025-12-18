import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in the project root (parent directory)
from pathlib import Path
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "fed_prov_agency_data")

