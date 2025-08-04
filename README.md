# llm-memory-agent
A long-term memory system for GPT using OpenAI API

This test script (test_pinecone.py) demonstrates how memory storage and retrieval work using Pinecone vector database integration. It is designed to validate the memory insertion, similarity search, and cleanup functionalities of your LLM-powered memory agent.

🚀 What It Does
Connects to Pinecone

Reuses an existing index (test-memories) or connects to it if already available.

Stores a Test Memory

Example memory stored:
"I use Shram and Magnet as productivity tools"
(with user ID: test_user_123_1754300374)

Queries the Memory

Searches with the prompt:
- "What are the productivity tools that I use?"

- Displays Results

- Returns matching memory and its similarity score (e.g., 0.66).

- Cleans Up

- Deletes the test memory after verification.

## How to Run the Test
#### Ensure you're in your Python virtual environment and run:

D:/llm-memory-agent/.venv/Scripts/python.exe d:/llm-memory-agent/tests/test_pinecone.py
<img width="809" height="426" alt="image" src="https://github.com/user-attachments/assets/300ea4b7-b334-4b6d-b391-bca8c3f0bb0c" />
