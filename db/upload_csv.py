"""
Script to upload CSV files to MongoDB
Usage: python -m db.upload_csv <csv_file_path> <collection_name> [--clear]
"""
import sys
import csv
import argparse
from pathlib import Path
from .db_connection import MongoDBConnection


def upload_csv_to_mongodb(csv_file_path, collection_name, clear_existing=False):
    """
    Upload CSV file to MongoDB collection
    
    Args:
        csv_file_path: Path to the CSV file
        collection_name: Name of the MongoDB collection
        clear_existing: If True, clear existing documents in collection before inserting
    """
    # Validate CSV file exists
    csv_path = Path(csv_file_path)
    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_file_path}")
        return False
    
    if not csv_path.is_file():
        print(f"Error: Path is not a file: {csv_file_path}")
        return False
    
    print(f"Reading CSV file: {csv_file_path}")
    
    try:
        # Read CSV and convert to list of dictionaries
        documents = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            # Try to detect encoding if utf-8 fails
            try:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
                    # Clean empty strings and convert to None for better MongoDB handling
                    cleaned_row = {k: (v if v else None) for k, v in row.items()}
                    documents.append(cleaned_row)
            except UnicodeDecodeError:
                # Try with utf-8-sig (BOM) or latin-1
                f.seek(0)
                try:
                    reader = csv.DictReader(f, encoding='utf-8-sig')
                    for row_num, row in enumerate(reader, start=2):
                        cleaned_row = {k: (v if v else None) for k, v in row.items()}
                        documents.append(cleaned_row)
                except:
                    f.seek(0)
                    reader = csv.DictReader(f, encoding='latin-1')
                    for row_num, row in enumerate(reader, start=2):
                        cleaned_row = {k: (v if v else None) for k, v in row.items()}
                        documents.append(cleaned_row)
        
        if not documents:
            print("Warning: No data found in CSV file")
            return False
        
        print(f"Found {len(documents)} rows in CSV file")
        
        # Connect to MongoDB
        print(f"Connecting to MongoDB...")
        db_conn = MongoDBConnection()
        collection = db_conn.get_collection(collection_name)
        
        # Clear existing documents if requested
        if clear_existing:
            count = collection.count_documents({})
            if count > 0:
                print(f"Clearing {count} existing documents from '{collection_name}' collection...")
                collection.delete_many({})
                print("Collection cleared")
        
        # Insert documents
        print(f"Uploading {len(documents)} documents to '{collection_name}' collection...")
        result = collection.insert_many(documents)
        
        print(f"\n✓ Successfully uploaded {len(result.inserted_ids)} documents to '{collection_name}' collection")
        print(f"  Collection: {collection_name}")
        print(f"  Documents inserted: {len(result.inserted_ids)}")
        
        # Show sample of inserted data
        sample = collection.find_one()
        if sample:
            print(f"\nSample document fields: {', '.join(list(sample.keys())[:5])}")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file_path}")
        return False
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
        return False
    except Exception as e:
        print(f"Error uploading to MongoDB: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(
        description='Upload CSV file to MongoDB collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m db.upload_csv data/AB/ministries.csv ministries
  python -m db.upload_csv data/AB/agencies_ab.csv agencies --clear
  python -m db.upload_csv "data/FED/ministries_fed.csv" federal_ministries
        """
    )
    
    parser.add_argument('csv_file', help='Path to the CSV file to upload')
    parser.add_argument('collection', help='Name of the MongoDB collection')
    parser.add_argument('--clear', action='store_true', 
                       help='Clear existing documents in collection before inserting')
    
    args = parser.parse_args()
    
    success = upload_csv_to_mongodb(args.csv_file, args.collection, args.clear)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

