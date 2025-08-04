from fastapi import FastAPI, HTTPException
from src.agents.retrieval_agent import RetrievalAgent
from src.api.schemas import QueryRequest, QueryResponse
from src.memory.manager import MemoryManager
import os

from fastapi import FastAPI, HTTPException
from src.agents.retrieval_agent import RetrievalAgent
from src.api.schemas import QueryRequest, QueryResponse
from src.memory.manager import MemoryManager
from src.memory.mongo_memory import MongoMemory  # or PineconeMemory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="LLM Memory Agent API",
    description="API for querying with memory-enhanced LLM agents",
    version="0.1.0",
)

# Initialize memory database
db = MongoMemory()

# Initialize components
memory_manager = MemoryManager(db)
retrieval_agent = RetrievalAgent(memory_manager)


@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    try:
        # Input validation
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Cache lookup
        if request.use_cache:
            try:
                cached_answer = memory_manager.retrieve_memory(
                    question=request.question,
                    user_id=request.user_id,
                    conversation_id=request.conversation_id,
                )
                if cached_answer:
                    return QueryResponse(
                        answer=cached_answer,
                        source="cache",
                        conversation_id=request.conversation_id,
                        cached=True,
                    )
            except Exception as e:
                raise

        # LLM Query
        try:
            answer = retrieval_agent.query(
                question=request.question,
                user_id=request.user_id,
                conversation_id=request.conversation_id,
            )
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")

        # Store result
        try:
            memory_manager.store_memory(
                question=request.question,
                answer=answer,
                user_id=request.user_id,
                conversation_id=request.conversation_id,
            )
        except Exception as e:
            raise
        return QueryResponse(
            answer=answer,
            source="llm",
            conversation_id=request.conversation_id,
            cached=False,
        )

    except HTTPException:
        raise


@app.get("/health")
async def health_check():
    status = {"status": "healthy", "services": {}}

    # Check MongoDB
    try:
        memory_manager.db.client.admin.command("ping")
        status["services"]["mongodb"] = "healthy"
    except Exception as e:
        status["services"]["mongodb"] = f"unhealthy: {str(e)}"
        status["status"] = "degraded"

    # Check LLM
    try:
        retrieval_agent.ping()  # Implement this method in your agent
        status["services"]["llm"] = "healthy"
    except Exception as e:
        status["services"]["llm"] = f"unhealthy: {str(e)}"
        status["status"] = "degraded"

    return status
