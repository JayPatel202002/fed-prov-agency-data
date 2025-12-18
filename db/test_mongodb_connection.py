"""
Test script to verify MongoDB connection
"""
from .db_connection import MongoDBConnection
from .config import MONGODB_URI, MONGODB_DATABASE
import sys

def test_connection():
    """Test MongoDB connection and basic operations"""
    print("=" * 50)
    print("MongoDB Connection Test")
    print("=" * 50)
    
    # Display configuration
    print(f"\nConfiguration:")
    print(f"  MongoDB URI: {MONGODB_URI[:50]}..." if len(MONGODB_URI) > 50 else f"  MongoDB URI: {MONGODB_URI}")
    print(f"  Database: {MONGODB_DATABASE}")
    print()
    
    try:
        # Test 1: Connection
        print("Test 1: Connecting to MongoDB...")
        db_conn = MongoDBConnection()
        db = db_conn.connect()
        print("✓ Connection successful!")
        print()
        
        # Test 2: Ping
        print("Test 2: Testing ping...")
        db_conn._client.admin.command('ping')
        print("✓ Ping successful!")
        print()
        
        # Test 3: Database access
        print("Test 3: Accessing database...")
        database_names = db_conn._client.list_database_names()
        print(f"✓ Database access successful!")
        print(f"  Available databases: {', '.join(database_names)}")
        print()
        
        # Test 4: Collection creation and insertion
        print("Test 4: Testing collection operations...")
        test_collection = db_conn.get_collection("connection_test")
        
        # Insert a test document
        test_doc = {
            "test": True,
            "message": "MongoDB connection test successful",
            "timestamp": "test"
        }
        result = test_collection.insert_one(test_doc)
        print(f"✓ Document inserted with ID: {result.inserted_id}")
        
        # Query the test document
        found_doc = test_collection.find_one({"_id": result.inserted_id})
        if found_doc:
            print("✓ Document retrieval successful!")
        
        # Clean up - delete test document
        test_collection.delete_one({"_id": result.inserted_id})
        print("✓ Test document cleaned up")
        print()
        
        # Test 5: List collections
        print("Test 5: Listing collections...")
        collections = db.list_collection_names()
        print(f"✓ Collections in database: {len(collections)}")
        if collections:
            print(f"  Collections: {', '.join(collections)}")
        else:
            print("  (No collections yet)")
        print()
        
        # Summary
        print("=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nMongoDB connection is working correctly!")
        print(f"You can now use the database '{MONGODB_DATABASE}' in your project.")
        
        return True
        
    except Exception as e:
        print("=" * 50)
        print("✗ CONNECTION TEST FAILED")
        print("=" * 50)
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check that your MongoDB server is running")
        print("2. Verify your connection string in the .env file")
        print("3. For MongoDB Atlas, ensure your IP is whitelisted")
        print("4. Check your username and password are correct")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

