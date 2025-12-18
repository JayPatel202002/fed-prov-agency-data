from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from .config import MONGODB_URI, MONGODB_DATABASE

class MongoDBConnection:
    """Singleton class for MongoDB connection management"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            if self._client is None:
                self._client = MongoClient(MONGODB_URI)
                # Test the connection
                self._client.admin.command('ping')
                self._db = self._client[MONGODB_DATABASE]
                print(f"Successfully connected to MongoDB: {MONGODB_DATABASE}")
            return self._db
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
        except ConfigurationError as e:
            print(f"MongoDB configuration error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error connecting to MongoDB: {e}")
            raise
    
    def get_database(self):
        """Get the database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def get_collection(self, collection_name):
        """Get a collection from the database"""
        db = self.get_database()
        return db[collection_name]
    
    def close(self):
        """Close the MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("MongoDB connection closed")
    
    def insert_document(self, collection_name, document):
        """Insert a single document into a collection"""
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return result.inserted_id
    
    def insert_many(self, collection_name, documents):
        """Insert multiple documents into a collection"""
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        return result.inserted_ids
    
    def find_documents(self, collection_name, query=None, limit=None):
        """Find documents in a collection"""
        collection = self.get_collection(collection_name)
        if query is None:
            query = {}
        cursor = collection.find(query)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    
    def update_document(self, collection_name, query, update, upsert=False):
        """Update a document in a collection"""
        collection = self.get_collection(collection_name)
        result = collection.update_one(query, {"$set": update}, upsert=upsert)
        return result
    
    def delete_document(self, collection_name, query):
        """Delete documents from a collection"""
        collection = self.get_collection(collection_name)
        result = collection.delete_many(query)
        return result.deleted_count


# Convenience function to get database instance
def get_db():
    """Get MongoDB database instance"""
    db_conn = MongoDBConnection()
    return db_conn.get_database()


# Convenience function to get collection
def get_collection(collection_name):
    """Get MongoDB collection instance"""
    db_conn = MongoDBConnection()
    return db_conn.get_collection(collection_name)

