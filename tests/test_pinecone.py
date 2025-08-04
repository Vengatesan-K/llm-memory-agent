import os
import sys

# Add 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv
from src.memory.pinecone_memory import PineconeMemory
from src.utils.embeddings import get_embedding
import time

load_dotenv()


def run_pinecone_demo():
    print("🚀 Starting Pinecone Memory Demo")

    try:
        # Initialize with test index name
        print("🔌 Connecting to Pinecone...")
        pinecone = PineconeMemory(index_name="test-memories")
        print("✅ Pinecone connection established")

        # Test user ID
        user_id = "test_user_123"

        # Demo data
        memories = [
            "My favorite programming language is Python",
            "I enjoy building AI applications",
            "I have 3 years of experience with machine learning",
        ]

        # Store memories
        print("\n💾 Storing test memories:")
        for mem in memories:
            mem_id = pinecone.store_memory(user_id, mem)
            print(f"  - {mem} (ID: {mem_id})")
            time.sleep(1)  # Avoid rate limiting

        # Test query
        query = "What programming experience do I have?"
        print(f"\n🔍 Querying: '{query}'")
        results = pinecone.retrieve_memories(user_id, query)

        if results:
            print("🎯 Results:")
            for i, res in enumerate(results, 1):
                print(f"  {i}. {res['text']} (score: {res['score']:.2f})")
        else:
            print("❌ No results found")

        # Cleanup
        print("\n🧹 Cleaning up test data...")
        pinecone.clear_memories(user_id)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        print("\n🏁 Demo completed")


if __name__ == "__main__":
    run_pinecone_demo()
