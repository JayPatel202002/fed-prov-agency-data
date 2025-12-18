# fed-prov-agency-data
FPMGAABBCCCCCCCOSSTM

## MongoDB Setup

This project now supports MongoDB for data storage. Follow these steps to connect MongoDB:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure MongoDB Connection

Create a `.env` file in the project root with your MongoDB connection details:

```env
# For local MongoDB
MONGODB_URI=mongodb://localhost:27017/

# For MongoDB Atlas (cloud)
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Database name
MONGODB_DATABASE=fed_prov_agency_data
```

### 3. Usage

#### Basic Connection

```python
from db.db_connection import MongoDBConnection, get_collection

# Initialize connection
db_conn = MongoDBConnection()
db = db_conn.connect()

# Get a collection
collection = db_conn.get_collection("ministries")

# Insert a document
document = {"region": "AB", "name": "Example Ministry"}
result = collection.insert_one(document)
print(f"Inserted ID: {result.inserted_id}")

# Query documents
documents = db_conn.find_documents("ministries", {"region": "AB"})
```

#### Insert Data from CSV

```python
from db.db_connection import MongoDBConnection
import csv

db_conn = MongoDBConnection()

# Read CSV and insert into MongoDB
documents = []
with open("data/AB/ministries.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        documents.append(row)

if documents:
    db_conn.insert_many("ministries", documents)
```

See `db/example_mongodb_usage.py` for more examples.

### Testing Connection

To test your MongoDB connection, run:

```bash
python -m db.test_mongodb_connection
```

### MongoDB Collections

Suggested collection names:
- `ministries` - Ministry/Department data
- `agencies` - Agency data
- `agency_members` - Agency member data