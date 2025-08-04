import os

# Root directory
root = r"D:\llm-memory-agent"

# File structure to create
file_structure = [
    "requirements.txt",
    "src/__init__.py",
    "src/memory/__init__.py",
    "src/memory/base_memory.py",
    "src/memory/mongo_memory.py",
    "src/memory/pinecone_memory.py",
    "src/memory/manager.py",
    "src/agents/__init__.py",
    "src/agents/retrieval_agent.py",
    "src/agents/prompts.py",
    "src/utils/__init__.py",
    "src/utils/embeddings.py",
    "src/utils/memory_extractor.py",
    "src/api/__init__.py",
    "src/api/endpoints.py",
    "src/api/schemas.py",
    "tests/__init__.py",
    "tests/test_mongo.py",
    "tests/test_pinecone.py",
    "examples/mongo_demo.py",
    "examples/pinecone_demo.py",
]

# Create each file and its parent directories
for relative_path in file_structure:
    file_path = os.path.join(root, relative_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        pass  # Creates an empty file

print("✅ Project structure created successfully at:", root)
