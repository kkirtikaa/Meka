from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database():
    try:
        # Get MongoDB URI from environment
        MONGO_URI = os.getenv('MONGO_URI')
        
        if not MONGO_URI:
            raise ValueError("MONGO_URI not found in environment variables")
        
        # Create a connection
        client = MongoClient(MONGO_URI)
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        
        # Return database instance
        return client['capisnap']  # Replace 'capisnap' with your database name
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        return None

# Get users collection
def get_users_collection():
    db = get_database()
    if db is not None:  # Changed from "if db:"
        return db['users']
    return None

# Test the connection
if __name__ == "__main__":
    db = get_database()
    if db is not None:  # Changed from "if db:"
        print(f"Database: {db.name}")
        print(f"Collections: {db.list_collection_names()}")