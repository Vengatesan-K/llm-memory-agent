import os
from pymongo import MongoClient
import sys
import os
from dotenv import load_dotenv

load_dotenv()


# Add 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.memory.mongo_memory import MongoMemory
from bson import ObjectId


def verify_system():
    # 1. Test direct connection
    client = MongoClient(os.getenv("MONGODB_URI"))
    print("Collections:", client["gpt_memory"].list_collection_names())

    # 2. Test class functionality
    db = MongoMemory()
    test_text = "Verification test"
    memory_id = db.store_memory("verify_user", test_text)

    # 3. Verify
    stored = db.memories.find_one({"_id": ObjectId(memory_id)})
    print("Stored document:", stored["text"] if stored else "NOT FOUND")

    # 4. Cleanup
    db.memories.delete_many({"user_id": "verify_user"})


if __name__ == "__main__":
    verify_system()
