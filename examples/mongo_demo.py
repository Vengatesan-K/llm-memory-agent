# In tests/test_mongo.py (at the start of test_retrieval)
from pymongo import MongoClient
import os

# Direct connection check
# client = MongoClient(os.getenv("MONGODB_URI"))
# db = client["gpt_memory"]
# print("All documents in collection:", list(db.user_memories.find({}, {"text": 1})))


from urllib.parse import quote_plus
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


# def get_mongo_client():
#     try:
#         # For local MongoDB
#         if os.getenv("MONGODB_URI", "").startswith("mongodb://localhost"):
#             return MongoClient(os.getenv("MONGODB_URI"))

#         # For MongoDB Atlas with proper encoding
#         username = quote_plus(os.getenv("MONGO_USER", ""))
#         password = quote_plus(os.getenv("MONGO_PASS", ""))
#         cluster = os.getenv("MONGO_CLUSTER", "")

#         uri = f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/?retryWrites=true&w=majority"
#         return MongoClient(uri, serverSelectionTimeoutMS=5000)

#     except Exception as e:
#         print(f"❌ Connection failed: {e}")
#         raise

# At the start of mongo_demo.py
# from pymongo import MongoClient
# client = MongoClient(os.getenv("MONGODB_URI"), serverSelectionTimeoutMS=5000)
# try:
#     client.server_info()
#     print("✅ MongoDB connection successful")
# except Exception as e:
#     print(f"❌ MongoDB connection failed: {e}")
#     exit(1)


# Right after store_memory() call in your test
from bson import ObjectId

# Verify using raw PyMongo
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["gpt_memory"]
memory_id = "68904440541b6ee96cd61c9e"
stored = db.user_memories.find_one({"_id": ObjectId(memory_id)})
print("Raw document lookup:", stored)

# Add this before storage test
print("All collections:", db.list_collection_names())


from pymongo import MongoClient
from bson import ObjectId


# Direct connection bypassing your Memory class
# def test_collection_reference():
#     """Verify both methods use the same collection"""
#     from src.memory.mongo_memory import MongoMemory

#     # Direct connection
#     client = MongoClient(os.getenv("MONGODB_URI"))
#     direct_coll = client["gpt_memory"]["user_memories"]

#     # Class connection
#     memory_db = MongoMemory()
#     class_coll = memory_db.memories

#     print("\n=== Collection Verification ===")
#     print(f"Direct collection: {direct_coll.full_name}")
#     print(f"Class collection: {class_coll.full_name}")
#     print(f"Same collection? {direct_coll.full_name == class_coll.full_name}")

#     # Test insert through both references
#     test_id = direct_coll.insert_one({"test": "direct"}).inserted_id
#     print(
#         f"\nDirect insert found via class: {bool(class_coll.find_one({'_id': test_id}))}"
#     )

#     test_id = class_coll.insert_one({"test": "class"}).inserted_id
#     print(
#         f"Class insert found via direct: {bool(direct_coll.find_one({'_id': test_id}))}"
#     )
from dotenv import load_dotenv

load_dotenv()
import sys

# Add 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.memory.manager import MemoryManager
import time
from src.memory.mongo_memory import MongoMemory


# Check collection exists
coll_names = db.client["gpt_memory"].list_collection_names()
print("Existing collections:", coll_names)
assert "user_memories" in coll_names, "user_memories collection missing"

# Verify reference
assert (
    db.memories.name == "user_memories"
), f"Collection name mismatch. Using: {db.memories.name}, Expected: user_memories"
