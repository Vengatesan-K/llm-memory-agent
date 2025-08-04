import sys
import os
from dotenv import load_dotenv

load_dotenv()


# Add 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.memory.mongo_memory import MongoMemory
from src.memory.manager import MemoryManager
from src.agents.retrieval_agent import RetrievalAgent
import unittest
from bson import ObjectId

load_dotenv()
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    load_dotenv()

    try:
        # 1. Initialize with verification
        logger.info("Initializing MongoDB connection...")
        db = MongoMemory()
        manager = MemoryManager(db)
        agent = RetrievalAgent(manager)
        logger.info("✅ Components initialized successfully")

        # Test user ID
        user_id = "demo_user"

        # 2. Clear previous test data
        logger.info("Clearing previous test data...")
        db.memories.delete_many({"user_id": user_id})

        # 3. Store test memory
        test_memory = "I work at Tesla and use Python daily"
        logger.info(f"Storing test memory: '{test_memory}'")
        memory_id = manager.store_memory(user_id, test_memory)
        logger.info(f"✅ Memory stored with ID: {memory_id}")

        # 4. Verify with proper ObjectId conversion
        logger.info("Verifying direct database access...")
        stored = db.memories.find_one(
            {"_id": ObjectId(memory_id)}
        )  # Convert string to ObjectId
        if stored:
            logger.info(f"✅ Found stored document: {stored['text']}")
        else:
            logger.error("❌ No document found!")
            return

        # 5. Test semantic search
        query = "What programming language do I use?"
        logger.info(f"Searching for: '{query}'")
        memories = manager.get_relevant_memories(user_id, query)
        if memories:
            logger.info("✅ Search results:")
            for i, mem in enumerate(memories, 1):
                logger.info(f"{i}. {mem['text']} (score: {mem['score']:.3f})")
        else:
            logger.error("❌ No memories found!")
            return

        # 6. Test full agent response
        question = "Where do I work?"
        logger.info(f"Asking agent: '{question}'")
        answer = agent.retrieve_and_answer(user_id, question)
        logger.info(f"🤖 Agent response: {answer}")

    except Exception as e:
        logger.error(f"❌ Operation failed: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
