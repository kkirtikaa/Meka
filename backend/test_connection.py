from database import get_database

def test_mongodb_connection():
    print("Testing MongoDB connection...")
    
    db = get_database()
    
    if db is not None:  # Changed from "if db:"
        print("\n✅ Connection successful!")
        print(f"Database name: {db.name}")
        
        # Try to list collections
        collections = db.list_collection_names()
        print(f"Collections: {collections if collections else 'No collections yet'}")
        
        # Try a simple operation
        test_collection = db['test']
        result = test_collection.insert_one({'test': 'data'})
        print(f"Test insert ID: {result.inserted_id}")
        
        # Clean up test data
        test_collection.delete_one({'_id': result.inserted_id})
        print("✅ All tests passed!")
    else:
        print("❌ Connection failed!")

if __name__ == "__main__":
    test_mongodb_connection()