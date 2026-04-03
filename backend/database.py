from pymongo import MongoClient
from dotenv import load_dotenv
import os
from urllib.parse import urlparse, unquote

load_dotenv(override=True)

_client = None


def _extract_db_name_from_uri(mongo_uri):
    """Try to infer db name from URI path; fallback to env/default."""
    parsed = urlparse(mongo_uri)
    path = (parsed.path or "").lstrip("/")
    return path if path else os.getenv("MONGO_DB_NAME", "capisnap")

def get_database():
    global _client
    try:
        # Get MongoDB URI from environment
        MONGO_URI = os.getenv('MONGO_URI', '').strip()
        
        if not MONGO_URI:
            raise ValueError("MONGO_URI not found in environment variables")

        # Helpful diagnostics for common URI mistakes, like unencoded special chars
        if MONGO_URI.count('@') > 1:
            print("⚠️ Mongo URI looks malformed: credentials may contain unencoded special characters.")
            print("   Tip: URL-encode password characters like @ as %40")
        
        if _client is None:
            # Create and cache a connection
            _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        _client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")

        db_name = os.getenv('MONGO_DB_NAME', '').strip() or _extract_db_name_from_uri(MONGO_URI)
        
        # Return database instance
        return _client[db_name]
        
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