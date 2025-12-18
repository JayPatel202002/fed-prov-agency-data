"""
Example script showing how to use MongoDB with this project
"""
from .db_connection import MongoDBConnection, get_collection
import csv

def example_insert_from_csv(csv_file_path, collection_name):
    """Example: Insert data from CSV file into MongoDB"""
    db_conn = MongoDBConnection()
    
    # Read CSV and convert to list of dictionaries
    documents = []
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            documents.append(row)
    
    # Insert into MongoDB
    if documents:
        inserted_ids = db_conn.insert_many(collection_name, documents)
        print(f"Inserted {len(inserted_ids)} documents into '{collection_name}' collection")
        return inserted_ids
    else:
        print("No documents to insert")
        return []

def example_query_data(collection_name, query=None):
    """Example: Query data from MongoDB"""
    db_conn = MongoDBConnection()
    documents = db_conn.find_documents(collection_name, query)
    print(f"Found {len(documents)} documents")
    return documents

def example_usage():
    """Example usage of MongoDB connection"""
    # Initialize connection
    db_conn = MongoDBConnection()
    db = db_conn.connect()
    
    # Example: Insert a sample document
    sample_doc = {
        "region": "AB",
        "type": "ministry",
        "name": "Example Ministry",
        "website": "https://example.com"
    }
    
    collection = db_conn.get_collection("ministries")
    result = collection.insert_one(sample_doc)
    print(f"Inserted document with ID: {result.inserted_id}")
    
    # Example: Query documents
    ministries = db_conn.find_documents("ministries", {"region": "AB"})
    print(f"Found {len(ministries)} ministries from AB")
    
    # Example: Close connection (optional, will be closed when script ends)
    # db_conn.close()

if __name__ == "__main__":
    # Uncomment to test
    # example_usage()
    pass

