from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class BaseMemory(ABC):
    @abstractmethod
    def store_memory(self, user_id: str, text: str, metadata: Dict = None) -> str:
        pass

    @abstractmethod
    def retrieve_memories(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        pass

    @abstractmethod
    def update_memory(
        self, user_id: str, old_text: str, new_text: Optional[str] = None
    ) -> bool:
        pass
