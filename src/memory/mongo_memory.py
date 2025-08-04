import os
from datetime import datetime
from typing import List, Dict
from pymongo import MongoClient, WriteConcern
from pymongo.server_api import ServerApi
from src.memory.base_memory import BaseMemory
from src.utils.embeddings import get_embedding
from typing import List, Dict, Optional
from bson import ObjectId
import os
from datetime import datetime
from typing import List, Dict
from pymongo import MongoClient, ReturnDocument
from pymongo.server_api import ServerApi
from src.utils.embeddings import get_embedding
from pymongo.errors import OperationFailure


class MongoMemory:
    def __init__(self, collection_name: str = "user_memories"):
        self.client = MongoClient(
            os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=30000,
        )
        self.db = self.client[os.getenv("MONGO_DB_NAME", "llm_memory")]
        self.collection = self.db[collection_name]

        # Create regular indexes instead of vector index
        self._create_basic_indexes()

    def _create_basic_indexes(self):
        """Create basic text indexes that work on all MongoDB tiers"""
        try:
            # Create text index for searching
            self.collection.create_index([("text", "text")])

            # Create compound index for user_id and is_active
            self.collection.create_index([("user_id", 1), ("is_active", 1)])

            print("✅ Created basic indexes")
        except OperationFailure as e:
            print(f"⚠️ Index creation failed (non-critical): {str(e)}")
            # Continue even if index creation fails

    # In MongoMemory class
    def retrieve_memories(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        """Text-based search implementation for all MongoDB tiers

        Args:
            user_id: The user identifier
            query: The search query text
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing:
            - text: The memory text
            - score: Relevance score
            - metadata: Associated metadata
        """
        try:
            # Execute text search query
            results = (
                self.collection.find(
                    {
                        "$text": {"$search": query},
                        "user_id": user_id,
                        "is_active": True,
                    },
                    {"text": 1, "metadata": 1, "score": {"$meta": "textScore"}},
                )
                .sort([("score", {"$meta": "textScore"})])
                .limit(limit)
            )

            # Format results
            return [
                {
                    "text": doc["text"],
                    "score": doc["score"],
                    "metadata": doc.get("metadata", {}),
                }
                for doc in results
            ]

        except Exception as e:
            print(f"⚠️ Text search failed: {str(e)}")
            return []  # Return empty list on failure

    def store_memory(
        self,
        question: str,
        answer: str,
        user_id: str = None,
        conversation_id: str = None,
    ):
        """Store question-answer pair"""
        metadata = {
            "conversation_id": conversation_id,
            "type": "qa_pair",
            "question": question,
        }
        return self.store_memory(
            user_id=user_id or "global", text=answer, metadata=metadata
        )

    def update_memory(
        self, user_id: str, old_text: str, new_text: Optional[str] = None
    ) -> bool:
        self.memories.update_many(
            {"user_id": user_id, "text": old_text}, {"$set": {"is_active": False}}
        )
        if new_text:
            self.store_memory(user_id, new_text)
        return True
