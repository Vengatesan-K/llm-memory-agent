from typing import Optional
import openai
import os
from dotenv import load_dotenv

load_dotenv()


class RetrievalAgent:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def query(
        self,
        question: str,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
    ) -> str:
        """
        Query the LLM with a question and optional context

        Args:
            question: The user's question
            user_id: Optional user identifier
            conversation_id: Optional conversation tracking

        Returns:
            The generated answer
        """
        try:
            # Get relevant context from memory
            context = self._get_context(question, user_id, conversation_id)

            # Construct the prompt
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ]

            if context:
                messages.insert(
                    1, {"role": "system", "content": f"Relevant context: {context}"}
                )

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages, temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"LLM query failed: {str(e)}")

    def _get_context(
        self, question: str, user_id: Optional[str], conversation_id: Optional[str]
    ) -> str:
        """
        Retrieve relevant context from memory

        Args:
            question: The question to find context for
            user_id: Optional user identifier
            conversation_id: Optional conversation tracking

        Returns:
            Relevant context as a string
        """
        memories = self.memory_manager.retrieve_memories(
            user_id=user_id or "global", query=question, limit=3
        )

        return "\n".join([mem["text"] for mem in memories]) if memories else ""

    def is_ready(self) -> bool:
        """Check if the agent is ready to handle queries"""
        try:
            # Simple ping to verify OpenAI connection
            openai.Model.list()
            return True
        except:
            return False
