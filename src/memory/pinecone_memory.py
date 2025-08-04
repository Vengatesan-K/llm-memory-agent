import os
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Optional
from src.memory.base_memory import BaseMemory
from src.utils.embeddings import get_embedding
import time
import os
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Optional
from src.utils.embeddings import get_embedding


class PineconeMemory:
    def __init__(self, index_name: str = "gpt-memories"):
        self.api_key = os.getenv("PINECONE_API_KEY")
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY environment variable not set")

        self.index_name = index_name.lower()
        self.pc = Pinecone(api_key=self.api_key)
        self.index = self._initialize_index()

    def _initialize_index(self):
        """Initialize or connect to Pinecone index with proper spec"""
        # First check if index exists
        existing_indexes = self.pc.list_indexes().names()

        if self.index_name in existing_indexes:
            print(f"✅ Using existing Pinecone index: {self.index_name}")
            return self.pc.Index(self.index_name)

        # Create new index with serverless spec
        print(f"🛠️ Creating new Pinecone index: {self.index_name}")

        try:
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,  # Standard for OpenAI embeddings
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            # Wait for index to be ready
            time.sleep(1)
            return self.pc.Index(self.index_name)
        except Exception as e:
            print(f"❌ Failed to create index: {str(e)}")
            raise

    def store_memory(self, user_id: str, text: str, metadata: Dict = None) -> str:
        """Store memory in Pinecone"""
        vector_id = f"{user_id}_{int(time.time())}"
        try:
            self.index.upsert(
                vectors=[
                    {
                        "id": vector_id,
                        "values": get_embedding(text),
                        "metadata": {
                            "text": text,
                            "user_id": user_id,
                            **(metadata or {}),
                        },
                    }
                ]
            )
            return vector_id
        except Exception as e:
            print(f"❌ Failed to store memory: {str(e)}")
            raise

    def retrieve_memories(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        """Retrieve relevant memories"""
        try:
            results = self.index.query(
                vector=get_embedding(query),
                top_k=limit,
                filter={"user_id": user_id},
                include_metadata=True,
            )
            return [
                {"text": match.metadata["text"], "score": match.score, "id": match.id}
                for match in results.matches
            ]
        except Exception as e:
            print(f"❌ Failed to retrieve memories: {str(e)}")
            return []

    def clear_memories(self, user_id: str):
        """Clear all memories for a user"""
        try:
            self.index.delete(filter={"user_id": user_id})
            return True
        except Exception as e:
            print(f"❌ Failed to clear memories: {str(e)}")
            return False
