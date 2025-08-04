from typing import List, Dict
from src.memory.base_memory import BaseMemory


class MemoryManager:
    def __init__(self, memory_db: BaseMemory):
        self.db = memory_db

    def store_memory(self, user_id: str, text: str, metadata: Dict = None) -> str:
        return self.db.store_memory(user_id, text, metadata)

    def get_relevant_memories(
        self, user_id: str, query: str, limit: int = 5
    ) -> List[Dict]:
        return self.db.retrieve_memories(user_id, query, limit)

    def update_user_memory(
        self, user_id: str, old_text: str, new_text: str = None
    ) -> bool:
        return self.db.update_memory(user_id, old_text, new_text)
